import re, requests
from abp.filters import parse_filterlist
domain_list_base = './domain-list-community/data/'

def import_processor(src, exclusion=None):
    import_regex = '^include\:(\S*)$'
    content = []
    for line in src:
        import_flag = re.match(import_regex, line)
        if import_flag and import_flag.group(1) != exclusion:
            import_file = open(domain_list_base + import_flag.group(1), mode='r').read().split('\n')
            for line in import_processor(import_file, exclusion):
                content.append(line)
        content.append(line)
    return content

def convert(src, target):
    # The following 2 regexes' group 1 matches domains without "@cn" directive.
    fulldomain_regex = '^full\:(\S*)(?: @cn)?$'
    subdomain_regex = '^([a-zA-Z0-9-]*(?:\.\S*)?)(?: @cn)?$'
    invaild_regex = '^(?:regexp\:|keyword\:).*$'
    list = []
    for line in src:
        fulldomain = re.match(fulldomain_regex, line)
        subdomain = re.match(subdomain_regex, line)
        invaild = re.match(invaild_regex, line)
        if target == 'surge':
            if fulldomain:
                line = fulldomain.group(1)
                list.append(line)
            elif subdomain and subdomain.group(1) != '':
                line = subdomain.group(1)
                list.append('.' + line)
            elif invaild:
                pass
        elif target == 'clash':
            if fulldomain:
                line = "  - '" + fulldomain.group(1) + "'"
                list.append(line)
            elif subdomain and subdomain.group(1) != '':
                line = "  - '+." + subdomain.group(1) + "'"
                list.append(line)
            elif invaild:
                pass
        else:
            raise TypeError("Target type unsupported, only accept 'surge' or 'clash'.")
    if target == 'surge':
        list.sort()
    else:
        list.sort()
        list.insert(0, "payload:")
    return list

def batch_convert(targets, tools, exclusions=[]):
    for tool in tools:
        for target in targets:
            for exclusion in exclusions:
                o_file = open(domain_list_base + target, mode='r').read().split('\n')
                dist = open("./dists/" + tool + "/" + target + ".txt", mode='w')
                o_content = import_processor(o_file, exclusion)
                list = convert(o_content, tool)
                for line in list:
                    dist.writelines(line + '\n')
                dist.close()

# Stage 1: Sync advertisements blocking and privacy protection rules with AdGuard Base, CN, JP, Mobile filters and EasyList China.
regex_ip = '((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}' ## IP addresses shouldn't be added.
url_base = 'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt'
url_cn = 'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/ChineseFilter/sections/adservers.txt'
url_jp = 'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/JapaneseFilter/sections/adservers.txt'
url_mobile = 'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt'
url_extend = 'https://easylist-downloads.adblockplus.org/easylistchina.txt'
dist_surge = open('./dists/surge/protection.txt', mode='w')
dist_clash = open('./dists/clash/protection.txt', mode='w')

content = (
    requests.get(url_base).text +
    requests.get(url_cn).text +
    requests.get(url_jp).text +
    requests.get(url_mobile).text +
    requests.get(url_extend).text
    ).splitlines()

exceptions = []

for line in parse_filterlist(content):
    if (line.type == 'filter'
    and line.action == 'block'
    and line.selector['type'] == 'url-pattern'
    and line.text.find('/') == -1
    and line.text.find('*') == -1
    and line.text.find('=') == -1
    and line.text.find('~') == -1
    and not re.search(regex_ip, line.text)
    and not line.text.startswith('_')
    and not line.text.endswith('.')
    and not line.text.endswith('_')
    and not line.options):
        if line.text.startswith('.'):
            domain = line.text.replace('.', '').replace('^', '')
            dist_surge.writelines('.' + domain + '\n')
            dist_clash.writelines("  - '+." + domain + "'" + '\n')
        else:
            domain = line.text.replace("||", '').replace('^', '')
            dist_surge.writelines('.' + domain + '\n')
            dist_clash.writelines("  - '+." + domain + "'" + '\n')
    if (line.type == 'filter'
    and line.action == 'allow'
    and line.selector['type'] == 'url-pattern'
    and line.text.find('/') == -1
    and line.text.find('*') == -1
    and line.text.find('=') == -1
    and line.text.find('~') == -1
    and not re.search(regex_ip, line.text)
    and not line.text.startswith('_')
    and not line.text.endswith('.')
    and not line.text.endswith('_')
    and not line.options):
        exceptions.append(line.text)

dist_surge.close()
dist_clash.close()
# Stage 1 finished.

# Stage 2: Remove redundant rules.
dist_surge = open('./dists/surge/protection.txt', mode='r')
dist_clash = open('./dists/clash/protection.txt', mode='r')
list_domain_surge = dist_surge.read().splitlines()
list_domain_clash = dist_clash.read().splitlines()
## After loading temporary rules, reopen rule files as write mode.
dist_surge.close()
dist_surge = open('./dists/surge/protection.txt', mode='w')
dist_clash.close()
dist_clash = open('./dists/clash/protection.txt', mode='w')
regex_domain_suffix_surge = '^\.(\S*)$'
regex_domain_suffix_clash = "^  - '\+\.(\S*)'$"
list_domain_suffix_surge = []
list_domain_suffix_clash = []
## Split domain suffixes from domain_list to list_domain_suffix.
for line in list_domain_surge[:]:
    domain_suffix = re.match(regex_domain_suffix_surge, line)
    if domain_suffix:
        list_domain_suffix_surge.append(domain_suffix[1])
        list_domain_surge.remove(line)
