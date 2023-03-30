import os, re
from abp.filters import parse_filterlist
from requests import get
from time import time_ns

PREFIX_DOMAIN_LIST = './domain-list-community/data/'
PREFIX_CUSTOM_SRC = './Source/'
PREFIX_CUSTOM_ADJUST = './Custom/'

def import_processor(src, exclusion=None):
    regex_import = re.compile('^include\:(\S*)$')
    list_converted = []
    for line in src:
        flag_import = regex_import.match(line)
        if flag_import and flag_import.group(1) != exclusion:
            file_import = open(PREFIX_DOMAIN_LIST + flag_import.group(1), mode='r').read().splitlines()
            list_converted += import_processor(file_import)
            continue
        list_converted.append(line)
    return list_converted

def convert(src, target):
    # The following 2 regexes' group 1 matches domains without "@cn" directive.
    regex_fulldomain = re.compile('^full\:(\S*)(?: @cn)?$')
    regex_subdomain = re.compile('^([a-zA-Z0-9-]*(?:\.\S*)?)(?: @cn)?$')
    list_converted = []
    for line in src:
        if not line.startswith("regexp:") or line.startswith("keyword:") or line.startswith("#"):
            fulldomain = regex_fulldomain.match(line)
            subdomain = regex_subdomain.match(line)
            if target == 'surge' or target == 'plain':
                if fulldomain:
                    list_converted.append(fulldomain.group(1))
                elif subdomain and subdomain.group(1) != '':
                    list_converted.append('.' + subdomain.group(1))
            elif target == 'clash':
                if fulldomain:
                    list_converted.append("  - '" + fulldomain.group(1) + "'")
                elif subdomain and subdomain.group(1) != '':
                    list_converted.append("  - '+." + subdomain.group(1) + "'")
            else:
                raise TypeError("Target type unsupported, only accept 'surge', 'clash' or 'plain'.")
    if target == 'clash':
        list_converted = list(set(list_converted))
        list_converted.sort()
        list_converted.insert(0, "payload:")
    else:
        list_converted = list(set(list_converted))
        list_converted.sort()
    return list_converted

def batch_convert(targets, tools, exclusions=[]):
    for tool in tools:
        for target in targets:
            for exclusion in exclusions:
                file_orig = open(PREFIX_DOMAIN_LIST + target, mode='r').read().splitlines()
                dist = open("./dists/" + tool + "/" + target + ".txt", mode='w')
                content_orig = import_processor(file_orig, exclusion)
                for line in convert(content_orig, tool):
                    dist.writelines(line + '\n')
                dist.close()

def is_domain_rule(rule):
    if (rule.type == 'filter'
    and rule.selector['type'] == 'url-pattern'
    and rule.text.find('/') == -1
    and rule.text.find('*') == -1
    and rule.text.find('=') == -1
    and rule.text.find('~') == -1
    and rule.text.find('?') == -1
    and rule.text.find('#') == -1
    and rule.text.find(',') == -1
    and not rule.text.find('.') == -1
    and not regex_ip.search(rule.text)
    and not rule.text.startswith('_')
    and not rule.text.startswith('-')
    and not rule.text.startswith('^')
    and not rule.text.startswith('[')
    and not rule.text.endswith('.')
    and not rule.text.endswith('_')
    and not rule.text.endswith(']')
    and not rule.text.endswith(';')
    and not rule.options):
        return True
    else:
        return False

# Stage 1: Sync advertisements blocking and privacy protection rules.
print("START Stage 1: Sync advertisements blocking and privacy protection rules.")
START_TIME = time_ns()
regex_ip = re.compile('((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}') ## IP addresses shouldn't be added.
## AdGuard Base Filter
src_base = 'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt'
## Easylist China
src_cn = 'https://easylist-downloads.adblockplus.org/easylistchina.txt'
## もちフィルタ
src_jp = 'https://raw.githubusercontent.com/eEIi0A5L/adblock_filter/master/mochi_filter.txt'
## AdGuard Mobile Filter
src_mobile = 'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt'
## ADgk
src_cn_extend = 'https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt'
dist_surge = open('./dists/surge/reject.txt', mode='w')
dist_clash = open('./dists/clash/reject.txt', mode='w')
dist_clash.writelines("payload:\n")

