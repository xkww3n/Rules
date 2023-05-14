import logging
import logging.config
import re
from pathlib import Path
from time import time_ns

from abp.filters.parser import Filter, parse_filterlist
from requests import Session

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("root")

TARGETS = ["surge", "clash", "surge-compatible", "clash-compatible"]
PATH_DOMAIN_LIST = Path("./domain-list-community/data/")
PATH_CUSTOM_BUILD = Path("./Source/")
PATH_CUSTOM_APPEND = Path("./Custom/Append/")
PATH_CUSTOM_REMOVE = Path("./Custom/Remove/")
PATH_DIST = Path("./dists/")


def geosite_import(src: list, exclusions: list = []) -> set:
    set_converted = set()
    for line in src:
        if line.startswith("include:"):
            name_import = line.split("include:")[1]
            if "#" in name_import:
                name_import = name_import.split(" #")[0]
                if name_import not in exclusions:
                    src_import = open(PATH_DOMAIN_LIST/name_import, mode="r").read().splitlines()
                    set_converted |= geosite_import(src_import)
            else:
                if name_import not in exclusions:
                    src_import = open(PATH_DOMAIN_LIST/name_import, mode="r").read().splitlines()
                    set_converted |= geosite_import(src_import)
            continue
        set_converted.add(line)
    return set_converted


def geosite_convert(src: set) -> set:
    # The following 2 regexes' group 1 matches domains without "@cn" directive.
    REGEX_FULLDOMAIN = re.compile(r"^full\:([-\.a-zA-Z\d]{1,}?(?:\.[-\.a-zA-Z\d]{1,}))(?: @cn){0,1}?$")
    REGEX_SUBDOMAIN = re.compile(r"^([-a-zA-Z\d]{1,}(?:\.\S*)?)(?: @cn){0,1}?$")
    set_converted = set()
    for line in src:
        if not line.startswith("regexp:") or line.startswith("keyword:") or line.startswith("#"):
            fulldomain = REGEX_FULLDOMAIN.match(line)
            subdomain = REGEX_SUBDOMAIN.match(line)
            if fulldomain:
                set_converted.add(fulldomain.group(1))
            elif subdomain:
                set_converted.add("." + subdomain.group(1))
    return set_converted


def geosite_batch_convert(categories: list, tools: list, exclusions: list = []) -> None:
    for tool in tools:
        for category in categories:
            src_geosite = open(PATH_DOMAIN_LIST/category, mode="r").read().splitlines()
            src_geosite_imported = geosite_import(src_geosite, exclusions)
            set_geosite = geosite_convert(src_geosite_imported)
            list_geosite_sorted = set_to_sorted_list(set_geosite)
            rules_dump(list_geosite_sorted, tool, PATH_DIST/tool/(category + ".txt"))


def custom_convert(src: Path) -> set:
    src_custom = open(src, mode="r").read().splitlines()
    set_converted = set()
    for line in src_custom:
        if line and not line.startswith("#"):
            set_converted.add(line)
    return set_converted


def is_ipaddr(str: str) -> bool:
    if str.count(".") != 3:
        return False
    for part in str.split("."):
        if not part.isdigit():
            return False
        i = int(part)
        if i < 0 or i > 255:
            return False
    return True


def is_domain_rule(rule: Filter) -> bool:
    if (
        rule.type == "filter"
        and rule.selector["type"] == "url-pattern"
        and "." in rule.text
        and "/" not in rule.text
        and "*" not in rule.text
        and "=" not in rule.text
        and "~" not in rule.text
        and "?" not in rule.text
        and "#" not in rule.text
        and "," not in rule.text
        and ":" not in rule.text
        and not rule.text.startswith("_")
        and not rule.text.startswith("-")
        and not rule.text.startswith("^")
        and not rule.text.startswith("[")
        and not rule.text.endswith(".")
        and not rule.text.endswith("_")
        and not rule.text.endswith("]")
        and not rule.text.endswith(";")
        and not rule.options
        and not is_ipaddr(rule.text.replace("||", "").replace("^", ""))
    ):
        return True
    else:
        return False


def rules_dump(src: list, target: str, dst: Path) -> None:
    try:
        dist = open(dst, mode="w")
    except FileNotFoundError:
        dst.parent.mkdir(parents=True)
        dist = open(dst, mode="w")
    match target:
        case "surge":
            for domain in src:
                if domain:
                    if domain.startswith("."):
                        dist.writelines(domain + "\n")
                    elif not domain.startswith("#"):
                        dist.writelines(domain + "\n")
        case "clash":
            dist.writelines("payload:\n")
            for domain in src:
                if domain:
                    if domain.startswith("."):
                        dist.writelines("  - '+" + domain + "'\n")
                    elif not domain.startswith("#"):
                        dist.writelines("  - '" + domain + "'\n")
        case "surge-compatible":
            for domain in src:
                if domain:
                    if domain.startswith("."):
                        dist.writelines(domain.replace(".", "DOMAIN-SUFFIX,", 1) + "\n")
                    elif not domain.startswith("#"):
                        dist.writelines("DOMAIN," + domain + "\n")
        case "clash-compatible":
            for domain in src:
                if domain:
                    if domain.startswith("."):
                        dist.writelines(domain.replace(".", "DOMAIN-SUFFIX,", 1) + ",Policy\n")
                    elif not domain.startswith("#"):
                        dist.writelines("DOMAIN," + domain + ",Policy\n")
        case _:
            raise TypeError(
                "Target type unsupported, only accept 'surge', 'clash', 'surge-compatible' or 'clash-compatible'."
            )


