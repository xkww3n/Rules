import logging

from abp.filters.parser import parse_filterlist
from requests import Session

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType
from utils.log_decorator import log
from utils.rule import strip_adblock
from utils.ruleset import batch_dump, patch


@log
def build():
    """
    reject and exclude ruleset
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

    logging.info(f"Imported {len(src_rejections)} lines of reject rules from defined sources.")

    src_exclusions = []
    for url in config.LIST_EXCL_URL:
        src_exclusions += connection.get(url).text.splitlines()

    logging.info(f"Imported {len(src_exclusions)} lines of exclude rules from defined sources.")

    ruleset_rejections = RuleSet(RuleSetType.Domain, [])
    ruleset_exclusions_raw = RuleSet(RuleSetType.Domain, [])

    for line in parse_filterlist(src_rejections):
        line_stripped = strip_adblock(line)
        if not line_stripped:
            continue
        if line.action == "block":
            if line_stripped.startswith("."):
                line_stripped = line_stripped.strip(".")
            domain_level = line_stripped.count(".")
            for ps in set_psl:
                if line_stripped.endswith(ps):
                    domain_level -= ps.count(".") - 1
            if domain_level <= 2:
                rule_reject = Rule(RuleType.DomainSuffix, line_stripped)
            else:
                # If a domain's level is bigger than 2, this domain mostly doesn't have any other subdomain.
                rule_reject = Rule(RuleType.DomainFull, line_stripped)
            ruleset_rejections.add(rule_reject)
            logging.debug(f'(ruleset) Reject: Added "{line.text}" -> "{rule_reject}".')
        elif line.action == "allow":
            src_exclusions.append(line.text)
            logging.debug(f'(source) Exclude: Added "{line.text}"')

    for line in parse_filterlist(src_exclusions):
        line_stripped = strip_adblock(line)
        if not line_stripped:
            continue
        rule_exclude = Rule(RuleType.DomainFull, line_stripped)
        ruleset_exclusions_raw.add(rule_exclude)
        logging.debug(f'(ruleset) Exclude_raw: Added "{line.text}" -> "{rule_exclude}"')

    ruleset_rejections = patch(ruleset_rejections, "reject")
    ruleset_exclusions = RuleSet(RuleSetType.Domain, [])
    logging.debug("Deduplicate reject and exclude set.")
    ruleset_rejections.dedup()
    for domain_exclude in ruleset_exclusions_raw.deepcopy():
        for domain_reject in ruleset_rejections.deepcopy():
            if domain_exclude.includes(domain_reject):
                ruleset_rejections.remove(domain_reject)
                ruleset_exclusions_raw.remove(domain_exclude)
                logging.debug(f'Removed "{domain_reject}": excluded by "{domain_exclude}"')
    batch_dump(ruleset_rejections, config.TARGETS, config.PATH_DIST, "reject")
    logging.info(f"Processed {len(ruleset_rejections)} reject rules.")

    for domain_exclude in ruleset_exclusions_raw:
        for domain_reject in ruleset_rejections:
            if domain_reject.includes(domain_exclude):
                ruleset_exclusions.add(domain_exclude)
                logging.debug(f'(ruleset) Exclude: Added "{domain_exclude}"')
    ruleset_exclusions = patch(ruleset_exclusions, "exclude")
    logging.info(f"Processed {len(ruleset_exclusions)} exclude rules.")
    batch_dump(ruleset_exclusions, config.TARGETS, config.PATH_DIST, "exclude")
