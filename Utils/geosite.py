import logging

from . import const, rule


def parse(src: set, excluded_imports=None, excluded_tags=None) -> rule.RuleSet:
    excluded_imports = [] if not excluded_imports else excluded_imports
    excluded_tags = [] if not excluded_tags else excluded_tags
    ruleset_parsed = rule.RuleSet("Domain", [])
    for raw_line in src:
        line = raw_line.split("#")[0].strip()
        if not line:
            continue
        parsed_rule = rule.Rule()
        if "@" in line:
            parsed_rule.set_tag(line.split("@")[1])
            if parsed_rule.Tag in excluded_tags:
                logging.debug(f'Line "{raw_line}" has a excluded tag "{parsed_rule.Tag}", skipped.')
                continue
            line = line.split(" @")[0]
        if ":" not in line:
            parsed_rule.set_type("DomainSuffix")
            parsed_rule.set_payload(line)
        elif line.startswith("full:"):
            parsed_rule.set_type("DomainFull")
            parsed_rule.set_payload(line.strip("full:"))
        elif line.startswith("include:"):
            name_import = line.split("include:")[1]
            if name_import not in excluded_imports:
                logging.debug(f'Line "{raw_line}" is a import rule. Start importing "{name_import}".')
                src_import = set(
                    open(const.PATH_SOURCE_V2FLY/name_import, mode="r", encoding="utf-8").read().splitlines())
                ruleset_parsed |= parse(src_import, excluded_imports, excluded_tags)
                logging.debug(f'Imported "{name_import}".')
                continue
            else:
                logging.debug(f'Line "{raw_line}" is a import rule, but hit exclusion "{name_import}", skipped.')
                continue
        else:
            logging.debug(f'Unsupported rule: "{raw_line}", skipped.')
            continue
        ruleset_parsed.add(parsed_rule)
        logging.debug(f'Line "{raw_line}" is parsed: {parsed_rule}')
    return ruleset_parsed


def batch_convert(categories: list, tools: list, exclusions=None) -> None:
    exclusions = [] if not exclusions else exclusions
    for tool in tools:
        for category in categories:
            src_geosite = set(open(const.PATH_SOURCE_V2FLY/category, mode="r", encoding="utf-8").read().splitlines())
            ruleset_geosite = parse(src_geosite, exclusions)
            ruleset_geosite.sort()
            rule.dump(ruleset_geosite, tool, const.PATH_DIST/tool, category)
