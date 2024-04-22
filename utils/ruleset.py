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
                to_write = rule.Payload if rule.Type in ("DomainFull", "IPCIDR", "IPCIDR6") else f".{rule.Payload}"
                to_write = f"+{to_write}\n" if (target == "text-plus"
                                                and rule.Type == "DomainSuffix"
                                                ) else f"{to_write}\n"
                dist.writelines(to_write)
        elif target in ("surge-compatible", "clash-compatible", "yaml"):
            if target == "yaml":
                dist.writelines("payload:\n")
            for rule in src:
                if target == "yaml" and src.Type != "Combined":
                    to_write = f"+.{rule.Payload}" if rule.Type == "DomainSuffix" else rule.Payload
                else:
                    prefix = list(config.RULE_TYPE_CONVERSION.keys())[
                        list(config.RULE_TYPE_CONVERSION.values()).index(rule.Type)
                    ]  # Reverse lookup the conversion table
                    to_write = f"{prefix},{rule.Payload}"
                if target == "clash-compatible":
                    to_write += ",Policy"
                if rule.Tag:
                    to_write += f",{rule.Tag}"
                if target == "yaml":
                    to_write = f"  - '{to_write}'"
                dist.writelines(f"{to_write}\n")
        elif target == "geosite":
            for rule in src:
                match rule.Type:
                    case "DomainSuffix":
                        dist.writelines(f"{rule.Payload}\n")
                    case "DomainFull":
                        dist.writelines(f"full:{rule.Payload}\n")
        elif target == "sing-ruleset":
            ruleset = {
                "version": 1,
                "rules": [{}]
            }
            for rule in src:
                if rule.Type == "DomainFull":
                    key = "domain"
                elif rule.Type == "DomainSuffix":
                    key = "domain_suffix"
                elif rule.Type in ("IPCIDR", "IPCIDR6"):
                    key = "ip_cidr"

                if key not in ruleset["rules"][0]:
                    ruleset["rules"][0][key] = []

                ruleset["rules"][0][key].append(rule.Payload)
            dist.write(dumps(ruleset, indent=2))


def batch_dump(src: RuleSet, targets: list, dst_path: Path, filename: str) -> None:
    for target in targets:
        if src.Type in ["IPCIDR", "Combined"] and target in ["text-plus", "geosite"] \
                or src.Type == "Combined" and target == "text":
            logging.warning(f'{filename}: Ignored unsupported type "{target}" for {src.Type} ruleset.')
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
                logging.debug(f'Rule "{rule}" added.')
            else:
                logging.warning(f"Already exist: {rule}")
        elif parsed_line[0] == "REM":
            if rule in src:
                src.remove(rule)
                logging.debug(f'Rule "{rule}" Removed.')
            else:
                logging.warning(f"Not found: {rule}")
    logging.info(f'Patch "{name + ".txt"}" applied.')
    return src


def sort(ruleset: RuleSet):
    if ruleset.Type == "Combined":
        logging.warning("Combined-type ruleset shouldn't be sorted as maybe ordered, skipped.")
        return

    def sort_key(item):
        match item.Type:
            # Domain suffixes should always in front of full domains
            # Shorter domains should in front of longer domains
            # For IPCIDR ruleset, default sort method is ok.
            case "DomainSuffix":
                sortkey = (0, len(item.Payload), item.Payload)
            case "DomainFull":
                sortkey = (1, len(item.Payload), item.Payload)
            case _:
                sortkey = item.Payload
        return sortkey

    ruleset.Payload.sort(key=sort_key)


def dedup(src: RuleSet) -> RuleSet:
    sort(src)
    list_unique = []
    for item in src:
        flag_unique = True
        for added in list_unique:
            if added.includes(item):
                flag_unique = False
                logging.debug(f"{item} is removed as duplicated with {added}.")
        if flag_unique:
            list_unique.append(item)
    src.Payload = list_unique
    return src