content_rejections = (
    get(src_base).text +
    get(src_cn).text +
    get(src_jp).text +
    get(src_mobile).text +
    get(src_cn_extend).text
    ).splitlines()

list_rejections = []
list_exclusions = []

for line in parse_filterlist(content_rejections):
    if is_domain_rule(line) and line.action == 'block' and not line.text.endswith('|'):
        if line.text.startswith('.'):
            list_rejections.append(line.text.replace('^', ''))
        else:
            list_rejections.append(line.text.replace("||", '.').replace('^', ''))
    if is_domain_rule(line) and line.action == 'allow' and not line.text.endswith('|'):
        list_exclusions.append(line.text)

rejections_v2fly = open(PREFIX_DOMAIN_LIST + "category-ads-all", mode='r')
list_rejections += convert(import_processor(rejections_v2fly), "plain")
rejections_custom = open(PREFIX_CUSTOM_ADJUST + "append-reject.txt", mode='r')
list_rejections += rejections_custom.read().splitlines()
list_rejections = list(set(list_rejections))
list_rejections.sort()

for domain in list_rejections:
    dist_surge.writelines(domain + '\n')
    if domain.startswith('.'):
        dist_clash.writelines("  - '+" + domain + "'\n")
    else:
        dist_clash.writelines("  - '" + domain + "'\n")
dist_surge.close()
dist_clash.close()

