import os, re
from abp.filters.parser import parse_filterlist, Filter
from requests import get
from time import time_ns

TARGETS = ['surge', 'clash', 'surge-compatible', 'clash-compatible']
PREFIX_DOMAIN_LIST = './domain-list-community/data/'
PREFIX_CUSTOM_SRC = './Source/'
PREFIX_CUSTOM_ADJUST = './Custom/'
PREFIX_DIST = './dists/'

def geosite_import(src:list, exclusion:str='') -> set:
    regex_import = re.compile(r'^include\:([-\w]{1,})$')
    set_converted = set()
    for line in src:
        flag_import = regex_import.match(line)
        if flag_import and flag_import.group(1) != exclusion:
            src_import = open(PREFIX_DOMAIN_LIST + flag_import.group(1), mode='r').read().splitlines()
            set_converted |= geosite_import(src_import)
            continue
        set_converted.add(line)
    return set_converted

def geosite_convert(src:set) -> set:
    # The following 2 regexes' group 1 matches domains without "@cn" directive.
    regex_fulldomain = re.compile(r'^full\:([-\.a-zA-Z\d]{1,}?(?:\.[-\.a-zA-Z\d]{1,}))(?: @cn){0,1}?$')
    regex_subdomain = re.compile(r'^([-a-zA-Z\d]{1,}(?:\.\S*)?)(?: @cn){0,1}?$')
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
                src_geosite = open(PREFIX_DOMAIN_LIST + target, mode='r').read().splitlines()
                src_geosite_imported = geosite_import(src_geosite, exclusion)
                set_geosite = geosite_convert(src_geosite_imported)
                list_geosite_sorted = [item for item in set_geosite]
                list_geosite_sorted.sort()
                rules_dump(list_geosite_sorted, tool, "./dists/" + tool + "/" + target + ".txt")

def custom_convert(src:str) -> set:
    src_custom = open(src, mode='r').read().splitlines()
    set_converted = set()
    for line in src_custom:
        if line and not line.startswith('#'):
            set_converted.add(line)
    return set_converted

def is_domain_rule(rule:Filter) -> bool:
    regex_ip = re.compile(r'(?:(?:2(?:5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(?:\.(?:(?:2(?:5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}')
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

def rules_dump(src:list, target:str, dst:str) -> None:
    dist = open(dst, mode='w')
    match target:
        case 'surge':
            for domain in src:
                if domain:
                    if domain.startswith('.'):
                        dist.writelines(domain + '\n')
                    elif not domain.startswith('#'):
                        dist.writelines(domain + '\n')
        case 'clash':
            dist.writelines("payload:\n")
            for domain in src:
                if domain:
                    if domain.startswith('.'):
                        dist.writelines("  - '+" + domain + "'\n")
                    elif not domain.startswith('#'):
                        dist.writelines("  - '" + domain + "'\n")
        case 'surge-compatible':
            for domain in src:
                if domain:
                    if domain.startswith('.'):
                        dist.writelines(domain.replace('.', "DOMAIN-SUFFIX,", 1) + '\n')
                    elif not domain.startswith('#'):
                        dist.writelines("DOMAIN," + domain + '\n')
        case 'clash-compatible':
            for domain in src:
                if domain:
                    if domain.startswith('.'):
                        dist.writelines(domain.replace('.', "DOMAIN-SUFFIX,", 1) + ",Policy\n")
                    elif not domain.startswith('#'):
                        dist.writelines("DOMAIN," + domain + ",Policy\n")
        case _:
            raise TypeError("Target type unsupported, only accept 'surge', 'clash', 'surge-compatible' or 'clash-compatible'.")

def rules_batch_dump(src:list, targets:list, dst_prefix:str, filename:str) -> None:
    for target in targets:
        rules_dump(src, target, dst_prefix + target + '/' + filename)

def set_to_sorted_list(src:set) -> list:
    list_sorted = [item for item in src]
    list_sorted.sort()
    return list_sorted

# Stage 1: Sync reject and exclude rules.
print("START Stage 1: Sync reject and exclude rules.")
START_TIME = time_ns()
## AdGuard Base Filter
URL_BASE = 'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt'
## Easylist China
URL_CN = 'https://easylist-downloads.adblockplus.org/easylistchina.txt'
## もちフィルタ
URL_JP = 'https://raw.githubusercontent.com/eEIi0A5L/adblock_filter/master/mochi_filter.txt'
## AdGuard Mobile Filter
URL_MOBILE = 'https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt'
## ADgk
URL_CN_EXTEND = 'https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt'
## AdGuard DNS Filter Whitelist
URL_EXCLUSIONS_1 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt'
URL_EXCLUSIONS_2 = 'https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt'

src_rejections = (
    get(URL_BASE).text +
    get(URL_CN).text +
    get(URL_JP).text +
    get(URL_MOBILE).text +
    get(URL_CN_EXTEND).text
    ).splitlines()
src_exclusions = (get(URL_EXCLUSIONS_1).text + get(URL_EXCLUSIONS_2).text).splitlines()

set_rejections = set()
set_exclusions_raw = set()

