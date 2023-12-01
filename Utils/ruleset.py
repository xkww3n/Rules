import logging
from copy import deepcopy
from json import dumps
from pathlib import Path

from .rule import Rule
from . import const


class RuleSet:
    Type: str  # Domain / IPCIDR / Combined
    Payload: list[Rule]

    def __init__(self, ruleset_type: str, payload: list):
        if ruleset_type or payload:
            self.set_type(ruleset_type)
            self.set_payload(payload)
        else:
            self.Type = ""
            self.Payload = []

    def __hash__(self):
        return hash(self.Type) + hash(self.Payload)

    def __eq__(self, other):
        return self.Type == other.Type and self.Payload == other.Payload

    def __len__(self):
        return len(self.Payload)

    def __or__(self, other):
        for rule in other.Payload:
            if rule not in self.Payload:
                self.Payload.append(rule)
        return self

    def __contains__(self, item):
        return item in self.Payload

    def __iter__(self):
        return iter(self.Payload)

    def set_type(self, ruleset_type):
        allowed_type = ("Domain", "IPCIDR", "Combined")
        if ruleset_type not in allowed_type:
            raise TypeError(f"Unsupported type: {ruleset_type}")
        self.Type = ruleset_type

    def set_payload(self, payload):
        match self.Type:
            case "Domain":
                for item in payload:
                    if "Domain" not in item.Type:
                        raise ValueError(f"{item.Type}-type rule found in a domain-type ruleset.")
            case "IPCIDR":
                for item in payload:
                    if "IPCIDR" not in item.Type:
                        raise ValueError(f"{item.Type}-type rule found in a IPCIDR-type ruleset.")
        self.Payload = payload

    def deepcopy(self):
        return deepcopy(self)

    def add(self, rule):
        self.Payload.append(rule)

    def remove(self, rule):
        self.Payload.remove(rule)

    def sort(self):
        if self.Type == "Combined":
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

        self.Payload.sort(key=sort_key)

    def dedup(self):
        self.sort()
        list_unique = []
        for item in self:
            flag_unique = True
            for added in list_unique:
                if added.includes(item):
                    flag_unique = False
                    logging.debug(f"{item} is removed as duplicated with {added}.")
            if flag_unique:
                list_unique.append(item)
        self.Payload = list_unique


def load(src: Path) -> RuleSet:
    src_toload = open(src, mode="r", encoding="utf-8").read().splitlines()
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
                            ruleset_loaded.add(Rule("IPCIDR", parsed[1]))
                        case "IP-CIDR6":
                            ruleset_loaded.add(Rule("IPCIDR6", parsed[1]))
                        case _:
                            raise ValueError()
    return ruleset_loaded


