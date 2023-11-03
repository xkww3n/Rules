import logging.config
from pathlib import Path
from time import time_ns

from abp.filters.parser import parse_filterlist
from aggregate6 import aggregate
from requests import Session

from Utils import const, geosite, rule

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("root")

# Generate reject and exclude rules.
logger.info("Start generating reject and exclude rules.")
START_TIME = time_ns()
connection = Session()

src_rejections = []
for url in const.LIST_REJECT_URL:
    src_rejections += (connection.get(url).text.splitlines())

logger.info(f"Imported {len(src_rejections)} lines of reject rules from defined sources.")

src_exclusions = []
for url in const.LIST_EXCL_URL:
    src_exclusions += connection.get(url).text.splitlines()

logger.info(f"Imported {len(src_exclusions)} lines of exclude rules from defined sources.")

set_rejections = set()
set_exclusions_raw = set()

for line in parse_filterlist(src_rejections):
    if rule.is_domain(line) and line.action == "block" and not line.text.endswith("|"):
        if line.text.startswith("."):
            rule_reject = rule.Rule("DomainSuffix", line.text.strip(".").strip("^"))
            set_rejections.add(rule_reject)
            logger.debug(f'Line "{line.text}" is added to reject set. {rule_reject}.')
        else:
            rule_reject = rule.Rule("DomainSuffix", line.text.strip("||").strip("^"))
            set_rejections.add(rule_reject)
            logger.debug(
                f'Line "{line.text}" is added to reject set. "{rule_reject}".'
            )
    elif rule.is_domain(line) and line.action == "allow" and not line.text.endswith("|"):
        src_exclusions.append(line.text)
        logger.debug(f'Line "{line.text}" is added to exclude set.')

for line in parse_filterlist(src_exclusions):
    if rule.is_domain(line):
        domain = line.text.strip("@").strip("^").strip("|")
        rule_exclude = rule.Rule("DomainFull", domain)
        set_exclusions_raw.add(rule_exclude)
        logger.debug(f'Line "{line.text}" is added to raw exclude set. "{rule_exclude}".')

src_rejections_v2fly = set(
    open(const.PATH_SOURCE_V2FLY/"category-ads-all", mode="r", encoding="utf-8").read().splitlines())
set_rejections_v2fly = geosite.parse(src_rejections_v2fly)
set_rejections |= set_rejections_v2fly
logger.info(f"Imported {(len(set_rejections_v2fly))} reject rules from v2fly category-ads-all list.")

set_exclusions = set()
logger.debug("Start deduplicating reject and exclude set.")
set_rejections = rule.dedup(set_rejections)
for domain_exclude in set_exclusions_raw.copy():
    for domain_reject in set_rejections.copy():
        if (domain_reject.Payload == domain_exclude.Payload and domain_reject.Type == domain_exclude.Type) \
                or (domain_reject.Payload == domain_exclude.Payload and
                    domain_reject.Type == "DomainFull" and domain_exclude.Type == "DomainSuffix"):
            set_rejections.remove(domain_reject)
            set_exclusions_raw.remove(domain_exclude)
            logger.debug(f"{domain_reject} is removed as excluded by {domain_exclude}.")

for domain_exclude in set_exclusions_raw:
    for domain_reject in set_rejections:
        if domain_exclude.Payload.endswith(domain_reject.Payload):
            set_exclusions.add(domain_exclude)
            logger.debug(f"{domain_exclude} is added to final exclude set.")

set_rejections = rule.apply_patch(set_rejections, "reject")
set_exclusions = rule.apply_patch(set_exclusions, "exclude")

logger.info(f"Generated {len(set_rejections)} reject rules.")
logger.info(f"Generated {len(set_exclusions)} exclude rules.")

list_rejections_sorted = rule.set_to_sorted_list(set_rejections)
list_exclusions_sorted = rule.set_to_sorted_list(set_exclusions)

rule.batch_dump(list_rejections_sorted, const.TARGETS, const.PATH_DIST, "reject")
rule.batch_dump(list_exclusions_sorted, const.TARGETS, const.PATH_DIST, "exclude")

END_TIME = time_ns()
logger.info(f"Finished. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")

# Generate domestic rules.
logger.info("Start generating domestic rules.")
START_TIME = time_ns()

src_domestic = set(open(const.PATH_SOURCE_V2FLY/"geolocation-cn", mode="r", encoding="utf-8").read().splitlines())
set_domestic = geosite.parse(src_domestic, None, ["!cn"])
logger.info(f"Imported {len(set_domestic)} domestic rules from v2fly geolocation-cn list.")

