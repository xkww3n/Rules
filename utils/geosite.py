from copy import deepcopy
import logging
from pathlib import Path

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType
from utils import ruleset


def parse(src_path: Path, excluded_imports=None, only_tags=None, excluded_tags=None) -> RuleSet:
    with open(src_path, mode="r", encoding="utf-8") as raw:
        src = raw.read().splitlines()
    excluded_imports = excluded_imports or []
    only_tags = only_tags or []
    excluded_tags = excluded_tags or []
    ruleset_parsed = RuleSet(RuleSetType.Domain)
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
            child_onlytags = deepcopy(only_tags)
            child_excltags = deepcopy(excluded_tags)
            if has_ruletag:
                if rule_tag.startswith("-"):
                    child_excltags.append(rule_tag[1:])
                else:
                    child_onlytags.append(rule_tag)
                name_import = name_import.split(" @")[0]
            logging.debug(f'Import ("{raw_line}"): "{name_import}" with only tags {child_onlytags} excl tags {child_excltags}')
            imported_ruleset = parse(src_path.parent/name_import, excluded_imports, child_onlytags, child_excltags)
            for imported_rule in imported_ruleset:
                ruleset_parsed.add(imported_rule)
            logging.debug(f'"{name_import}" imported.')
            continue  # Import rule itself doesn't contain any content and can't be included in a ruleset,
            # so whether an import rule is processed or not, the code below shouldn't be executed.
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
    return ruleset_parsed


def batch_gen(categories: list, tools: list, exclusions=None) -> None:
    exclusions = exclusions or []
    for category in categories:
        ruleset_geosite = parse(config.PATH_SOURCE_GEOSITE/category, exclusions)
        for tool in tools:
            ruleset.dump(ruleset_geosite, tool, config.PATH_DIST/tool, category)
