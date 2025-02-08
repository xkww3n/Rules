# noinspection PyProtectedMember
from abp.filters.parser import Filter


def is_ipv4addr(addr: str) -> bool:
    if addr.count(".") != 3:
        return False
    for part in addr.split("."):
        if not part.isdigit():
            return False
        i = int(part)
        if i < 0 or i > 255:
            return False
    return True


def is_domain(addr: str) -> bool:
    blacklist_include = {"/", "*", "=", "~", "?", "#", ",", ":", " ", "(", ")", "[", "]", "|", "@", "^"}
    if (any(bl_char in addr for bl_char in blacklist_include)
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
