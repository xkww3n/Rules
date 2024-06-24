import logging
from enum import Enum

from models.rule import Rule, RuleType


class RuleSetType(Enum):
    Domain = 1
    IPCIDR = 2
    Combined = 3


class RuleSet:
    type: RuleSetType
    _payload: list[Rule]

    def __init__(self, ruleset_type: RuleSetType, payload: list):
        self.type = ruleset_type
        self._payload = payload

    def __hash__(self):
        return hash((self.type, tuple(self._payload)))

    def __eq__(self, other):
        # noinspection PyProtectedMember
        return self.type == other.type and self._payload == other._payload

    def __len__(self):
        return len(self._payload)

    def __or__(self, other):
        payload_set = set(self._payload)
        # noinspection PyProtectedMember
        for rule in other._payload:
            if rule not in payload_set:
                self._payload.append(rule)
                payload_set.add(rule)
        return self

    def __contains__(self, item):
        return item in self._payload

    def __iter__(self):
        return iter(self._payload)

    @property
    def payload(self) -> list:
        return self._payload

    @payload.setter
    def payload(self, payload: list):
        if self.type == RuleSetType.Domain:
            for item in payload:
                if item.type not in {RuleType.DomainSuffix, RuleType.DomainFull}:
                    raise ValueError(f"{item.type.value} rule found in a domain-type ruleset.")
        elif self.type == RuleSetType.IPCIDR:
            for item in payload:
                if item.type not in {RuleType.IPCIDR, RuleType.IPCIDR6}:
                    raise ValueError(f"{item.type.value} rule found in a IPCIDR-type ruleset.")
        self._payload = payload

    def deepcopy(self):
        ruleset_copied = RuleSet(self.type, [])
        payload_copied = []
        for rule in self._payload:
            rule_copied_type = rule.type
            rule_copied_payload = rule.payload
            rule_copied_tag = rule.tag
            rule_copied = Rule(rule_copied_type, rule_copied_payload, rule_copied_tag)
            payload_copied.append(rule_copied)
        ruleset_copied._payload = payload_copied
        return ruleset_copied

    def add(self, rule):
        if rule not in self._payload:
            self._payload.append(rule)

    def remove(self, rule):
        self._payload.remove(rule)

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

        self._payload.sort(key=sort_key)

    def dedup(self):
        self.sort()
        list_unique = []
        for item in self._payload:
            flag_unique = True
            for added in list_unique:
                if added.includes(item):
                    flag_unique = False
                    logging.debug(f'Remove "{item}": included in "{added}".')
            if flag_unique:
                list_unique.append(item)
        self._payload = list_unique