def rules_batch_dump(src: list, targets: list, dst_path: Path, filename: str) -> None:
    for target in targets:
        rules_dump(src, target, dst_path/target/filename)


def set_to_sorted_list(src: set) -> list:
    list_sorted = [item for item in src]
    list_sorted.sort()
    return list_sorted


# Stage 1: Sync reject and exclude rules.
logger.info("START Stage 1: Sync reject and exclude rules.")
START_TIME = time_ns()
connection = Session()
## AdGuard Base Filter
URL_BASE = "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt"
## Easylist China
URL_CN = "https://easylist-downloads.adblockplus.org/easylistchina.txt"
## もちフィルタ
URL_JP = "https://raw.githubusercontent.com/eEIi0A5L/adblock_filter/master/mochi_filter.txt"
## AdGuard Mobile Filter
URL_MOBILE = "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt"
## ADgk
URL_CN_EXTEND = "https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt"
## AdGuard DNS Filter Whitelist
URL_EXCLUSIONS_1 = "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt"
URL_EXCLUSIONS_2 = "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt"

src_rejections = (
    connection.get(URL_BASE).text
    + connection.get(URL_CN).text
    + connection.get(URL_JP).text
    + connection.get(URL_MOBILE).text
    + connection.get(URL_CN_EXTEND).text
).splitlines()
logger.debug(f"Imported {format(str(len(src_rejections)))} lines of reject rules.")

src_exclusions = (connection.get(URL_EXCLUSIONS_1).text + connection.get(URL_EXCLUSIONS_2).text).splitlines()
logger.debug(f"Imported {format(str(len(src_exclusions)))} lines of exclude rules.")

set_rejections = set()
set_exclusions_raw = set()

for line in parse_filterlist(src_rejections):
    if is_domain_rule(line) and line.action == "block" and not line.text.endswith("|"):
        if line.text.startswith("."):
            set_rejections.add(line.text.replace("^", ""))
            logger.debug(f'Line "{line.text}" is added to reject set, converted to "{line.text.replace("^", "")}".')
        else:
            set_rejections.add(line.text.replace("||", ".").replace("^", ""))
            logger.debug(
                f'Line "{line.text}" is added to reject set, converted to "{line.text.replace("||", ".").replace("^", "")}".'
            )
    elif is_domain_rule(line) and line.action == "allow" and not line.text.endswith("|"):
        src_exclusions.append(line.text)
        logger.debug(f'Line "{line.text}" is added to exclude set.')

for line in parse_filterlist(src_exclusions):
    if is_domain_rule(line):
        domain = line.text.replace("@", "").replace("^", "").replace("|", "")
        if not domain.startswith("-"):
            set_exclusions_raw.add(domain)
            logger.debug(f'Line "{line.text}" is added to raw exclude set, converted to "{domain}".')

list_rejections_v2fly = open(PATH_DOMAIN_LIST/"category-ads-all", mode="r").read().splitlines()
set_rejections |= geosite_convert(geosite_import(list_rejections_v2fly))
logger.debug(
    f"Imported {str(len(geosite_convert(geosite_import(list_rejections_v2fly))))} reject rules from v2fly category-ads-all list."
)
set_rejections |= custom_convert(PATH_CUSTOM_APPEND/"reject.txt")
logger.debug(
    f'Imported {str(len(custom_convert(PATH_CUSTOM_APPEND/"reject.txt")))} reject rules from "Custom/Append/reject.txt".'
)
set_exclusions_raw |= custom_convert(PATH_CUSTOM_REMOVE/"reject.txt")
logger.debug(
    f'Imported {str(len(custom_convert(PATH_CUSTOM_REMOVE/"reject.txt")))} exclude rules from "Custom/Remove/reject.txt".'
)
set_exclusions_raw |= custom_convert(PATH_CUSTOM_APPEND/"exclude.txt")
logger.debug(
    f'Imported {str(len(custom_convert(PATH_CUSTOM_APPEND/"exclude.txt")))} exclude rules from "Custom/Append/exclude.txt".'
)

