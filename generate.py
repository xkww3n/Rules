import os, re
from abp.filters.parser import parse_filterlist, Filter
from requests import get
from time import time_ns

PREFIX_DOMAIN_LIST = './domain-list-community/data/'
PREFIX_CUSTOM_SRC = './Source/'
PREFIX_CUSTOM_ADJUST = './Custom/'

def geosite_import(src:list, exclusion:str='') -> set:
    regex_import = re.compile(r'^include\:([-\w]{1,})$')
    set_converted = set()
    for line in src:
        flag_import = regex_import.match(line)
        if flag_import and flag_import.group(1) != exclusion:
            file_import = open(PREFIX_DOMAIN_LIST + flag_import.group(1), mode='r').read().splitlines()
            set_converted |= geosite_import(file_import)
            continue
        set_converted.add(line)
    return set_converted

def geosite_convert(src:set) -> set:
    # The following 2 regexes' group 1 matches domains without "@cn" directive.
    regex_fulldomain = re.compile(r'^full\:([-\.a-zA-Z\d]{1,}?(?:\.[-\.a-zA-Z\d]{1,}))(?: @cn){0,1}?$')
    regex_subdomain = re.compile(r'^([-\.a-zA-Z\d]{1,}?(?:\.[-\.a-zA-Z\d]{1,}))(?: @cn){0,1}?$')
    set_converted = set()
    for line in src:
        if not line.startswith("regexp:") or line.startswith("keyword:") or line.startswith("#"):
            fulldomain = regex_fulldomain.match(line)
            subdomain = regex_subdomain.match(line)
            if fulldomain:
                set_converted.add(fulldomain.group(1))
            elif subdomain:
                set_converted.add('.' + subdomain.group(1))
    return set_converted

def geosite_batch_convert(targets:list, tools:list, exclusions:list=[]) -> None:
    for tool in tools:
        for target in targets:
            for exclusion in exclusions:
                file_orig = open(PREFIX_DOMAIN_LIST + target, mode='r').read().splitlines()
                content_orig = geosite_import(file_orig, exclusion)
                set_geosite = geosite_convert(content_orig)
                list_geosite_sorted = [item for item in set_geosite]
                list_geosite_sorted.sort()
                dump_rules(list_geosite_sorted, tool, "./dists/" + tool + "/" + target + ".txt")

def custom_convert(src:str) -> set:
    content_custom = open(src, mode='r').read().splitlines()
    set_converted = set()
    for line in content_custom:
        if not line.startswith('#'):
            set_converted.add(line)
    return set_converted

def is_domain_rule(rule:Filter) -> bool:
    regex_ip = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$')
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

def dump_rules(src:list, target:str, dst:str) -> None:
    dist = open(dst, mode='w')
    if target not in ['surge', 'clash']:
        raise TypeError("Target type unsupported, only accept 'surge' or 'clash'.")
    if target == 'clash':
        dist.writelines("payload:\n")
    for domain in src:
        if domain:
            if domain.startswith('.'):
                if target == 'surge':
                    dist.writelines(domain + '\n')
                if target == 'clash':
                    dist.writelines("  - '+" + domain + "'\n")
            elif not domain.startswith('#'):
                if target == 'surge':
                    dist.writelines(domain + '\n')
                if target == 'clash':
                    dist.writelines("  - '" + domain + "'\n")

# Stage 1: Sync reject and exclude rules.
print("START Stage 1: Sync reject and exclude rules.")
START_TIME = time_ns()
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
## AdGuard DNS Filter Whitelist
src_exclusions_1 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt'
src_exclusions_2 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt'

src_rejections = (
    get(src_base).text +
    get(src_cn).text +
    get(src_jp).text +
    get(src_mobile).text +
    get(src_cn_extend).text
    ).splitlines()
src_exclusions = (get(src_exclusions_1).text + get(src_exclusions_2).text).splitlines()

set_rejections = set()
set_exclusions_raw = set()

for line in parse_filterlist(src_rejections):
    if is_domain_rule(line) and line.action == 'block' and not line.text.endswith('|'):
        if line.text.startswith('.'):
            set_rejections.add(line.text.replace('^', ''))
        else:
            set_rejections.add(line.text.replace("||", '.').replace('^', ''))
    if is_domain_rule(line) and line.action == 'allow' and not line.text.endswith('|'):
        src_exclusions.append(line.text)

for line in parse_filterlist(src_exclusions):
    if is_domain_rule(line):
        domain = line.text.replace('@','').replace('^','').replace('|','')
        if not domain.startswith('-'):
            set_exclusions_raw.add(domain)

list_rejections_v2fly = open(PREFIX_DOMAIN_LIST + "category-ads-all", mode='r').read().splitlines()
set_rejections |= geosite_convert(geosite_import(list_rejections_v2fly))
set_rejections |= custom_convert(PREFIX_CUSTOM_ADJUST + "append-reject.txt")
set_exclusions = set()

