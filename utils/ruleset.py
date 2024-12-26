import logging
from json import dumps as json_dumps
from pathlib import Path

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType


def load(src: Path) -> RuleSet:
    with open(src, mode="r", encoding="utf-8") as raw:
        src_toload = raw.read().splitlines()
    try:
        ruleset_type = RuleSetType[src_toload[0].split("@")[1]]
    except IndexError:
        logging.warning(f"File {src} doesn't have a valid type header, treat as domain type.")
        ruleset_type = RuleSetType.Domain
    ruleset_loaded = RuleSet(ruleset_type, [])
    match ruleset_type:
        case RuleSetType.Domain:
            for line in src_toload:
                if line.startswith("."):
                    ruleset_loaded.add(Rule(RuleType.DomainSuffix, line.strip(".")))
                elif line and not line.startswith("#"):
                    ruleset_loaded.add(Rule(RuleType.DomainFull, line))
        case RuleSetType.IPCIDR:
            for line in src_toload:
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    ruleset_loaded.add(Rule(RuleType.IPCIDR6, line))
                else:
                    ruleset_loaded.add(Rule(RuleType.IPCIDR, line))
        case RuleSetType.Combined:
            for line in src_toload:
                if not line or line.startswith("#"):
                    continue
                parsed = line.split(",")
                rule_type = RuleType(parsed[0])
                if len(parsed) == 3:
                    parsed_rule = Rule(rule_type, parsed[1], parsed[2])
                else:
                    parsed_rule = Rule(rule_type, parsed[1])
                ruleset_loaded.add(parsed_rule)
    return ruleset_loaded


def dump(src: RuleSet, target: str, dst: Path, filename: str) -> None:
    if target not in config.TARGETS:
        raise TypeError("Invalid target.")
    match target:
        case "yaml":
            file = filename + ".yaml"
        case "geosite":
            file = filename
        case "sing-ruleset":
            file = filename + ".json"
        case _:
            file = filename + ".txt"
    dst.mkdir(parents=True, exist_ok=True)
    with open(dst/file, mode="w", encoding="utf-8") as dist:
        dist_built = ""
        if target in {"text", "text-plus"}:
            for rule in src:
                if rule.type == RuleType.DomainSuffix:
                    to_write = f"+.{rule.payload}\n" if target == "text-plus" else f".{rule.payload}\n"
                else:
                    to_write = f"{rule.payload}\n"
                dist_built += to_write
        elif target in {"surge-compatible", "clash-compatible", "yaml"}:
            if target == "yaml":
                dist_built += "payload:\n"
            for rule in src:
                if target == "yaml" and src.type != RuleSetType.Combined:
                    to_write = f"+.{rule.payload}" if rule.type == RuleType.DomainSuffix else rule.payload
                else:
                    prefix = rule.type.value
                    to_write = f"{prefix},{rule.payload}"
                if target == "clash-compatible":
                    to_write += ",Policy"
                if rule.tag:
                    to_write += f",{rule.tag}"
                if target == "yaml":
                    to_write = f"  - '{to_write}'"
                dist_built += f"{to_write}\n"
        elif target == "geosite":
            for rule in src:
                if rule.type == RuleType.DomainSuffix:
                    dist_built += f"{rule.payload}\n"
                elif rule.type == RuleType.DomainFull:
                    dist_built += f"full:{rule.payload}\n"
        elif target == "sing-ruleset":
            ruleset = {
                "version": 1,
                "rules": [{}]
            }
            for rule in src:
                match rule.type:
                    case RuleType.DomainFull:
                        key = "domain"
                    case RuleType.DomainSuffix:
                        key = "domain_suffix"
                    case _:
                        key = "ip_cidr"

                if key not in ruleset["rules"][0]:
                    ruleset["rules"][0][key] = []

                ruleset["rules"][0][key].append(rule.payload)
            dist_built = json_dumps(ruleset, indent=2)

        dist.write(dist_built)


def batch_dump(src: RuleSet, targets: list, dst_path: Path, filename: str) -> None:
    for target in targets:
        if src.type in {RuleSetType.IPCIDR, RuleSetType.Combined} and target in {"text-plus", "geosite"} \
                or src.type == RuleSetType.Combined and target == "text":
            logging.warning(f'{filename}: Ignore unsupported type "{target}" for {src.type.name} ruleset.')
            continue
        dump(src, target, dst_path/target, filename)


def patch(src: RuleSet, name: str, override_patch_loc: Path = Path("")) -> RuleSet:
    path_base = override_patch_loc if override_patch_loc != Path("") else config.PATH_SOURCE_PATCH
    try:
        loaded_patch = open(path_base/f"{name}.txt", mode="r", encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        logging.warning(f'Patch "{name + ".txt"}" not found.')
        return src
    logging.info(f'Apply patch "{name + ".txt"}"')
    for line in loaded_patch:
        if not line or line.startswith("#"):
            continue
        parsed_line = line.split(":")
        if parsed_line[1].startswith("."):
            rule = Rule(RuleType.DomainSuffix, parsed_line[1].strip("."))
        else:
            rule = Rule(RuleType.DomainFull, parsed_line[1])
        if parsed_line[0] == "ADD":
            if rule not in src:
                src.add(rule)
                logging.debug(f'Added: "{rule}"')
            else:
                logging.warning(f"Already exist: {rule}")
        elif parsed_line[0] == "REM":
            if rule in src:
                src.remove(rule)
                logging.debug(f'Removed: "{rule}"')
            else:
                logging.warning(f"Not found: {rule}")
    logging.info(f'Patch "{name + ".txt"}" applied.')
    return src
