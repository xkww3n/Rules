# noinspection PyProtectedMember
from abp.filters.parser import parse_filterlist

DOMAIN_BLACKLIST_CHARS = frozenset("/,*=~?#,: ()[]|@^")
ADBLOCK_UNSUPPORTED_CHARS = frozenset("*,=~? ()[]")
ADBLOCK_ALLOWED_OPTIONS = {"all", "document", "popup"}


def is_ipv4addr(addr: str) -> bool:
    parts = addr.split(".")
    if len(parts) != 4:
        return False
    return all(
        part.isdigit() and 0 <= int(part) <= 255 
        for part in parts
    )


def is_domain(addr: str) -> bool:
    if (not DOMAIN_BLACKLIST_CHARS.isdisjoint(addr)
            or addr.startswith(("-", "_"))
            or addr.endswith((".", "-", "_"))
            or addr.count(".") == 3 and addr[0].isdigit() and is_ipv4addr(addr)):
        return False
    return True


def parse_adblock_domain_rules(lines: list[str], psl: set[str]) -> tuple[int, list[tuple[str, str, str, bool]]]:
    filtered_lines = []
    skipped_count = 0
    for line in lines:
        stripped = line.strip()
        if (not stripped
                or stripped.startswith(("!", "#", "^", "/"))
                or "##" in stripped
                or "#@#" in stripped
                or "#$#" in stripped
                or not ADBLOCK_UNSUPPORTED_CHARS.isdisjoint(stripped)
                or "/" in stripped and "://" not in stripped):
            skipped_count += 1
            continue

        if "$" in stripped and stripped.split("$", 1)[1] not in ADBLOCK_ALLOWED_OPTIONS:
            skipped_count += 1
            continue

        filtered_lines.append(line)

    rules = []
    for parsed_filter in parse_filterlist(filtered_lines):
        if (parsed_filter.type != "filter"
                or parsed_filter.selector["type"] != "url-pattern"
                or parsed_filter.text.startswith("^")):
            continue

        domain = parsed_filter.selector["value"].strip("@").strip("|").strip("^")
        if not is_domain(domain):
            continue
        domain = domain.strip(".")

        include_subdomains = domain.count(".") <= 2
        if not include_subdomains:
            # Only suffixes starting within the first three labels can reduce the level to two.
            first_dot = domain.index(".")
            second_dot = domain.index(".", first_dot + 1)
            include_subdomains = (
                f".{domain}" in psl or domain[first_dot:] in psl or domain[second_dot:] in psl
            )
        rules.append((parsed_filter.action, parsed_filter.text, domain, include_subdomains))

    return skipped_count, rules
