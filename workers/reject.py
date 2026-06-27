import logging

from requests import Session

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType
from utils.log_decorator import log
from utils.rule import parse_adblock_domain_rules
from utils.ruleset import batch_dump, patch


def apply_allowlist(ruleset_rejections: RuleSet, ruleset_exclusions: RuleSet) -> RuleSet:
    filtered_rejections = RuleSet(RuleSetType.Domain)
    removed_by_allowlist = 0

    for rule in ruleset_rejections:
        covering_allow = ruleset_exclusions.find_covering(rule)
        if covering_allow:
            removed_by_allowlist += 1
            logging.debug(f'Remove "{rule}": allowlisted by "{covering_allow}".')
            continue
        filtered_rejections.add(rule)

    conflicts = []
    for rule in sorted(ruleset_exclusions, key=lambda item: (item.payload, item.type.value, item.tag)):
        covering_block = filtered_rejections.find_covering(rule)
        if covering_block:
            conflicts.append((rule, covering_block))

    blocking_rules_to_remove = {blocking_rule for _, blocking_rule in conflicts}
    if blocking_rules_to_remove:
        resolved_rejections = RuleSet(RuleSetType.Domain)
        for rule in filtered_rejections:
            if rule not in blocking_rules_to_remove:
                resolved_rejections.add(rule)
        filtered_rejections = resolved_rejections

    if removed_by_allowlist:
        logging.info(f"{removed_by_allowlist} reject rules removed by allowlist.")

    if conflicts:
        logging.warning(
            f"{len(conflicts)} allowlist rules were covered by reject rules; "
            f"{len(blocking_rules_to_remove)} reject rules removed."
        )
        for allowed_rule, blocking_rule in conflicts:
            logging.debug(f'Allowlist conflict: "{blocking_rule}" removed for covering "{allowed_rule}".')

    return filtered_rejections


def add_parsed_adblock_rules(
    lines: list[str],
    set_psl: set[str],
    ruleset_rejections: RuleSet,
    ruleset_exclusions: RuleSet,
    source_name: str,
    force_exclusion: bool = False
) -> None:
    skipped_count, parsed_rules = parse_adblock_domain_rules(lines, set_psl)
    logging.info(f"{skipped_count} {source_name} rule lines skipped before parsing.")

    for action, text, domain, include_subdomains in parsed_rules:
        if include_subdomains:
            rule = Rule(RuleType.DomainSuffix, domain)
        else:
            # If a domain's level is bigger than 2, this domain mostly doesn't have any other subdomain.
            rule = Rule(RuleType.DomainFull, domain)

        if force_exclusion or action == "allow":
            ruleset_exclusions.add(rule)
            logging.debug(f'Exclude: Added "{text}" -> "{rule}"')
        elif action == "block":
            ruleset_rejections.add(rule)
            logging.debug(f'Reject: Added "{text}" -> "{rule}".')


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

    ruleset_rejections = RuleSet(RuleSetType.Domain)
    ruleset_exclusions = RuleSet(RuleSetType.Domain)

    add_parsed_adblock_rules(src_rejections, set_psl, ruleset_rejections, ruleset_exclusions, "reject")
    add_parsed_adblock_rules(src_exclusions, set_psl, ruleset_rejections, ruleset_exclusions, "exclude", True)

    logging.debug("Use deduplicated raw reject and allowlist rulesets.")

    ruleset_rejections = patch(ruleset_rejections, "reject")

    ruleset_rejections = apply_allowlist(ruleset_rejections, ruleset_exclusions)
    
    batch_dump(ruleset_rejections, config.TARGETS, config.PATH_DIST, "reject")
    logging.info(f"{len(ruleset_rejections)} reject rules generated.")
