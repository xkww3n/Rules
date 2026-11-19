import logging
from pathlib import Path

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType
from utils import ruleset


def parse(src_path: Path, excluded_imports=None, only_tags=None, excluded_tags=None) -> RuleSet:
    ruleset_parsed = RuleSet(RuleSetType.Domain)
    _parse_into(src_path, ruleset_parsed, excluded_imports or [], only_tags or [], excluded_tags or [])
    return ruleset_parsed


def _parse_into(src_path: Path, ruleset_parsed: RuleSet, excluded_imports, only_tags, excluded_tags) -> None:
    with open(src_path, mode="r", encoding="utf-8") as raw:
        src = raw.read().splitlines()
    for raw_line in src:
        line = raw_line.split("#")[0].strip()
        if not line:
            continue
        if "@" in line:
            rule_tag = line.split(" @")[1]
            line = line.split(" @")[0]
            has_ruletag = True
        else:
            has_ruletag = False
        if line.startswith("include:"):
            name_import = line.split("include:")[1]
            if name_import in excluded_imports:
                logging.debug(f'Skipped (excl.import "{name_import}"): "{raw_line}"')
                continue
            child_onlytags = only_tags
            child_excltags = excluded_tags
            if has_ruletag:
                if rule_tag.startswith("-"):
                    child_excltags = [*excluded_tags, rule_tag[1:]]
                else:
                    child_onlytags = [*only_tags, rule_tag]
            logging.debug(f'Import ("{raw_line}"): "{name_import}" with only tags {child_onlytags} excl tags {child_excltags}')
            _parse_into(src_path.parent/name_import, ruleset_parsed, excluded_imports, child_onlytags, child_excltags)
            logging.debug(f'"{name_import}" imported.')
            continue
        if only_tags and (not has_ruletag or rule_tag not in only_tags):
            logging.debug(f'Skipped (only tag "{only_tags}"): "{raw_line}"')
            continue
        elif excluded_tags and has_ruletag and rule_tag in excluded_tags:
            logging.debug(f'Skipped (excl tag "{rule_tag}"): "{raw_line}"')
            continue
        if ":" not in line:
            parsed_rule = Rule(RuleType.DomainSuffix, line)
        elif line.startswith("full:"):
            parsed_rule = Rule(RuleType.DomainFull, line.replace("full:",""))
        else:
            logging.debug(f'Skipped (unsupported): "{raw_line}"')
            continue
        ruleset_parsed.add(parsed_rule)
        logging.debug(f'Parsed: "{raw_line}" -> "{parsed_rule}"')


def batch_gen(categories: list, tools: list, exclusions=None) -> None:
    for category in categories:
        ruleset_geosite = parse(config.PATH_SOURCE_GEOSITE/category, exclusions)
        ruleset.batch_dump(ruleset_geosite, tools, config.PATH_DIST, category)
