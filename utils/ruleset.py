import logging
from copy import deepcopy
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
                if line and not line.startswith("#"):
                    if ":" in line:
                        ruleset_loaded.add(Rule("IPCIDR6", line))
                    else:
                        ruleset_loaded.add(Rule("IPCIDR", line))
        case "Combined":
            for line in src_toload:
                if line and not line.startswith("#"):
                    parsed = line.split(",")
                    match parsed[0]:
                        case "DOMAIN":
                            ruleset_loaded.add(Rule("DomainFull", parsed[1]))
                        case "DOMAIN-SUFFIX":
                            ruleset_loaded.add(Rule("DomainSuffix", parsed[1]))
                        case "IP-CIDR":
                            if len(parsed) == 3:
                                parsed_rule = Rule("IPCIDR", parsed[1], parsed[2])
                            else:
                                parsed_rule = Rule("IPCIDR", parsed[1])
                            ruleset_loaded.add(parsed_rule)
                        case "IP-CIDR6":
                            if len(parsed) == 3:
                                parsed_rule = Rule("IPCIDR6", parsed[1], parsed[2])
                            else:
                                parsed_rule = Rule("IPCIDR6", parsed[1])
                            ruleset_loaded.add(parsed_rule)
                        case _:
                            raise ValueError()
    return ruleset_loaded


def dump(src: RuleSet, target: str, dst: Path, filename: str) -> None:
    if target not in config.TARGETS:
        raise TypeError("Invalid target.")
    match target:
        case "yaml":
            filename = filename + ".yaml"
        case "geosite":
            filename = filename
        case "sing-ruleset":
            filename = filename + ".json"
        case _:
            filename = filename + ".txt"
    dst.mkdir(parents=True, exist_ok=True)
    with open(dst/filename, mode="w", encoding="utf-8") as dist:
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
                    match rule.Type:
                        case "DomainSuffix":
                            to_write = f"DOMAIN-SUFFIX,{rule.Payload}"
                        case "DomainFull":
                            to_write = f"DOMAIN,{rule.Payload}"
                        case "IPCIDR":
                            to_write = f"IP-CIDR,{rule.Payload}"
                        case "IPCIDR6":
                            to_write = f"IP-CIDR6,{rule.Payload}"
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
                    if "domain" not in ruleset["rules"][0]:
                        ruleset["rules"][0]["domain"] = []
                    ruleset["rules"][0]["domain"].append(rule.Payload)
                elif rule.Type == "DomainSuffix":
                    if "domain_suffix" not in ruleset["rules"][0]:
                        ruleset["rules"][0]["domain_suffix"] = []
                    ruleset["rules"][0]["domain_suffix"].append(rule.Payload)
                elif rule.Type in ("IPCIDR", "IPCIDR6"):
                    if "ip_cidr" not in ruleset["rules"][0]:
                        ruleset["rules"][0]["ip_cidr"] = []
                    ruleset["rules"][0]["ip_cidr"].append(rule.Payload)
            dist.write(dumps(ruleset, indent=2))


def batch_dump(src: RuleSet, targets: list, dst_path: Path, filename: str) -> None:
    targets = deepcopy(targets)
    if src.Type == "IPCIDR":
        if all(t in targets for t in ["text", "text-plus"]):
            logging.info(f"{filename}: Ignored unsupported type for combined ruleset.")
            targets.remove("text-plus")
        if "geosite" in targets:
            logging.warning(f"{filename}: {src.Type}-type ruleset can't be exported to GeoSite source, ignored.")
            targets.remove("geosite")
    if src.Type == "Combined" and any(t in targets for t in ["text", "text-plus", "geosite"]):
        logging.info(f"{filename}: Ignored unsupported type for combined ruleset.")
        if "text" in targets:
            targets.remove("text")
        if "text-plus" in targets:
            targets.remove("text-plus")
        if "geosite" in targets:
            targets.remove("geosite")
    for target in targets:
        dump(src, target, dst_path/target, filename)


def patch(src: RuleSet, name: str, override_patch_loc: Path = Path("")) -> RuleSet:
    path_base = override_patch_loc if override_patch_loc != Path("") else config.PATH_SOURCE_PATCH
    try:
        loaded_patch = open(path_base/f"{name}.txt", mode="r", encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        logging.warning(f'Patch "{name + ".txt"}" not found.')
        return src
    logging.info(f'Start applying patch "{name + ".txt"}"')
    for line in loaded_patch:
        if line.startswith("#"):
            continue
        parsed_line = line.split(":")
        if parsed_line[0] == "ADD":
            if parsed_line[1].startswith("."):
                rule = Rule("DomainSuffix", parsed_line[1].strip("."))
            else:
                rule = Rule("DomainFull", parsed_line[1])
            if rule not in src:
                src.add(rule)
                logging.debug(f'Rule "{rule}" added.')
            else:
                logging.warning(f"Already exist: {rule}")
        elif parsed_line[0] == "REM":
            if parsed_line[1].startswith("."):
                rule = Rule("DomainSuffix", parsed_line[1].strip("."))
            else:
                rule = Rule("DomainFull", parsed_line[1])
            if rule in src:
                src.remove(rule)
                logging.debug(f'Rule "{rule}" Removed.')
            else:
                logging.warning(f"Not found: {rule}")
    logging.info(f'Patch "{name + ".txt"}" applied.')
    return src


def dedup(src: RuleSet) -> RuleSet:
    src.sort()
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