END_TIME = time_ns()
print("FINISHED Stage 1\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
# Stage 1 finished.

# Stage 2: Sync exclusions with AdGuard.
print("START Stage 2: Sync exclusions with AdGuard.")
START_TIME = time_ns()

src_exclusions_1 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt'
src_exclusions_2 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt'
dist_surge = open('./dists/surge/exclude.txt', mode='w')
dist_clash = open('./dists/clash/exclude.txt', mode='w')
content_exclusions = (get(src_exclusions_1).text + get(src_exclusions_2).text).splitlines() + list_exclusions
list_exclusions = []
for line in parse_filterlist(content_exclusions):
    if is_domain_rule(line):
        domain = line.text.replace('@','').replace('^','').replace('|','')
        if not domain.startswith('-'):
            list_exclusions.append(domain)

rejections_remove = open(PREFIX_CUSTOM_ADJUST + "remove-reject.txt", mode='r')
for line in rejections_remove.read().splitlines():
    try:
        list_exclusions.remove(line)
        list_exclusions.remove('.' + line)
    except ValueError:
        pass

list_exclusions = list(set(list_exclusions))
list_exclusions.sort()

dist_clash.writelines("payload:\n")
for line in list_exclusions:
    dist_surge.writelines("." + line + '\n')
    dist_clash.writelines("  - '+." + line + "'\n")
dist_surge.close()
dist_clash.close()

END_TIME = time_ns()
print("FINISHED Stage 2\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
# Stage 2 finished.

# Stage 3: Sync Bahamut, CN, DMM, Google FCM, Microsoft, niconico, PayPal and YouTube domains with v2fly community.
print("START Stage 3: Sync Bahamut, CN, DMM, Google FCM, Microsoft, niconico, PayPal and YouTube domains with v2fly community.")
START_TIME = time_ns()

target = ['bahamut', 'geolocation-cn', 'dmm', 'googlefcm', 'microsoft', 'niconico', 'paypal', 'youtube']
exclusions = ['github'] ## GitHub's domains are included in "microsoft", but its connectivity mostly isn't as high as Microsoft.
batch_convert(target, ['surge', 'clash'], exclusions)

END_TIME = time_ns()
print("FINISHED Stage 4.\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
# Stage 3 finished.

# Stage 4: Add all CN TLDs to CN rules, then remove CN domains with Chinese TLDs.
print("START Stage 4: Add all CN TLDs to CN rules, then remove CN domains with Chinese TLDs.")
START_TIME = time_ns()
regex_cntld = re.compile('^([a-zA-Z0-9-]*(?:\.\S*)?)( #.*)?$')

list_cntld = []
for line in open(PREFIX_DOMAIN_LIST + "tld-cn", mode='r').read().splitlines():
    istld = regex_cntld.match(line)
    if istld and istld[1] != '':
        list_cntld.append(istld[1])
dist_surge = open('./dists/surge/geolocation-cn.txt', mode='r')
dist_clash = open('./dists/clash/geolocation-cn.txt', mode='r')
list_domain_surge = dist_surge.read().splitlines()
list_domain_clash = dist_clash.read().splitlines()[1:]
## After loading temporary rules, reopen rule files as write mode.
dist_surge.close()
dist_surge = open('./dists/surge/geolocation-cn.txt', mode='w')
dist_clash.close()
dist_clash = open('./dists/clash/geolocation-cn.txt', mode='w')

dist_clash.writelines("payload:\n")

for tld in list_cntld:
    dist_surge.writelines('.' + tld + '\n')
    dist_clash.writelines("  - '+." + tld + "'\n")

for domain in list_domain_surge[:]:
    for tld in list_cntld:
        if domain.endswith(tld):
            list_domain_surge.remove(domain)
            break
for domain in list_domain_clash[:]:
    for tld in list_cntld:
        if domain.endswith(tld + "'"):
            list_domain_clash.remove(domain)
            break

for line in list_domain_surge:
    dist_surge.writelines(line + '\n')
for line in list_domain_clash:
    dist_clash.writelines(line + '\n')

dist_surge.close()
dist_clash.close()
END_TIME = time_ns()
print("FINISHED Stage 4\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
## Stage 4 finished.

## Stage 5: Build custom rules.
print("START Stage 5: Build custom rules.")
START_TIME = time_ns()
list_custom = os.listdir(PREFIX_CUSTOM_SRC)
for filename in list_custom:
    if os.path.isfile(PREFIX_CUSTOM_SRC + filename):
        file_custom = open(PREFIX_CUSTOM_SRC + filename, mode='r')
        content_custom = file_custom.read().splitlines()
        content_custom.sort()
        dist_surge = open('./dists/surge/' + filename, mode='w')
        dist_clash = open('./dists/clash/' + filename, mode='w')
        dist_clash.writelines("payload:\n")
        for line in content_custom:
            if line and not line.startswith('#'):
                dist_surge.writelines(line + '\n')
                if line.startswith('.'):
                    dist_clash.writelines("  - '+" + line + "'\n")
                else:
                    dist_clash.writelines("  - '" + line + "'\n")
        file_custom.close()
        dist_surge.close()
        dist_clash.close()

list_personal = os.listdir(PREFIX_CUSTOM_SRC + "personal/")
for filename in list_personal:
    file_custom = open(PREFIX_CUSTOM_SRC + "personal/" + filename, mode='r')
    content_custom = file_custom.read().splitlines()
    content_custom.sort()
    dist_surge = open('./dists/surge/personal/' + filename, mode='w')
    dist_clash = open('./dists/clash/personal/' + filename, mode='w')
    dist_clash.writelines("payload:\n")
    for line in content_custom:
        if line and not line.startswith('#'):
            dist_surge.writelines(line + '\n')
            if line.startswith('.'):
                dist_clash.writelines("  - '+" + line + "'\n")
            else:
                dist_clash.writelines("  - '" + line + "'\n")
    file_custom.close()
    dist_surge.close()
    dist_clash.close()

END_TIME = time_ns()
print("FINISHED Stage 5\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
## Stage 5 finished