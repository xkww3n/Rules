import re
from abp.filters import parse_filterlist
from os import listdir
from requests import get
from time import time_ns

PREFIX_DOMAIN_LIST = './domain-list-community/data/'
PREFIX_CUSTOM_BUILD = './custom/build/'
PREFIX_CUSTOM_EXTRA = './custom/extra/'

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
dist_surge = open('./dists/surge/protection.txt', mode='w')
dist_clash = open('./dists/clash/protection.txt', mode='w')
dist_clash.writelines("payload:\n")

content_block = (
    get(src_base).text +
    get(src_cn).text +
    get(src_jp).text +
    get(src_mobile).text +
    get(src_cn_extend).text
    ).splitlines()

list_block = []
list_exceptions = []

for line in parse_filterlist(content_block):
    if (line.type == 'filter'
    and line.action == 'block'
    and line.selector['type'] == 'url-pattern'
    and line.text.find('/') == -1
    and line.text.find('*') == -1
    and line.text.find('=') == -1
    and line.text.find('~') == -1
    and line.text.find('?') == -1
    and line.text.find('#') == -1
    and line.text.find(',') == -1
    and not line.text.find('.') == -1
    and not regex_ip.search(line.text)
    and not line.text.startswith('_')
    and not line.text.startswith('-')
    and not line.text.startswith('^')
    and not line.text.startswith('[')
    and not line.text.endswith('.')
    and not line.text.endswith('_')
    and not line.text.endswith('|')
    and not line.text.endswith(']')
    and not line.text.endswith(';')
    and not line.options):
        if line.text.startswith('.'):
            list_block.append(line.text.replace('^', ''))
        else:
            list_block.append(line.text.replace("||", '.').replace('^', ''))
    if (line.type == 'filter'
    and line.action == 'allow'
    and line.selector['type'] == 'url-pattern'
    and line.text.find('/') == -1
    and line.text.find('*') == -1
    and line.text.find('=') == -1
    and line.text.find('~') == -1
    and line.text.find('?') == -1
    and line.text.find('#') == -1
    and line.text.find(',') == -1
    and not line.text.find('.') == -1
    and not re.search(regex_ip, line.text)
    and not line.text.startswith('_')
    and not line.text.startswith('-')
    and not line.text.startswith('^')
    and not line.text.startswith('[')
    and not line.text.endswith('.')
    and not line.text.endswith('_')
    and not line.text.endswith('|')
    and not line.text.endswith(']')
    and not line.text.endswith(';')
    and not line.options):
        list_exceptions.append(line.text)

block_v2fly = open(PREFIX_DOMAIN_LIST + "category-ads-all", mode='r')
list_block += convert(import_processor(block_v2fly), "plain")
block_local = open(PREFIX_CUSTOM_EXTRA + "reject.txt", mode='r')
list_block += list(block_local)
list_block = list(set(list_block))
list_block.sort()

for domain in list_block:
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

# Stage 2: Sync exceptions with AdGuard.
print("START Stage 2: Sync exceptions with AdGuard.")
START_TIME = time_ns()
src_exceptions_1 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt'
src_exceptions_2 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt'
dist_surge = open('./dists/surge/exceptions.txt', mode='w')
dist_clash = open('./dists/clash/exceptions.txt', mode='w')
content_exceptions = (get(src_exceptions_1).text + get(src_exceptions_2).text).splitlines() + list_exceptions
list_exceptions = []
for line in parse_filterlist(content_exceptions):
    if (line.type == 'filter'
    and line.selector['type'] == 'url-pattern'
    and line.text.find('/') == -1
    and line.text.find('*') == -1
    and line.text.find('=') == -1
    and line.text.find('~') == -1
    and line.text.find('?') == -1
    and line.text.find('#') == -1
    and line.text.find(',') == -1
    and not line.text.find('.') == -1
    and not re.search(regex_ip, line.text)
    and not line.text.startswith('_')
    and not line.text.startswith('-')
    and not line.text.startswith('^')
    and not line.text.startswith('[')
    and not line.text.endswith('.')
    and not line.text.endswith('_')
    and not line.text.endswith(']')
    and not line.text.endswith(';')
    and not line.options):
        domain = line.text.replace('@','').replace('^','').replace('|','')
        if not domain.startswith('-'):
            list_exceptions.append(domain)

list_exceptions = list(set(list_exceptions))
list_exceptions.sort()

dist_clash.writelines("payload:\n")

for line in list_exceptions:
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
to_convert = ['bahamut', 'geolocation-cn', 'dmm', 'googlefcm', 'microsoft', 'niconico', 'paypal', 'youtube']
exclusion = ['github'] ## GitHub's domains are included in "microsoft", but its connectivity mostly isn't as high as Microsoft.
batch_convert(to_convert, ['surge', 'clash'], exclusion)
END_TIME = time_ns()
print("FINISHED Stage 4.\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
# Stage 3 finished.

## Stage 4: Build custom rules.
print("START Stage 4: Build custom rules.")
START_TIME = time_ns()
list_custom = listdir(PREFIX_CUSTOM_BUILD)
for filename in list_custom:
    file_custom = open(PREFIX_CUSTOM_BUILD + filename, mode='r')
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
END_TIME = time_ns()
print("FINISHED Stage 4\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
## Stage 4 finished