# Add all domestic TLDs to domestic rules, then perform deduplication.
src_domestic_tlds = set(open(const.PATH_SOURCE_V2FLY/"tld-cn", mode="r", encoding="utf-8").read().splitlines())
set_domestic_tlds = geosite.parse(src_domestic_tlds)
logger.info(f"Imported {len(set_domestic_tlds)} domestic TLDs.")
set_domestic |= set_domestic_tlds
set_domestic = rule.apply_patch(set_domestic, "domestic")
set_domestic = rule.dedup(set_domestic)
for item in set_domestic.copy():
    tld_overseas = (".hk", ".kr", ".my", ".sg", ".au", ".tw", ".in", ".ru", ".us", ".fr", ".th", ".id", ".jp")
    if any([item.Payload.endswith(os_tld) for os_tld in tld_overseas]):
        set_domestic.remove(item)
        logger.debug(f"{item} removed for having a overseas TLD.")
logger.info(f"Generated {len(set_domestic)} domestic rules.")

list_domestic_sorted = rule.set_to_sorted_list(set_domestic)
rule.batch_dump(list_domestic_sorted, const.TARGETS, const.PATH_DIST, "domestic")

END_TIME = time_ns()
logger.info(f"Finished. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")

# Convert domestic CIDR rules.
logger.info("Start converting domestic CIDR rules.")
START_TIME = time_ns()
src_cidr = connection.get(const.URL_CHNROUTES2).text.splitlines()
list_cidr = []
for line in src_cidr:
    if not line.startswith("#"):
        list_cidr.append(rule.Rule("IPCIDR", line))
logger.info(f"Generated {len(list_cidr)} domestic IPv4 rules.")
rule.batch_dump(list_cidr, ["text", "text-plus", "yaml", "surge-compatible", "clash-compatible"],
                const.PATH_DIST, "domestic_ip")

src_cidr6 = connection.get(const.URL_CHNROUTES_V6).text.splitlines()
list_cidr6_raw = []
for line in src_cidr6:
    if "apnic|CN|ipv6" in line:
        parts = line.split("|")
        list_cidr6_raw.append(f"{parts[3]}/{parts[4]}")
list_cidr6_raw = aggregate(list_cidr6_raw)
list_cidr6 = []
for cidr in list_cidr6_raw:
    list_cidr6.append(rule.Rule("IPCIDR6", cidr))
logger.info(f"Generated {len(list_cidr6)} domestic IPv6 rules.")
rule.batch_dump(list_cidr6, ["text", "text-plus", "yaml", "surge-compatible", "clash-compatible"],
                const.PATH_DIST, "domestic_ip6")
END_TIME = time_ns()
logger.info(f"Finished. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")

# Convert v2fly community rules.
logger.info("Start converting v2fly community rules.")
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
    "github",  # GitHub's domains are included in "microsoft", but its connectivity mostly isn't as high as Microsoft.
    "bing",  # Bing has a more restricted ver for Mainland China.
]
geosite.batch_convert(CATEGORIES, const.TARGETS, EXCLUSIONS)

END_TIME = time_ns()
logger.info(f"Finished. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")

# Generate custom rules.
logger.info("Start generating custom rules.")
START_TIME = time_ns()
list_file_custom = Path.iterdir(const.PATH_SOURCE_CUSTOM)
for filename in list_file_custom:
    if filename.is_file():
        logger.debug(f'Start converting "{filename.name}".')
        set_custom = rule.custom_convert(filename)
        is_classical = False
        is_ipcidr = False
        for item in set_custom:
            if item.Type == "Classic":
                is_classical = True  # If one rule's type is "Classic", this is a classical ruleset.
                break
            if item.Type == "IPCIDR":
                is_ipcidr = True
                break
            break
        list_custom_sorted = rule.set_to_sorted_list(set_custom)
        if is_classical:
            rule.batch_dump(list_custom_sorted,
                            ["yaml", "surge-compatible", "clash-compatible"],
                            # Classical ruleset doesn't have plain text type.
                            const.PATH_DIST, filename.stem)
        elif is_ipcidr:
            rule.batch_dump(list_custom_sorted,
                            ["text", "text-plus", "yaml", "surge-compatible", "clash-compatible"],
                            const.PATH_DIST, filename.stem)
        else:
            rule.batch_dump(list_custom_sorted, const.TARGETS, const.PATH_DIST, filename.stem)
        logger.debug(f"Converted {len(list_custom_sorted)} rules.")

# There's no personal classical type ruleset. So no logic about that.
list_file_personal = Path.iterdir(const.PATH_SOURCE_CUSTOM/"personal")
for filename in list_file_personal:
    logger.debug(f'Start converting "{filename.name}".')
    set_personal = rule.custom_convert(filename)
    list_personal_sorted = rule.set_to_sorted_list(set_personal)
    rule.batch_dump(list_personal_sorted, ["text", "text-plus", "yaml", "surge-compatible", "clash-compatible"],
                    const.PATH_DIST/"personal", filename.stem)
    rule.dump(list_personal_sorted, "geosite", const.PATH_DIST/"geosite", ("personal-" + filename.stem))
    logger.debug(f"Converted {len(list_personal_sorted)} rules.")

END_TIME = time_ns()
logger.info(f"Finished. Total time: {format((END_TIME - START_TIME) / 1e9, '.3f')}s\n")