set_exclusions = set()
logger.debug("Start deduplicating reject and exclude set.")
for domain_exclude in set_exclusions_raw.copy():
    for domain_reject in set_rejections.copy():
        if domain_reject == domain_exclude or domain_reject == "." + domain_exclude:
            set_rejections.remove(domain_reject)
            set_exclusions_raw.remove(domain_exclude)
            logger.debug(f"{domain_reject} is removed as duplicate with {domain_exclude}.")

for domain_exclude in set_exclusions_raw:
    for domain_reject in set_rejections:
        if domain_exclude.endswith(domain_reject):
            set_exclusions.add(domain_exclude)
            logger.debug(f"{domain_exclude} is added to final exclude set.")


list_rejections_sorted = set_to_sorted_list(set_rejections)
list_exclusions_sorted = set_to_sorted_list(set_exclusions)

rules_batch_dump(list_rejections_sorted, TARGETS, PATH_DIST, "reject.txt")
rules_batch_dump(list_exclusions_sorted, TARGETS, PATH_DIST, "exclude.txt")

END_TIME = time_ns()
logger.info(f"FINISHED Stage 1. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")
# Stage 1 finished.

# Stage 2: Sync domestic rules.
logger.info("START Stage 2: Sync domestic rules.")
START_TIME = time_ns()

src_domestic_raw = geosite_import(open(PATH_DOMAIN_LIST/"geolocation-cn", mode="r").read().splitlines())
logger.debug(f"Imported {str(len(src_domestic_raw))} domestic rules from v2fly geolocation-cn list.")
set_domestic_raw = geosite_convert(src_domestic_raw)
set_domestic_raw |= custom_convert(PATH_CUSTOM_APPEND/"domestic.txt")
logger.debug(
    f'Imported {str(len(custom_convert(PATH_CUSTOM_APPEND/"domestic.txt")))} domestic rules from "Custom/Append/domestic.txt".'
)

## Add all domestic TLDs to domestic rules, then remove domestic domains with domestic TLDs.
set_domestic_tld = set()
for line in open(PATH_DOMAIN_LIST/"tld-cn", mode="r").read().splitlines():
    if line and not line.startswith("#"):
        if "#" in line:
            set_domestic_tld.add("." + line.split(" #")[0])
            logger.debug(f'TLD "{"." + line.split(" #")[0]}" is added to domestic set.')
        else:
            set_domestic_tld.add("." + line)
            logger.debug(f'TLD "{"." + line}" is added to domestic set.')
logger.debug(f"Imported {str(len(set_domestic_tld))} domestic TLDs.")
for domain in set_domestic_raw.copy():
    for tld in set_domestic_tld:
        if domain.endswith(tld):
            set_domestic_raw.remove(domain)
            logger.debug(f'"{domain}"" is removed for having a domestic TLD "{tld}"".')
            break
set_domestic_raw |= set_domestic_tld

list_domestic_sorted = set_to_sorted_list(set_domestic_raw)
rules_batch_dump(list_domestic_sorted, TARGETS, PATH_DIST, "domestic.txt")

END_TIME = time_ns()
logger.info(f"FINISHED Stage 2. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")
# Stage 2 finished.

# Stage 3: Sync v2fly community rules.
logger.info("START Stage 3: Sync v2fly community rules.")
START_TIME = time_ns()

CATEGORIES = [
    "bahamut",
    "bing",
    "dmm",
    "googlefcm",
    "microsoft",
    "niconico",
    "openai",
    "paypal",
    "youtube",
]
EXCLUSIONS = [
    "github",  ## GitHub's domains are included in "microsoft", but its connectivity mostly isn't as high as Microsoft.
    "bing",  ## Bing has a more restricted ver for Mainland China.
]
geosite_batch_convert(CATEGORIES, TARGETS, EXCLUSIONS)

END_TIME = time_ns()
logger.info(f"FINISHED Stage 3. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")
# Stage 3 finished.

# Stage 4: Build custom rules.
logger.info("START Stage 4: Build custom rules.")
START_TIME = time_ns()
list_file_custom = Path.iterdir(PATH_CUSTOM_BUILD)
for filename in list_file_custom:
    if filename.is_file():
        logger.debug(f'Start converting "{filename.name}".')
        set_custom = custom_convert(filename)
        list_custom_sorted = set_to_sorted_list(set_custom)
        rules_batch_dump(list_custom_sorted, TARGETS, PATH_DIST, filename.name)
        logger.debug(f"Converted {str(len(list_custom_sorted))} rules.")

list_file_personal = Path.iterdir(PATH_CUSTOM_BUILD/"personal")
for filename in list_file_personal:
    logger.debug(f'Start converting "{filename.name}".')
    set_personal = custom_convert(filename)
    list_personal_sorted = set_to_sorted_list(set_personal)
    rules_batch_dump(list_personal_sorted, TARGETS, PATH_DIST, "personal/" + filename.name)
    logger.debug(f"Converted {str(len(list_personal_sorted))} rules.")

END_TIME = time_ns()
logger.info(f"FINISHED Stage 4. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")
# Stage 4 finished
