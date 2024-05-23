import logging
from json import dumps
from pathlib import Path

import config
from models.rule import Rule
from models.ruleset import RuleSet


def load(src: Path) -> RuleSet:
    with open(src, mode="r", encoding="utf-8") as raw:
        src_toload = raw.read().splitlines()
    try:
        ruleset_type = src_toload[0].split("@")[1]
    except IndexError:
        logging.warning(f"File {src} doesn't have a valid type header, treat as domain type.")
        ruleset_type = "Domain"
    ruleset_loaded = RuleSet(ruleset_type, [])
    match ruleset_type:
        case "Domain":
            for line in src_toload:
                if line.startswith("."):
                    ruleset_loaded.add(Rule("DomainSuffix", line.strip(".")))
                elif line and not line.startswith("#"):
                    ruleset_loaded.add(Rule("DomainFull", line))
        case "IPCIDR":
            for line in src_toload:
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    ruleset_loaded.add(Rule("IPCIDR6", line))
                else:
                    ruleset_loaded.add(Rule("IPCIDR", line))
        case "Combined":
            for line in src_toload:
                if not line or line.startswith("#"):
                    continue
                parsed = line.split(",")
                rule_type = config.RULE_TYPE_CONVERSION[parsed[0]]
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
        if target in ("text", "text-plus"):
            for rule in src:
                to_write = rule.payload if rule.type in ("DomainFull", "IPCIDR", "IPCIDR6") else f".{rule.payload}"
                to_write = f"+{to_write}\n" if (target == "text-plus"
                                                and rule.type == "DomainSuffix"
                                                ) else f"{to_write}\n"
                dist.writelines(to_write)
        elif target in ("surge-compatible", "clash-compatible", "yaml"):
            if target == "yaml":
                dist.writelines("payload:\n")
            for rule in src:
                if target == "yaml" and src.type != "Combined":
                    to_write = f"+.{rule.payload}" if rule.type == "DomainSuffix" else rule.payload
                else:
                    prefix = list(config.RULE_TYPE_CONVERSION.keys())[
                        list(config.RULE_TYPE_CONVERSION.values()).index(rule.type)
                    ]  # Reverse lookup the conversion table
                    to_write = f"{prefix},{rule.payload}"
                if target == "clash-compatible":
                    to_write += ",Policy"
                if rule.tag:
                    to_write += f",{rule.tag}"
                if target == "yaml":
                    to_write = f"  - '{to_write}'"
                dist.writelines(f"{to_write}\n")
        elif target == "geosite":
            for rule in src:
                if rule.type == "DomainSuffix":
                    dist.writelines(f"{rule.payload}\n")
                elif rule.type == "DomainFull":
                    dist.writelines(f"full:{rule.payload}\n")
        elif target == "sing-ruleset":
            ruleset = {
                "version": 1,
                "rules": [{}]
            }
            for rule in src:
                match rule.type:
                    case "DomainFull":
                        key = "domain"
                    case "DomainSuffix":
                        key = "domain_suffix"
                    case _:
                        key = "ip_cidr"

                if key not in ruleset["rules"][0]:
                    ruleset["rules"][0][key] = []

                ruleset["rules"][0][key].append(rule.payload)
            dist.write(dumps(ruleset, indent=2))


def batch_dump(src: RuleSet, targets: list, dst_path: Path, filename: str) -> None:
    for target in targets:
        if src.type in ["IPCIDR", "Combined"] and target in ["text-plus", "geosite"] \
                or src.type == "Combined" and target == "text":
            logging.warning(f'{filename}: Ignored unsupported type "{target}" for {src.type} ruleset.')
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
            rule = Rule("DomainSuffix", parsed_line[1].strip("."))
        else:
            rule = Rule("DomainFull", parsed_line[1])
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