for line in parse_filterlist(src_rejections):
    if is_domain_rule(line) and line.action == 'block' and not line.text.endswith('|'):
        if line.text.startswith('.'):
            set_rejections.add(line.text.replace('^', ''))
        else:
            set_rejections.add(line.text.replace("||", '.').replace('^', ''))
    elif is_domain_rule(line) and line.action == 'allow' and not line.text.endswith('|'):
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

path_exclusions_append = PREFIX_CUSTOM_ADJUST + "append-exclude.txt"
for line in custom_convert(path_exclusions_append):
    if (line not in set_exclusions or '.' + line not in set_exclusions):
        set_exclusions.add(line)
    else:
        print(line + " has already been excluded.")

list_rejections_sorted = set_to_sorted_list(set_rejections)
list_exclusions_sorted = set_to_sorted_list(set_exclusions)

rules_batch_dump(list_rejections_sorted, TARGETS, PREFIX_DIST, "reject.txt")
rules_batch_dump(list_exclusions_sorted, TARGETS, PREFIX_DIST, "reject.txt")

END_TIME = time_ns()
print("FINISHED Stage 1\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
# Stage 1 finished.

# Stage 2: Sync v2fly community rules.
print("START Stage 2: Sync v2fly community rules.")
START_TIME = time_ns()

rules_dump(list_cn_sorted, 'surge', './dists/surge/geolocation-cn.txt')
rules_dump(list_cn_sorted, 'clash', './dists/clash/geolocation-cn.txt')
rules_dump(list_cn_sorted, 'surge-compatible', './dists/surge-compatible/geolocation-cn.txt')
rules_dump(list_cn_sorted, 'clash-compatible', './dists/clash-compatible/geolocation-cn.txt')

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
dist_surge_compatible = open('./dists/surge-compatible/geolocation-cn.txt', mode='r')
dist_clash_compatible = open('./dists/clash-compatible/geolocation-cn.txt', mode='r')
list_domain_surge = dist_surge.read().splitlines()
list_domain_clash = dist_clash.read().splitlines()[1:]
list_domain_surge_compatible = dist_surge_compatible.read().splitlines()
list_domain_clash_compatible = dist_clash_compatible.read().splitlines()
## After loading temporary rules, reopen rule files as write mode.
dist_surge.close()
dist_clash.close()
dist_surge_compatible.close()
dist_clash_compatible.close()

list_cntld_sorted = set_to_sorted_list(set_cntld)

rules_batch_dump(list_cntld_sorted, TARGETS, PREFIX_DIST, "geolocation-cn.txt")
rules_dump(list_cntld_sorted, 'surge', './dists/surge/geolocation-cn.txt')
rules_dump(list_cntld_sorted, 'clash', './dists/clash/geolocation-cn.txt')
rules_dump(list_cntld_sorted, 'surge-compatible', './dists/surge-compatible/geolocation-cn.txt')
rules_dump(list_cntld_sorted, 'clash-compatible', './dists/clash-compatible/geolocation-cn.txt')

dist_surge = open('./dists/surge/geolocation-cn.txt', mode='a')
dist_clash = open('./dists/clash/geolocation-cn.txt', mode='a')
dist_surge_compatible = open('./dists/surge-compatible/geolocation-cn.txt', mode='a')
dist_clash_compatible = open('./dists/clash-compatible/geolocation-cn.txt', mode='a')

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
for domain in list_domain_surge_compatible[:]:
    for tld in set_cntld:
        if domain.endswith(tld):
            list_domain_surge_compatible.remove(domain)
            break
for domain in list_domain_clash_compatible[:]:
    for tld in set_cntld:
        if domain.endswith(tld + ",Policy"):
            list_domain_clash_compatible.remove(domain)
            break

for line in list_domain_surge:
    dist_surge.writelines(line + '\n')
for line in list_domain_clash:
    dist_clash.writelines(line + '\n')
for line in list_domain_surge_compatible:
    dist_surge_compatible.writelines(line + '\n')
for line in list_domain_clash_compatible:
    dist_clash_compatible.writelines(line + '\n')

dist_surge.close()
dist_clash.close()
dist_surge_compatible.close()
dist_clash_compatible.close()
END_TIME = time_ns()
print("FINISHED Stage 3\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
## Stage 3 finished.

## Stage 4: Build custom rules.
print("START Stage 4: Build custom rules.")
START_TIME = time_ns()
list_file_custom = os.listdir(PREFIX_CUSTOM_SRC)
for filename in list_file_custom:
    if os.path.isfile(PREFIX_CUSTOM_SRC + filename):
        set_custom = custom_convert(PREFIX_CUSTOM_SRC + filename)
        list_custom_sorted = set_to_sorted_list(set_custom)
        rules_batch_dump(list_custom_sorted, TARGETS, PREFIX_DIST, filename)

list_file_personal = os.listdir(PREFIX_CUSTOM_SRC + "personal/")
for filename in list_file_personal:
    set_personal = custom_convert(PREFIX_CUSTOM_SRC + "personal/" + filename)
    list_personal_sorted = set_to_sorted_list(set_personal)
    rules_batch_dump(list_personal_sorted, TARGETS, PREFIX_DIST, "personal/" + filename)

END_TIME = time_ns()
print("FINISHED Stage 4\nTotal time: " + str(format((END_TIME - START_TIME) / 1000000000, '.3f')) + 's\n')
## Stage 4 finished