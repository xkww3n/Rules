import logging
import logging.config
from pathlib import Path
from shutil import copytree
from time import time_ns

from abp.filters.parser import parse_filterlist
from requests import Session

from Utils import const, geosite, rule

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("root")


# Stage 1: Sync reject and exclude rules.
logger.info("START Stage 1: Sync reject and exclude rules.")
START_TIME = time_ns()
connection = Session()

src_rejections = []
for url in const.LIST_REJECT_URL:
    src_rejections += (connection.get(url).text.splitlines())

logger.debug(f"Imported {str(len(src_rejections))} lines of reject rules.")

src_exclusions = []
for url in const.LIST_EXCL_URL:
    src_exclusions += connection.get(url).text.splitlines()

logger.debug(f"Imported {str(len(src_exclusions))} lines of exclude rules.")

set_rejections = set()
set_exclusions_raw = set()

for line in parse_filterlist(src_rejections):
    if rule.is_domain(line) and line.action == "block" and not line.text.endswith("|"):
        if line.text.startswith("."):
            set_rejections.add(line.text.strip("^"))
            logger.debug(f'Line "{line.text}" is added to reject set, converted to "{line.text.strip("^")}".')
        else:
            set_rejections.add(line.text.replace("||", ".").strip("^"))
            logger.debug(
                f'Line "{line.text}" is added to reject set, converted to "{line.text.replace("||", ".").strip("^")}".'
            )
    elif rule.is_domain(line) and line.action == "allow" and not line.text.endswith("|"):
        src_exclusions.append(line.text)
        logger.debug(f'Line "{line.text}" is added to exclude set.')

for line in parse_filterlist(src_exclusions):
    if rule.is_domain(line):
        domain = line.text.strip("@").strip("^").strip("|")
        if not domain.startswith("-"):
            set_exclusions_raw.add(domain)
            logger.debug(f'Line "{line.text}" is added to raw exclude set, converted to "{domain}".')

src_rejections_v2fly = set(open(const.PATH_DOMAIN_LIST/"category-ads-all", mode="r").read().splitlines())
set_rejections_v2fly = geosite.convert(geosite.parse(src_rejections_v2fly))
set_rejections |= set_rejections_v2fly
logger.debug(f"Imported {str(len(set_rejections_v2fly))} reject rules from v2fly category-ads-all list.")
set_rejections |= rule.custom_convert(const.PATH_CUSTOM_APPEND/"reject.txt")
logger.debug(
    f'Imported {str(len(rule.custom_convert(const.PATH_CUSTOM_APPEND/"reject.txt")))} reject rules from "Custom/Append/reject.txt".'
)
set_exclusions_raw |= rule.custom_convert(const.PATH_CUSTOM_REMOVE/"reject.txt")
logger.debug(
    f'Imported {str(len(rule.custom_convert(const.PATH_CUSTOM_REMOVE/"reject.txt")))} exclude rules from "Custom/Remove/reject.txt".'
)
set_exclusions_raw |= rule.custom_convert(const.PATH_CUSTOM_APPEND/"exclude.txt")
logger.debug(
    f'Imported {str(len(rule.custom_convert(const.PATH_CUSTOM_APPEND/"exclude.txt")))} exclude rules from "Custom/Append/exclude.txt".'
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


list_rejections_sorted = rule.set_to_sorted_list(set_rejections)
list_exclusions_sorted = rule.set_to_sorted_list(set_exclusions)

rule.batch_dump(list_rejections_sorted, const.TARGETS, const.PATH_DIST, "reject.txt")
rule.batch_dump(list_exclusions_sorted, const.TARGETS, const.PATH_DIST, "exclude.txt")

END_TIME = time_ns()
logger.info(f"FINISHED Stage 1. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")
# Stage 1 finished.

# Stage 2: Sync domestic rules.
logger.info("START Stage 2: Sync domestic rules.")
START_TIME = time_ns()

src_domestic_raw = set(open(const.PATH_DOMAIN_LIST/"geolocation-cn", mode="r").read().splitlines())
logger.debug(f"Imported {str(len(src_domestic_raw))} domestic rules from v2fly geolocation-cn list.")
set_domestic_raw = geosite.convert(geosite.parse(src_domestic_raw), ["!cn"])
set_domestic_raw |= rule.custom_convert(const.PATH_CUSTOM_APPEND/"domestic.txt")
logger.debug(
    f'Imported {str(len(rule.custom_convert(const.PATH_CUSTOM_APPEND/"domestic.txt")))} domestic rules from "Custom/Append/domestic.txt".'
)

## Add all domestic TLDs to domestic rules, then remove domestic domains with domestic TLDs.
src_domestic_tlds = set(open(const.PATH_DOMAIN_LIST/"tld-cn", mode="r").read().splitlines())
set_domestic_tlds = geosite.convert(geosite.parse(src_domestic_tlds))
logger.debug(f"Imported {str(len(set_domestic_tlds))} domestic TLDs.")
for domain in set_domestic_raw.copy():
    for tld in set_domestic_tlds:
        if domain.endswith(tld):
            set_domestic_raw.remove(domain)
            logger.debug(f'"{domain}"" is removed for having a domestic TLD "{tld}"".')
            break
set_domestic_raw |= set_domestic_tlds

list_domestic_sorted = rule.set_to_sorted_list(set_domestic_raw)
rule.batch_dump(list_domestic_sorted, const.TARGETS, const.PATH_DIST, "domestic.txt")

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
geosite.batch_convert(CATEGORIES, const.TARGETS, EXCLUSIONS)

END_TIME = time_ns()
logger.info(f"FINISHED Stage 3. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")
# Stage 3 finished.

# Stage 4: Build custom rules.
logger.info("START Stage 4: Build custom rules.")
START_TIME = time_ns()
list_file_custom = Path.iterdir(const.PATH_CUSTOM_BUILD)
for filename in list_file_custom:
    if filename.is_file():
        logger.debug(f'Start converting "{filename.name}".')
        set_custom = rule.custom_convert(filename)
        list_custom_sorted = rule.set_to_sorted_list(set_custom)
        rule.batch_dump(list_custom_sorted, const.TARGETS, const.PATH_DIST, filename.name)
        logger.debug(f"Converted {str(len(list_custom_sorted))} rules.")

list_file_personal = Path.iterdir(const.PATH_CUSTOM_BUILD/"personal")
for filename in list_file_personal:
    logger.debug(f'Start converting "{filename.name}".')
    set_personal = rule.custom_convert(filename)
    list_personal_sorted = rule.set_to_sorted_list(set_personal)
    rule.batch_dump(list_personal_sorted, const.TARGETS, const.PATH_DIST, "personal/" + filename.name)
    logger.debug(f"Converted {str(len(list_personal_sorted))} rules.")

END_TIME = time_ns()
logger.info(f"FINISHED Stage 4. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")
# Stage 4 finished

# For backward compatibility
copytree(const.PATH_DIST/"text", const.PATH_DIST/"surge", dirs_exist_ok=True)
copytree(const.PATH_DIST/"yaml", const.PATH_DIST/"clash", dirs_exist_ok=True)
