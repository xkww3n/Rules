from pathlib import Path

from abp.filters.parser import Filter


class Rule:
    Type: str
    Payload: str
    Tag: str

    def __init__(self, content_type: str = "", payload: str = "", tag: str = ""):
        self.Type = content_type
        self.Payload = payload
        self.Tag = tag

    def __str__(self):
        return f'Type: "{self.Type}", Payload: "{self.Payload}", Tag: {self.Tag if self.Tag else "NONE"}'


def custom_convert(src: Path) -> set:
    src_custom = open(src, mode="r", encoding="utf-8").read().splitlines()
    set_converted = set()
    for line in src_custom:
        if line.startswith("."):
            set_converted.add(Rule("DomainSuffix", line.strip(".")))
        elif line and not line.startswith("#"):
            set_converted.add(Rule("DomainFull", line))
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
                if rule.Type == "DomainSuffix":
                    dist.writelines(f"DOMAIN-SUFFIX,{rule.Payload}\n")
                elif rule.Type == "DomainFull":
                    dist.writelines(f"DOMAIN,{rule.Payload}\n")
                elif rule.Type == "IPCIDR":
                    dist.writelines(f"IP-CIDR,{rule.Payload}\n")
                elif rule.Type == "IPCIDR6":
                    dist.writelines(f"IP-CIDR6,{rule.Payload}\n")
        case "clash-compatible":
            for rule in src:
                if rule.Type == "DomainSuffix":
                    dist.writelines(f"DOMAIN-SUFFIX,{rule.Payload},Policy\n")
                elif rule.Type == "DomainFull":
                    dist.writelines(f"DOMAIN,{rule.Payload},Policy\n")
                elif rule.Type == "IPCIDR":
                    dist.writelines(f"IP-CIDR,{rule.Payload},Policy\n")
                elif rule.Type == "IPCIDR6":
                    dist.writelines(f"IP-CIDR6,{rule.Payload},Policy\n")
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
