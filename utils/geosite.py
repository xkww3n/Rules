import logging
from pathlib import Path

import config
from models.rule import Rule
from models.ruleset import RuleSet
from utils import ruleset


def parse(src_path: Path, excluded_imports=None, excluded_tags=None) -> RuleSet:
    with open(src_path, mode="r", encoding="utf-8") as raw:
        src = raw.read().splitlines()
    excluded_imports = [] if not excluded_imports else excluded_imports
    excluded_tags = [] if not excluded_tags else excluded_tags
    ruleset_parsed = RuleSet("Domain", [])
    for raw_line in src:
        line = raw_line.split("#")[0].strip()
        if not line:
            continue
        parsed_rule = Rule()
        if "@" in line:
            parsed_rule_tag = line.split("@")[1]
            if parsed_rule_tag in excluded_tags:
                logging.debug(f'Skipped (excl.tag "{parsed_rule_tag}"): "{raw_line}"')
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
            if name_import in excluded_imports:
                logging.debug(f'Skipped (excl.import "{name_import}"): "{raw_line}"')
                continue
            logging.debug(f'Import ("{raw_line}"): "{name_import}"')
            ruleset_parsed |= parse(src_path.parent/name_import, excluded_imports, excluded_tags)
            logging.debug(f'Imported "{name_import}".')
            continue  # Import rule itself doesn't contain any content and can't be included in a ruleset,
            # so whether an import rule is processed or not, the code below shouldn't be executed.
        else:
            logging.debug(f'Skipped (unsupported): "{raw_line}"')
            continue
        ruleset_parsed.add(parsed_rule)
        logging.debug(f'Parsed: "{raw_line}" as "{parsed_rule}"')
    return ruleset_parsed


def batch_gen(categories: list, tools: list, exclusions=None) -> None:
    exclusions = [] if not exclusions else exclusions
    for tool in tools:
        for category in categories:
            ruleset_geosite = parse(config.PATH_SOURCE_GEOSITE/category, exclusions)
            ruleset.dedup(ruleset_geosite)
            ruleset.dump(ruleset_geosite, tool, config.PATH_DIST/tool, category)
