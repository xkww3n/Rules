import logging
from enum import Enum

from models.rule import Rule, RuleType


class RuleSetType(Enum):
    Domain = 1
    IPCIDR = 2
    Combined = 3


class RuleSet:
    type: RuleSetType
    payload: list[Rule]

    def __init__(self, ruleset_type: RuleSetType, payload: list):
        self.type = ruleset_type
        if self.type == RuleSetType.Domain:
            for item in payload:
                if item.type not in {RuleType.DomainSuffix, RuleType.DomainFull}:
                    raise ValueError(f"{item.type.value} rule found in a domain-type ruleset.")
        elif self.type == RuleSetType.IPCIDR:
            for item in payload:
                if item.type not in {RuleType.IPCIDR, RuleType.IPCIDR6}:
                    raise ValueError(f"{item.type.value} rule found in a IPCIDR-type ruleset.")
        self.payload = payload

    def __hash__(self):
        return hash((self.type, tuple(self.payload)))

    def __eq__(self, other):
        return self.type == other.type and self.payload == other.payload

    def __len__(self):
        return len(self.payload)

    def __or__(self, other):
        payload_set = set(self.payload)
        self.payload.extend(rule for rule in other.payload if rule not in payload_set)
        return self

    def __contains__(self, item):
        return item in self.payload

    def __iter__(self):
        return iter(self.payload)


    def add(self, rule):
        if rule not in self.payload:
            self.payload.append(rule)

    def remove(self, rule):
        self.payload.remove(rule)

    def sort(self):
        if self.type == RuleSetType.Combined:
            logging.warning("Skipped: Combined-type ruleset shouldn't be sorted as maybe ordered.")
            return

        def sort_key(item: Rule) -> tuple:
            match item.type:
                # Domain suffixes should always in front of full domains
                # Shorter domains should in front of longer domains
                # For IPCIDR ruleset, default sort method is ok.
                case RuleType.DomainSuffix:
                    sortkey = (0, len(item.payload), item.payload)
                case RuleType.DomainFull:
                    sortkey = (1, len(item.payload), item.payload)
                case _:
                    sortkey = (2, len(item.payload), item.payload)
            return sortkey

        self.payload.sort(key=sort_key)

    def dedup(self):
        self.sort()
        list_unique = []
        for item in self.payload:
            if not any(added.includes(item) for added in list_unique):
                list_unique.append(item)
            else:
                for added in list_unique:
                    if added.includes(item):
                        logging.debug(f'Remove "{item}": included in "{added}".')
                        break
        self.payload = list_unique
