from pathlib import Path

from abp.filters.parser import Filter


def custom_convert(src: Path) -> set:
    src_custom = open(src, mode="r", encoding="utf-8").read().splitlines()
    set_converted = set()
    for line in src_custom:
        if line and not line.startswith("#"):
            set_converted.add(line)
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


def dump(content_type: str, src: list, target: str, dst: Path) -> None:
    try:
        dist = open(dst, mode="w", encoding="utf-8")
    except FileNotFoundError:
        dst.parent.mkdir(parents=True)
        dist = open(dst, mode="w")
    match target:
        case "text":
            for line in src:
                if line:
                    if line.startswith("."):
                        dist.writelines(line + "\n")
                    elif not line.startswith("#"):
                        dist.writelines(line + "\n")
        case "text-plus":
            for line in src:
                if line:
                    if line.startswith("."):
                        dist.writelines("+" + line + "\n")
                    elif not line.startswith("#"):
                        dist.writelines(line + "\n")
        case "yaml":
            dist.writelines("payload:\n")
            for line in src:
                if line:
                    if line.startswith("."):
                        dist.writelines("  - '+" + line + "'\n")
                    elif not line.startswith("#"):
                        dist.writelines("  - '" + line + "'\n")
        case "surge-compatible":
            for line in src:
                if line:
                    if content_type == "domain":
                        if line.startswith("."):
                            dist.writelines(line.replace(".", "DOMAIN-SUFFIX,", 1) + "\n")
                        elif not line.startswith("#"):
                            dist.writelines("DOMAIN," + line + "\n")
                    elif content_type == "ipcidr":
                        if not line.startswith("#"):
                            dist.writelines("IP-CIDR," + line + "\n")
        case "clash-compatible":
            for line in src:
                if line:
                    if content_type == "domain":
                        if line.startswith("."):
                            dist.writelines(line.replace(".", "DOMAIN-SUFFIX,", 1) + ",Policy\n")
                        elif not line.startswith("#"):
                            dist.writelines("DOMAIN," + line + ",Policy\n")
                    elif content_type == "ipcidr":
                        if not line.startswith("#"):
                            dist.writelines("IP-CIDR," + line + ",Policy\n")
        case _:
            raise TypeError("Target type unsupported, "
                            "only accept 'text', 'text-plus', 'yaml', 'surge-compatible' or 'clash-compatible'."
                            )


def batch_dump(content_type: str, src: list, targets: list, dst_path: Path, filename: str) -> None:
    for target in targets:
        dump(content_type, src, target, dst_path/target/filename)


def set_to_sorted_list(src: set) -> list:
    list_sorted = [item for item in src]
    list_sorted.sort()
    return list_sorted
