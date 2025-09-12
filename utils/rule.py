# noinspection PyProtectedMember
from abp.filters.parser import Filter


def is_ipv4addr(addr: str) -> bool:
    parts = addr.split(".")
    if len(parts) != 4:
        return False
    return all(
        part.isdigit() and 0 <= int(part) <= 255 
        for part in parts
    )


def is_domain(addr: str) -> bool:
    blacklist_chars = frozenset("/,*=~?#,: ()[]|@^")
    if (any(char in blacklist_chars for char in addr)
            or addr.startswith("-")
            or addr.endswith(".")
            or addr.endswith("-")
            or is_ipv4addr(addr)):
        return False
    return True


def strip_adblock(filter_to_strip: Filter) -> str | None:
    if (filter_to_strip.type != "filter"
            or filter_to_strip.selector["type"] != "url-pattern"
            or filter_to_strip.options and filter_to_strip.options not in (
                [("all", True)],
                [("document", True)],
                [("popup", True)]
            )
            or filter_to_strip.text.startswith("^")):
        return
    stripped = filter_to_strip.selector["value"].strip("@").strip("|").strip("^")
    if is_domain(stripped):
        return stripped
    return
