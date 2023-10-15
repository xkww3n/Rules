import logging
from pathlib import Path

from abp.filters.parser import Filter

from . import const


class Rule:
    Type: str
    Payload: str
    Tag: str

    def __init__(self, content_type: str = "", payload: str = "", tag: str = ""):
        self.Type = content_type  # DomainSuffix / DomainFull / IPCIDR / IPCIDR6 / Classic
        self.Payload = payload
        self.Tag = tag

    def __str__(self):
        return f'Type: "{self.Type}", Payload: "{self.Payload}", Tag: {self.Tag if self.Tag else "NONE"}'

    def __hash__(self):
        return hash(("type" + self.Type, "payload" + self.Payload, "tag" + self.Tag))

    def __eq__(self, other):
        return self.Type == other.Type and self.Payload == other.Payload and self.Tag == other.Tag


def custom_convert(src: Path) -> set:
    src_custom = open(src, mode="r", encoding="utf-8").read().splitlines()
    set_converted = set()
    try:
        rule_type = src_custom[0].split("#@@TYPE:")[1]
    except IndexError:
        logging.warning(f"File {src} doesn't have a valid type header, treat as domain type.")
        rule_type = "DOMAIN"
    for line in src_custom:
        if rule_type == "DOMAIN":
            if line.startswith("."):
                set_converted.add(Rule("DomainSuffix", line.strip(".")))
            elif line and not line.startswith("#"):
                set_converted.add(Rule("DomainFull", line))
        elif rule_type == "IP":
            if line and not line.startswith("#"):
                set_converted.add(Rule("IPCIDR", line))
        elif rule_type == "CLASSIC":
            if line and not line.startswith("#"):
                set_converted.add(Rule("Classic", line))
    return set_converted


def is_ipaddr(addr: str) -> bool:
    if addr.count(".") != 3:
        return False
    for part in addr.split("."):
        if not part.isdigit():
            return False
        i = int(part)
        if i < 0 or i > 255:
            return False
    return True


def is_domain(rule: Filter) -> bool:
    if (
            rule.type == "filter"
            and rule.selector["type"] == "url-pattern"
            and "." in rule.text
            and "/" not in rule.text
            and "*" not in rule.text
            and "=" not in rule.text
            and "~" not in rule.text
            and "?" not in rule.text
            and "#" not in rule.text
            and "," not in rule.text
            and ":" not in rule.text
            and " " not in rule.text
            and ("(" or ")") not in rule.text
            and not rule.text.startswith("_")
            and not rule.text.startswith("-")
            and not rule.text.startswith("^")
            and not rule.text.startswith("[")
            and not rule.text.endswith(".")
            and not rule.text.endswith("_")
            and not rule.text.endswith("]")
            and not rule.text.endswith(";")
            and not rule.options
            and not is_ipaddr(rule.text.strip("||").strip("^"))
    ):
        return True
    else:
        return False


def dump(src: list, target: str, dst: Path) -> None:
    try:
        dist = open(dst, mode="w", encoding="utf-8")
    except FileNotFoundError:
        dst.parent.mkdir(parents=True)
        dist = open(dst, mode="w")
    match target:
        case "text":
            for rule in src:
                if rule.Type == "DomainSuffix":
                    dist.writelines(f".{rule.Payload}\n")
                elif rule.Type == "DomainFull" or "IPCIDR" or "IPCIDR6" or "Classic":
                    dist.writelines(f"{rule.Payload}\n")
                else:
                    raise TypeError(f'Unsupported rule type "{rule.Type}". File: {dst}.')
        case "text-plus":
            for rule in src:
                if rule.Type == "DomainSuffix":
                    dist.writelines(f"+.{rule.Payload}\n")
                elif rule.Type == "DomainFull" or "IPCIDR" or "IPCIDR6" or "Classic":
                    dist.writelines(f"{rule.Payload}\n")
                else:
                    raise TypeError(f'Unsupported rule type "{rule.Type}". File: {dst}.')
        case "yaml":
            dist.writelines("payload:\n")
            for rule in src:
                if rule.Type == "DomainSuffix":
                    dist.writelines(f"  - '+.{rule.Payload}'\n")
                elif rule.Type == "DomainFull" or "IPCIDR" or "IPCIDR6" or "Classic":
                    dist.writelines(f"  - '{rule.Payload}'\n")
                else:
                    raise TypeError(f'Unsupported rule type "{rule.Type}". File: {dst}.')
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
                    case "Classic":
                        dist.writelines(f"{rule.Payload}\n")
                    case _:
                        raise TypeError(f'Unsupported rule type "{rule.Type}". File: {dst}.')
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
                    case "Classic":
                        dist.writelines(f"{rule.Payload},Policy\n")
                    case _:
                        raise TypeError(f'Unsupported rule type "{rule.Type}". File: {dst}.')
        case _:
            raise TypeError("Target type unsupported, "
                            "only accept 'text', 'text-plus', 'yaml', 'surge-compatible' or 'clash-compatible'."
                            )


def batch_dump(src: list, targets: list, dst_path: Path, filename: str) -> None:
    for target in targets:
        dump(src, target, dst_path/target/filename)


def set_to_sorted_list(src: set) -> list:
    list_sorted = [item for item in src]
    list_sorted.sort(key=lambda item: str(item))
    return list_sorted


def apply_patch(src: set, name: str) -> set:
    try:
        patch = open(const.PATH_SOURCE_PATCH/(name + ".txt"), mode="r").read().splitlines()
    except FileNotFoundError:
        logging.warning(f'Patch "{name + ".txt"}" not found.')
        return src
    logging.info(f'Start applying patch "{name + ".txt"}"')
    for line in patch:
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