for domain_exclude in set_exclusions_raw.copy():
    for domain_reject in set_rejections.copy():
        if domain_reject == domain_exclude or domain_reject == '.' + domain_exclude:
            set_rejections.remove(domain_reject)
            set_exclusions_raw.remove(domain_exclude)

for domain_exclude in set_exclusions_raw:
    for domain_reject in set_rejections:
        if domain_exclude.endswith(domain_reject):
            set_exclusions.add(domain_exclude)

exclusions_append = PREFIX_CUSTOM_ADJUST + "append-exclude.txt"
for line in custom_convert(exclusions_append):
    if (line not in set_exclusions or '.' + line not in set_exclusions):
        set_exclusions.add(line)
    else:
        print(line + " has already been excluded.")

list_rejections_sorted = [item for item in set_rejections]
list_rejections_sorted.sort()
list_exclusions_sorted = [item for item in set_exclusions]
list_exclusions_sorted.sort()

dump_rules(list_rejections_sorted, 'surge', './dists/surge/reject.txt')
dump_rules(list_rejections_sorted, 'clash', './dists/clash/reject.txt')

dump_rules(list_exclusions_sorted, 'surge', './dists/surge/exclude.txt')
dump_rules(list_exclusions_sorted, 'clash', './dists/clash/exclude.txt')

END_TIME = time_ns()
print("FINISHED Stage 1\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
# Stage 1 finished.

# Stage 2: Sync v2fly community rules.
print("START Stage 2: Sync v2fly community rules.")
START_TIME = time_ns()

target = ['bahamut', 'geolocation-cn', 'dmm', 'googlefcm', 'microsoft', 'niconico', 'openai', 'paypal', 'youtube']
exclusions = ['github'] ## GitHub's domains are included in "microsoft", but its connectivity mostly isn't as high as Microsoft.
geosite_batch_convert(target, ['surge', 'clash'], exclusions)

END_TIME = time_ns()
print("FINISHED Stage 2.\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
# Stage 2 finished.

# Stage 3: Add all CN TLDs to CN rules, then remove CN domains with Chinese TLDs.
print("START Stage 3: Add all CN TLDs to CN rules, then remove CN domains with Chinese TLDs.")
START_TIME = time_ns()
regex_cntld = re.compile(r'^([-\.a-zA-Z\d]{1,}(?:\.\w{1,})?)( #.*){0,1}$')

set_cntld = set()
for line in open(PREFIX_DOMAIN_LIST + "tld-cn", mode='r').read().splitlines():
    istld = regex_cntld.match(line)
    if istld:
        set_cntld.add('.' + istld[1])
dist_surge = open('./dists/surge/geolocation-cn.txt', mode='r')
dist_clash = open('./dists/clash/geolocation-cn.txt', mode='r')
list_domain_surge = dist_surge.read().splitlines()
list_domain_clash = dist_clash.read().splitlines()[1:]
## After loading temporary rules, reopen rule files as write mode.
dist_surge.close()
dist_clash.close()

list_cntld_sorted = [item for item in set_cntld]
list_cntld_sorted.sort()

dump_rules(list_cntld_sorted, 'surge', './dists/surge/geolocation-cn.txt')
dump_rules(list_cntld_sorted, 'clash', './dists/clash/geolocation-cn.txt')

dist_surge = open('./dists/surge/geolocation-cn.txt', mode='a')
dist_clash = open('./dists/clash/geolocation-cn.txt', mode='a')

for domain in list_domain_surge[:]:
    for tld in set_cntld:
        if domain.endswith(tld):
            list_domain_surge.remove(domain)
            break
for domain in list_domain_clash[:]:
    for tld in set_cntld:
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
print("FINISHED Stage 3\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
## Stage 3 finished.

## Stage 4: Build custom rules.
print("START Stage 4: Build custom rules.")
START_TIME = time_ns()
list_custom = os.listdir(PREFIX_CUSTOM_SRC)
for filename in list_custom:
    if os.path.isfile(PREFIX_CUSTOM_SRC + filename):
        content_custom = custom_convert(PREFIX_CUSTOM_SRC + filename)
        list_custom_sorted = [item for item in content_custom]
        list_custom_sorted.sort()
        dump_rules(list_custom_sorted, 'surge', './dists/surge/' + filename)
        dump_rules(list_custom_sorted, 'clash', './dists/clash/' + filename)

list_personal = os.listdir(PREFIX_CUSTOM_SRC + "personal/")
for filename in list_personal:
    content_personal = custom_convert(PREFIX_CUSTOM_SRC + "personal/" + filename)
    list_personal_sorted = [item for item in content_personal]
    list_personal_sorted.sort()
    dump_rules(list_personal_sorted, 'surge', './dists/surge/personal/' + filename)
    dump_rules(list_personal_sorted, 'clash', './dists/clash/personal/' + filename)

END_TIME = time_ns()
print("FINISHED Stage 4\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
## Stage 4 finished