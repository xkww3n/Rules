import logging

from abp.filters.parser import parse_filterlist
from requests import Session

import config
from models.log_decoration import log
from models.rule import Rule
from models.ruleset import RuleSet
from utils import rule, ruleset


@log
def build():
    """
    reject and exclude ruleset
    """

    connection = Session()

    src_psl = connection.get("https://publicsuffix.org/list/public_suffix_list.dat").text.splitlines()
    set_psl = set()
    for line in src_psl:
        if "//" not in line and "." in line:
            if line.startswith("*"):
                line = line.strip("*")
            set_psl.add(line)

    src_rejections = []
    for url in config.LIST_REJECT_URL:
        src_rejections += (connection.get(url).text.splitlines())

    logging.info(f"Imported {len(src_rejections)} lines of reject rules from defined sources.")

    src_exclusions = []
    for url in config.LIST_EXCL_URL:
        src_exclusions += connection.get(url).text.splitlines()

    logging.info(f"Imported {len(src_exclusions)} lines of exclude rules from defined sources.")

    ruleset_rejections = RuleSet("Domain", [])
    ruleset_exclusions_raw = RuleSet("Domain", [])

    for line in parse_filterlist(src_rejections):
        line_stripped = rule.strip_adblock(line)
        if line_stripped and rule.is_domain(line_stripped):
            if line.action == "block":
                if line.text.startswith("."):
                    line_stripped = line.text.strip(".").strip("^")
                else:
                    line_stripped = line.text.strip("|").strip("^")
                domain_level = line_stripped.count(".")
                if any(ps in line_stripped for ps in set_psl):
                    domain_level -= 1
                if domain_level == 1:
                    rule_reject = Rule("DomainSuffix", line_stripped)
                else:
                    rule_reject = Rule("DomainFull", line_stripped)
                ruleset_rejections.add(rule_reject)
                logging.debug(f'Line "{line.text}" is added to reject set. "{rule_reject}".')
            elif line.action == "allow":
                src_exclusions.append(line.text)
                logging.debug(f'Line "{line.text}" is added to exclude set.')

    for line in parse_filterlist(src_exclusions):
        line_stripped = rule.strip_adblock(line)
        if line_stripped and rule.is_domain(line_stripped):
            rule_exclude = Rule("DomainFull", line_stripped)
            ruleset_exclusions_raw.add(rule_exclude)
            logging.debug(f'Line "{line.text}" is added to raw exclude set. "{rule_exclude}".')

    ruleset_rejections = ruleset.patch(ruleset_rejections, "reject")
    ruleset_exclusions = RuleSet("Domain", [])
    logging.debug("Deduplicate reject and exclude set.")
    ruleset.dedup(ruleset_rejections)
    for domain_exclude in ruleset_exclusions_raw.deepcopy():
        for domain_reject in ruleset_rejections.deepcopy():
            if (domain_reject.Payload == domain_exclude.Payload and domain_reject.Type == domain_exclude.Type) \
                    or (domain_reject.Payload == domain_exclude.Payload and
                        domain_reject.Type == "DomainFull" and domain_exclude.Type == "DomainSuffix"):
                ruleset_rejections.remove(domain_reject)
                ruleset_exclusions_raw.remove(domain_exclude)
                logging.debug(f"{domain_reject} is removed as excluded by {domain_exclude}.")
    ruleset.batch_dump(ruleset_rejections, config.TARGETS, config.PATH_DIST, "reject")
    logging.info(f"Processed {len(ruleset_rejections)} reject rules.")

    for domain_exclude in ruleset_exclusions_raw:
        for domain_reject in ruleset_rejections:
            if domain_exclude.Payload.endswith(domain_reject.Payload):
                ruleset_exclusions.add(domain_exclude)
                logging.debug(f"{domain_exclude} is added to final exclude set.")
    ruleset_exclusions = ruleset.patch(ruleset_exclusions, "exclude")
    logging.info(f"Processed {len(ruleset_exclusions)} exclude rules.")
    ruleset.batch_dump(ruleset_exclusions, config.TARGETS, config.PATH_DIST, "exclude")
