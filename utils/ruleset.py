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

    rules_to_add = []

    match ruleset_type:
        case RuleSetType.Domain:
            domain_suffix_rules = [
                Rule(RuleType.DomainSuffix, line.strip("."))
                for line in src_toload
                if line.startswith(".") and line
            ]

            domain_full_rules = [
                Rule(RuleType.DomainFull, line)
                for line in src_toload
                if line and not line.startswith("#") and not line.startswith(".")
            ]

            rules_to_add.extend(domain_suffix_rules)
            rules_to_add.extend(domain_full_rules)

        case RuleSetType.IPCIDR:
            ipv4_rules = [
                Rule(RuleType.IPCIDR, line)
                for line in src_toload
                if line and not line.startswith("#") and ":" not in line
            ]

            ipv6_rules = [
                Rule(RuleType.IPCIDR6, line)
                for line in src_toload
                if line and not line.startswith("#") and ":" in line
            ]

            rules_to_add.extend(ipv4_rules)
            rules_to_add.extend(ipv6_rules)

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
                rules_to_add.append(parsed_rule)

    ruleset_loaded.payload = rules_to_add
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

    def generate_content():
        if target in {"text", "text-plus"}:
            for rule in src:
                if rule.type == RuleType.DomainSuffix:
                    yield f"+.{rule.payload}\n" if target == "text-plus" else f".{rule.payload}\n"
                else:
                    yield f"{rule.payload}\n"
        elif target in {"surge-compatible", "clash-compatible", "yaml"}:
            if target == "yaml":
                yield "payload:\n"
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
                yield f"{to_write}\n"
        elif target == "geosite":
            for rule in src:
                if rule.type == RuleType.DomainSuffix:
                    yield f"{rule.payload}\n"
                elif rule.type == RuleType.DomainFull:
                    yield f"full:{rule.payload}\n"
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
            yield json_dumps(ruleset, indent=2)

    with open(dst/file, mode="w", encoding="utf-8", buffering=8192) as dist:
        for chunk in generate_content():
            dist.write(chunk)


def batch_dump(src: RuleSet, targets: list, dst_path: Path, filename: str) -> None:
    compatible_targets = []
    for target in targets:
        if src.type in {RuleSetType.IPCIDR, RuleSetType.Combined} and target in {"text-plus", "geosite"} \
                or src.type == RuleSetType.Combined and target == "text":
            logging.warning(f'{filename}: Ignore unsupported type "{target}" for {src.type.name} ruleset.')
            continue
        compatible_targets.append(target)

    if not compatible_targets:
        return

    for target in compatible_targets:
        (dst_path/target).mkdir(parents=True, exist_ok=True)

    for target in compatible_targets:
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
