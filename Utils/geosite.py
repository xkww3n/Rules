import logging

from . import const, rule


def parse(src: set, excluded_imports=None, excluded_tags=None) -> set:
    excluded_imports = [] if not excluded_imports else excluded_imports
    excluded_tags = [] if not excluded_tags else excluded_tags
    set_parsed = set()
    for raw_line in src:
        line = raw_line.split("#")[0].strip()
        if not line:
            continue
        parsed_rule = rule.Rule()
        if "@" in line:
            parsed_rule.Tag = line.split("@")[1]
            if parsed_rule.Tag in excluded_tags:
                logging.debug(f'Line "{raw_line}" has a excluded tag "{parsed_rule.Tag}", skipped.')
                continue
            line = line.split(" @")[0]
        if ":" not in line:
            parsed_rule.Type = "DomainSuffix"
            parsed_rule.Payload = line
        elif line.startswith("full:"):
            parsed_rule.Type = "DomainFull"
            parsed_rule.Payload = line.strip("full:")
        elif line.startswith("include:"):
            name_import = line.split("include:")[1]
            if name_import not in excluded_imports:
                logging.debug(f'Line "{raw_line}" is a import rule. Start importing "{name_import}".')
                src_import = set(
                    open(const.PATH_SOURCE_V2FLY/name_import, mode="r", encoding="utf-8").read().splitlines())
                set_parsed |= parse(src_import, excluded_imports, excluded_tags)
                logging.debug(f'Imported "{name_import}".')
                continue
            else:
                logging.debug(f'Line "{raw_line}" is a import rule, but hit exclusion "{name_import}", skipped.')
                continue
        else:
            logging.debug(f'Unsupported rule: "{raw_line}", skipped.')
            continue
        set_parsed.add(parsed_rule)
        logging.debug(f'Line "{raw_line}" is parsed: {parsed_rule}')
    return set_parsed


def batch_convert(categories: list, tools: list, exclusions=None) -> None:
    exclusions = [] if not exclusions else exclusions
    for tool in tools:
        for category in categories:
            src_geosite = set(open(const.PATH_SOURCE_V2FLY/category, mode="r", encoding="utf-8").read().splitlines())
            set_geosite = parse(src_geosite, exclusions)
            list_geosite_sorted = rule.set_to_sorted_list(set_geosite)
            rule.dump(list_geosite_sorted, tool, const.PATH_DIST/tool, category)