for line in list_domain_clash[:]:
    domain_suffix = re.match(regex_domain_suffix_clash, line)
    if domain_suffix:
        list_domain_suffix_clash.append(domain_suffix[1])
        list_domain_clash.remove(line)
## If a second-level domain has been blocked, then remove all the subdomains of it if exist.
for line in list_domain_surge[:]:
    for line2 in list_domain_suffix_surge:
        if line.find(line2) != -1:
            list_domain_surge.remove(line)
            break
for line in list_domain_clash[:]:
    for line2 in list_domain_suffix_clash:
        if line.find(line2) != -1:
            list_domain_clash.remove(line)
            break
content_surge = []
content_clash = []
for line in list_domain_suffix_surge:
    content_surge.append('.' + line)
for line in list_domain_suffix_clash:
    content_clash.append("  - '+." + line + "'")
for line in list_domain_surge:
    content_surge.append(line)
for line in list_domain_clash:
    content_clash.append(line)

content_surge = list(set(content_surge))
content_clash = list(set(content_clash))
content_surge.sort()
content_clash.sort()
content_clash.insert(0, "payload:")

for line in content_surge:
    dist_surge.writelines(line + '\n')
for line in content_clash:
    dist_clash.writelines(line + '\n')
dist_surge.close()
dist_clash.close()
# Stage 2 finished.

# Stage 3: Sync exceptions with AdGuard.
url_exceptions_1 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt'
url_exceptions_2 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt'
dist_surge = open('./dists/surge/exceptions.txt', mode='w')
dist_clash = open('./dists/clash/exceptions.txt', mode='w')
content_exceptions = (requests.get(url_exceptions_1).text + requests.get(url_exceptions_2).text).splitlines() + exceptions
exceptions_list_surge = []
exceptions_list_clash = []
for line in parse_filterlist(content_exceptions):
    if (line.type == 'filter'
    and line.selector['type'] == 'url-pattern'
    and line.text.find('/') == -1
    and line.text.find('*') == -1
    and line.text.find('=') == -1
    and not re.search('((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}', line.text)
    and not line.text.startswith('_')
    and not line.text.endswith('.')
    and not line.text.endswith('_')
    and not line.options):
        domain = line.text.replace('@','').replace('^','').replace('|','')
        if not domain.startswith('-'):
            exceptions_list_surge.append(domain)
            exceptions_list_clash.append("  - '" + domain + "'")

exceptions_list_surge = list(set(exceptions_list_surge))
exceptions_list_clash = list(set(exceptions_list_clash))
exceptions_list_surge.sort()
exceptions_list_clash.sort()
exceptions_list_clash.insert(0, "payload:")

for line in exceptions_list_surge:
    dist_surge.writelines(line + '\n')
for line in exceptions_list_clash:
    dist_clash.writelines(line + '\n')
dist_surge.close()
dist_clash.close()
# Stage 3 finished.

# Stage 4: Sync Bahamut, CN, DMM, Google FCM, Microsoft, niconico, PayPal and YouTube domains with v2fly community.
to_convert = ['bahamut', 'geolocation-cn', 'dmm', 'googlefcm', 'microsoft', 'niconico', 'paypal', 'youtube']
exclusion = ['github'] ## GitHub's domains are included in "microsoft", but its connectivity mostly isn't as high as Microsoft.
batch_convert(to_convert, ['surge', 'clash'], exclusion)
# Stage 4 finished.

# Stage 5: Remove CN domains with Chinese TLDs.
cntld = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/tld-cn"
cntld_regex = "^([a-zA-Z0-9-]*(?:\.\S*)?)( #.*)?$"

cntld_list = []
for line in open(domain_list_base + "tld-cn", mode='r').read().split('\n'):
    istld = re.match(cntld_regex, line)
    if istld and istld[1] != '':
        cntld_list.append('.' + istld[1])
dist_surge = open('./dists/surge/geolocation-cn.txt', mode='r')
dist_clash = open('./dists/clash/geolocation-cn.txt', mode='r')
list_domain_surge = dist_surge.read().splitlines()
list_domain_clash = dist_clash.read().splitlines()
## After loading temporary rules, reopen rule files as write mode.
dist_surge.close()
dist_surge = open('./dists/surge/geolocation-cn.txt', mode='w')
dist_clash.close()
dist_clash = open('./dists/clash/geolocation-cn.txt', mode='w')

for domain in list_domain_surge[:]:
    for tld in cntld_list:
        if domain.find(tld) != -1:
            list_domain_surge.remove(domain)
            break
for domain in list_domain_clash[:]:
    for tld in cntld_list:
        if domain.find(tld) != -1:
            list_domain_clash.remove(domain)
            break

for line in list_domain_surge:
    if line != '':
        dist_surge.writelines(line + '\n')
for line in list_domain_clash:
    if line != '':
        dist_clash.writelines(line + '\n')

dist_surge.close()
dist_clash.close()