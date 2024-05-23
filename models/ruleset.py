from models.rule import Rule


class RuleSet:
    _type: str  # Domain / IPCIDR / Combined
    _payload: list[Rule]

    def __init__(self, ruleset_type: str, payload: list):
        self._type = ""
        self._payload = []
        if ruleset_type or payload:
            self.type = ruleset_type
            self.payload = payload

    def __hash__(self):
        return hash((self.type, self.payload))

    def __eq__(self, other):
        return self.type == other.type and self.payload == other.payload

    def __len__(self):
        return len(self.payload)

    def __or__(self, other):
        for rule in other.payload:
            if rule not in self.payload:
                self.payload.append(rule)
        return self

    def __contains__(self, item):
        return item in self.payload

    def __iter__(self):
        return iter(self.payload)

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
        match self.type:
            case "Domain":
                for item in payload:
                    if "Domain" not in item.type:
                        raise ValueError(f"{item.type}-type rule found in a domain-type ruleset.")
            case "IPCIDR":
                for item in payload:
                    if "IPCIDR" not in item.type:
                        raise ValueError(f"{item.type}-type rule found in a IPCIDR-type ruleset.")
        self._payload = payload

    def deepcopy(self):
        ruleset_copied = RuleSet(self.type, [])
        payload_copied = []
        for rule in self.payload:
            rule_copied = Rule()
            rule_copied.type = rule.type
            rule_copied.payload = rule.payload
            rule_copied.tag = rule.tag
            payload_copied.append(rule_copied)
        ruleset_copied.payload = payload_copied
        return ruleset_copied

    def add(self, rule):
        if rule not in self.payload:
            self.payload.append(rule)

    def remove(self, rule):
        self.payload.remove(rule)
