import logging

from abp.filters.parser import parse_filterlist
from requests import Session

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType
from utils.log_decorator import log
from utils.rule import count_domain_level, strip_adblock
from utils.ruleset import batch_dump, patch


@log
def build():
    """
    reject ruleset
    """

    connection = Session()

    # ps for public suffix, such as ".org.cn". Useful when guessing domains' levels.
    src_psl = connection.get("https://publicsuffix.org/list/public_suffix_list.dat").text.splitlines()
    set_psl = set()
    for line in src_psl:
        if "//" in line or "." not in line:
            continue
        if line.startswith("*"):
            line = line.strip("*.")
        set_psl.add(f".{line}")

    src_rejections = []
    for url in config.LIST_REJECT_URL:
        src_rejections += (connection.get(url).text.splitlines())

    logging.info(f"{len(src_rejections)} lines of reject rule recieved.")

    src_exclusions = []
    for url in config.LIST_EXCL_URL:
        src_exclusions += connection.get(url).text.splitlines()

    logging.info(f"{len(src_exclusions)} lines of exclude rule recieved.")

    ruleset_rejections = RuleSet(RuleSetType.Domain, [])
    ruleset_exclusions = set()

    for line in parse_filterlist(src_rejections):
        line_stripped = strip_adblock(line)
        if not line_stripped:
            continue
        if line_stripped.startswith("."):
            line_stripped = line_stripped.strip(".")
        domain_level = count_domain_level(line_stripped, set_psl)
        if domain_level <= 2:
            rule = Rule(RuleType.DomainSuffix, line_stripped)
        else:
            # If a domain's level is bigger than 2, this domain mostly doesn't have any other subdomain.
            rule = Rule(RuleType.DomainFull, line_stripped)
        if line.action == "block":
            ruleset_rejections.add(rule)
            logging.debug(f'Reject: Added "{line.text}" -> "{rule}".')
        elif line.action == "allow":
            ruleset_exclusions.add(rule)
            logging.debug(f'Exclude: Added "{line.text}" -> "{rule}"')

    for line in parse_filterlist(src_exclusions):
        line_stripped = strip_adblock(line)
        if not line_stripped:
            continue
        if line_stripped.startswith("."):
            line_stripped = line_stripped.strip(".")
        domain_level = count_domain_level(line_stripped, set_psl)
        if domain_level <= 2:
            rule = Rule(RuleType.DomainSuffix, line_stripped)
        else:
            rule = Rule(RuleType.DomainFull, line_stripped)
        ruleset_exclusions.add(rule)
        logging.debug(f'Exclude: Added "{line.text}" -> "{rule}"')

    ruleset_rejections = patch(ruleset_rejections, "reject")
    logging.debug("Deduplicate reject ruleset.")
    ruleset_rejections.dedup()
    
    # Remove rejected domains that are included in exclusions
    new_ruleset_rejections = [item for item in ruleset_rejections if item not in ruleset_exclusions]
    ruleset_rejections.payload = new_ruleset_rejections
    
    batch_dump(ruleset_rejections, config.TARGETS, config.PATH_DIST, "reject")
    logging.info(f"{len(ruleset_rejections)} reject rules generated.")