def dump(src: RuleSet, target: str, dst: Path, filename: str) -> None:
    match target:
        case "yaml":
            filename = filename + ".yaml"
        case "geosite":
            filename = filename
        case "sing-ruleset":
            filename = filename + ".json"
        case _:
            filename = filename + ".txt"
    try:
        dist = open(dst/filename, mode="w", encoding="utf-8")
    except FileNotFoundError:
        dst.mkdir(parents=True)
        dist = open(dst/filename, mode="w", encoding="utf-8")
    match target:
        case "text":
            for rule in src:
                if rule.Type == "DomainSuffix":
                    dist.writelines(f".{rule.Payload}\n")
                elif rule.Type == "DomainFull" or "IPCIDR" or "IPCIDR6":
                    dist.writelines(f"{rule.Payload}\n")
        case "text-plus":
            for rule in src:
                if rule.Type == "DomainSuffix":
                    dist.writelines(f"+.{rule.Payload}\n")
                elif rule.Type == "DomainFull" or "IPCIDR" or "IPCIDR6":
                    dist.writelines(f"{rule.Payload}\n")
        case "yaml":
            dist.writelines("payload:\n")
            for rule in src:
                if rule.Type == "DomainSuffix":
                    dist.writelines(f"  - '+.{rule.Payload}'\n")
                elif rule.Type == "DomainFull" or "IPCIDR" or "IPCIDR6":
                    dist.writelines(f"  - '{rule.Payload}'\n")
        case "surge-compatible":
            for rule in src:
                match rule.Type:
                    case "DomainSuffix":
                        dist.writelines(f"DOMAIN-SUFFIX,{rule.Payload}\n")
                    case "DomainFull":
                        dist.writelines(f"DOMAIN,{rule.Payload}\n")
                    case "IPCIDR":
                        dist.writelines(f"IP-CIDR,{rule.Payload}\n")
                    case "IPCIDR6":
                        dist.writelines(f"IP-CIDR6,{rule.Payload}\n")
        case "clash-compatible":
            for rule in src:
                match rule.Type:
                    case "DomainSuffix":
                        dist.writelines(f"DOMAIN-SUFFIX,{rule.Payload},Policy\n")
                    case "DomainFull":
                        dist.writelines(f"DOMAIN,{rule.Payload},Policy\n")
                    case "IPCIDR":
                        dist.writelines(f"IP-CIDR,{rule.Payload},Policy\n")
                    case "IPCIDR6":
                        dist.writelines(f"IP-CIDR6,{rule.Payload},Policy\n")
        case "geosite":
            for rule in src:
                match rule.Type:
                    case "DomainSuffix":
                        dist.writelines(f"{rule.Payload}\n")
                    case "DomainFull":
                        dist.writelines(f"full:{rule.Payload}\n")
                    case _:
                        raise TypeError(f'Unsupported rule type "{rule.Type}". File: {dst}.')
        case "sing-ruleset":
            ruleset = {
                "version": 1,
                "rules": [
                    {}
                ]
            }
            match src.Type:
                case "Domain":
                    for rule in src:
                        match rule.Type:
                            case "DomainSuffix":
                                if "domain_suffix" not in ruleset["rules"][0]:
                                    ruleset["rules"][0]["domain_suffix"] = []
                                ruleset["rules"][0]["domain_suffix"].append(f".{rule.Payload}")
                            case "DomainFull":
                                if "domain" not in ruleset["rules"][0]:
                                    ruleset["rules"][0]["domain"] = []
                                ruleset["rules"][0]["domain"].append(rule.Payload)
                    dist.write(dumps(ruleset, indent=2))
                case "IPCIDR":
                    for rule in src:
                        if "ip_cidr" not in ruleset["rules"][0]:
                            ruleset["rules"][0]["ip_cidr"] = []
                        ruleset["rules"][0]["ip_cidr"].append(rule.Payload)
                    dist.write(dumps(ruleset, indent=2))
                case "Combined":
                    for rule in src:
                        match rule.Type:
                            case "DomainFull":
                                if "domain" not in ruleset["rules"][0]:
                                    ruleset["rules"][0]["domain"] = []
                                ruleset["rules"][0]["domain"].append(rule.Payload)
                            case "DomainSuffix":
                                if "domain_suffix" not in ruleset["rules"][0]:
                                    ruleset["rules"][0]["domain_suffix"] = []
                                ruleset["rules"][0]["domain_suffix"].append(f".{rule.Payload}")
                            case "IPCIDR":
                                if "ip_cidr" not in ruleset["rules"][0]:
                                    ruleset["rules"][0]["ip_cidr"] = []
                                ruleset["rules"][0]["ip_cidr"].append(rule.Payload)
                    dist.write(dumps(ruleset, indent=2))
        case _:
            raise TypeError("Target type unsupported.")


def batch_dump(src: RuleSet, targets: list, dst_path: Path, filename: str) -> None:
    targets = deepcopy(targets)
    if src.Type == "IPCIDR":
        if all(t in targets for t in ["text", "text-plus"]):
            logging.info(f"{filename}: Ignored unsupported type for combined ruleset.")
            targets.remove("text-plus")
        if "geosite" in targets:
            logging.warning(f"{filename}: {src.Type}-type ruleset can't be exported to GeoSite source, ignored.")
            targets.remove("geosite")
    if src.Type == "Combined" and any(t in targets for t in ["text", "text-plus", "yaml", "geosite"]):
        logging.info(f"{filename}: Ignored unsupported type for combined ruleset.")
        if "text" in targets:
            targets.remove("text")
        if "text-plus" in targets:
            targets.remove("text-plus")
        if "yaml" in targets:
            targets.remove("yaml")
        if "geosite" in targets:
            targets.remove("geosite")
    for target in targets:
        dump(src, target, dst_path/target, filename)


def patch(src: RuleSet, name: str, override_patch_loc: Path = Path("")) -> RuleSet:
    try:
        if override_patch_loc != Path(""):
            loaded_patch = open(override_patch_loc/(name + ".txt"), mode="r").read().splitlines()
        else:
            loaded_patch = open(const.PATH_SOURCE_PATCH/(name + ".txt"), mode="r").read().splitlines()
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
