import logging

from models.rule import Rule


class RuleSet:
    _type: str  # Domain / IPCIDR / Combined
    _payload: list[Rule]

    def __init__(self, ruleset_type: str, payload: list):
        self._type = ""
        self._payload = []
        if ruleset_type:
            self.type = ruleset_type
        if payload:
            self.payload = payload

    def __hash__(self):
        return hash((self._type, tuple(self._payload)))

    def __eq__(self, other):
        # noinspection PyProtectedMember
        return self._type == other._type and self._payload == other._payload

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
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, ruleset_type: str):
        allowed_types = ("Domain", "IPCIDR", "Combined")
        if ruleset_type not in allowed_types:
            raise TypeError(f"Unsupported type: {ruleset_type}")
        self._type = ruleset_type

    @property
    def payload(self) -> list:
        return self._payload

    @payload.setter
    def payload(self, payload: list):
        if self._type == "Domain":
            for item in payload:
                # noinspection PyProtectedMember
                if "Domain" not in item._type:
                    # noinspection PyProtectedMember
                    raise ValueError(f"{item._type}-type rule found in a domain-type ruleset.")
        elif self._type == "IPCIDR":
            for item in payload:
                # noinspection PyProtectedMember
                if "IPCIDR" not in item._type:
                    # noinspection PyProtectedMember
                    raise ValueError(f"{item._type}-type rule found in a IPCIDR-type ruleset.")
        self._payload = payload

    def deepcopy(self):
        ruleset_copied = RuleSet(self._type, [])
        payload_copied = []
        for rule in self._payload:
            rule_copied = Rule()
            rule_copied._type = rule.type
            rule_copied._payload = rule.payload
            rule_copied._tag = rule.tag
            payload_copied.append(rule_copied)
        ruleset_copied._payload = payload_copied
        return ruleset_copied

    def add(self, rule):
        if rule not in self._payload:
            self._payload.append(rule)

    def remove(self, rule):
        self._payload.remove(rule)

    def sort(self):
        if self._type == "Combined":
            logging.warning("Skipped: Combined-type ruleset shouldn't be sorted as maybe ordered.")
            return

        # noinspection PyProtectedMember
        def sort_key(item: Rule) -> tuple:
            match item._type:
                # Domain suffixes should always in front of full domains
                # Shorter domains should in front of longer domains
                # For IPCIDR ruleset, default sort method is ok.
                case "DomainSuffix":
                    sortkey = (0, len(item._payload), item._payload)
                case "DomainFull":
                    sortkey = (1, len(item._payload), item._payload)
                case _:
                    sortkey = (2, len(item._payload), item._payload)
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
