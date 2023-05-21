from pathlib import Path

from abp.filters.parser import Filter


def custom_convert(src: Path) -> set:
    src_custom = open(src, mode="r").read().splitlines()
    set_converted = set()
    for line in src_custom:
        if line and not line.startswith("#"):
            set_converted.add(line)
    return set_converted


def is_ipaddr(str: str) -> bool:
    if str.count(".") != 3:
        return False
    for part in str.split("."):
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
        dist = open(dst, mode="w")
    except FileNotFoundError:
        dst.parent.mkdir(parents=True)
        dist = open(dst, mode="w")
    match target:
        case "text":
            for domain in src:
                if domain:
                    if domain.startswith("."):
                        dist.writelines(domain + "\n")
                    elif not domain.startswith("#"):
                        dist.writelines(domain + "\n")
        case "yaml":
            dist.writelines("payload:\n")
            for domain in src:
                if domain:
                    if domain.startswith("."):
                        dist.writelines("  - '+" + domain + "'\n")
                    elif not domain.startswith("#"):
                        dist.writelines("  - '" + domain + "'\n")
        case "surge-compatible":
            for domain in src:
                if domain:
                    if domain.startswith("."):
                        dist.writelines(domain.replace(".", "DOMAIN-SUFFIX,", 1) + "\n")
                    elif not domain.startswith("#"):
                        dist.writelines("DOMAIN," + domain + "\n")
        case "clash-compatible":
            for domain in src:
                if domain:
                    if domain.startswith("."):
                        dist.writelines(domain.replace(".", "DOMAIN-SUFFIX,", 1) + ",Policy\n")
                    elif not domain.startswith("#"):
                        dist.writelines("DOMAIN," + domain + ",Policy\n")
        case _:
            raise TypeError(
                "Target type unsupported, only accept 'text', 'yaml', 'surge-compatible' or 'clash-compatible'."
            )


def batch_dump(src: list, targets: list, dst_path: Path, filename: str) -> None:
    for target in targets:
        dump(src, target, dst_path/target/filename)


def set_to_sorted_list(src: set) -> list:
    list_sorted = [item for item in src]
    list_sorted.sort()
    return list_sorted
