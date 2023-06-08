import logging

from . import rule
from . import const


class Rule:
    def __init__(self):
        self.Type = None
        self.Payload = None
        self.Tag = None

    def type(self, rule_type):
        self.Type = rule_type

    def payload(self, payload):
        self.Payload = payload

    def tag(self, tag):
        self.Tag = tag

    def __str__(self):
        return f'Type: "{self.Type}", Payload: "{self.Payload}", Tag: "{self.Tag if self.Tag else ""}"'


def parse(src: set, excluded_import=None) -> set:
    excluded_import = [] if not excluded_import else excluded_import
    set_parsed = set()
    for raw_line in src:
        line = raw_line.split("#")[0].strip()
        if not line:
            continue
        parsed_rule = Rule()
        if "@" in line:
            parsed_rule.tag(line.split("@")[1])
            line = line.split(" @")[0]
        if ":" not in line:
            parsed_rule.type("Suffix")
            parsed_rule.payload(line)
        elif line.startswith("full:"):
            parsed_rule.type("Full")
            parsed_rule.payload(line.strip("full:"))
        elif line.startswith("include:"):
            name_import = line.split("include:")[1]
            if name_import not in excluded_import:
                logging.debug(f'Line "{raw_line}" is a import rule. Start importing "{name_import}".')
                src_import = set(
                    open(const.PATH_DOMAIN_LIST/name_import, mode="r", encoding="utf-8").read().splitlines())
                set_parsed |= parse(src_import, excluded_import)
                logging.debug(f'Imported "{name_import}".')
                continue
            else:
                logging.debug(f'Line "{raw_line}" is a import rule, but hit exclusion "{name_import}", skipped.')
                continue
        else:
            logging.debug(f'Unsupported rule: "{raw_line}", skipped.')
            continue
        set_parsed.add(parsed_rule)
        logging.debug(f"Line {raw_line} is parsed: {parsed_rule}")
    return set_parsed


def convert(src: set, excluded_tag=None) -> set:
    excluded_tag = [] if not excluded_tag else excluded_tag
    set_converted = set()
    for input_rule in src:
        if input_rule.Tag not in excluded_tag:
            if input_rule.Type == "Suffix":
                set_converted.add("." + input_rule.Payload)
            elif input_rule.Type == "Full":
                set_converted.add(input_rule.Payload)
    return set_converted


def batch_convert(categories: list, tools: list, exclusions=None) -> None:
    exclusions = [] if not exclusions else exclusions
    for tool in tools:
        for category in categories:
            src_geosite = set(open(const.PATH_DOMAIN_LIST/category, mode="r", encoding="utf-8").read().splitlines())
            set_geosite = convert(parse(src_geosite, exclusions))
            list_geosite_sorted = rule.set_to_sorted_list(set_geosite)
            rule.dump(list_geosite_sorted, tool, const.PATH_DIST/tool/(category + ".txt"))
