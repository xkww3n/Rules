from models.rule import Rule


class RuleSet:
    Type: str  # Domain / IPCIDR / Combined
    Payload: list[Rule]

    def __init__(self, ruleset_type: str, payload: list):
        if ruleset_type or payload:
            self.set_type(ruleset_type)
            self.set_payload(payload)
        else:
            self.Type = ""
            self.Payload = []

    def __hash__(self):
        return hash(self.Type) + hash(self.Payload)

    def __eq__(self, other):
        return self.Type == other.Type and self.Payload == other.Payload

    def __len__(self):
        return len(self.Payload)

    def __or__(self, other):
        for rule in other.Payload:
            if rule not in self.Payload:
                self.Payload.append(rule)
        return self

    def __contains__(self, item):
        return item in self.Payload

    def __iter__(self):
        return iter(self.Payload)

    def set_type(self, ruleset_type):
        allowed_type = ("Domain", "IPCIDR", "Combined")
        if ruleset_type not in allowed_type:
            raise TypeError(f"Unsupported type: {ruleset_type}")
        self.Type = ruleset_type

    def set_payload(self, payload):
        match self.Type:
            case "Domain":
                for item in payload:
                    if "Domain" not in item.Type:
                        raise ValueError(f"{item.Type}-type rule found in a domain-type ruleset.")
            case "IPCIDR":
                for item in payload:
                    if "IPCIDR" not in item.Type:
                        raise ValueError(f"{item.Type}-type rule found in a IPCIDR-type ruleset.")
        self.Payload = payload

    def deepcopy(self):
        ruleset_copied = RuleSet(self.Type, [])
        payload_copied = []
        for rule in self.Payload:
            rule_copied = Rule()
            rule_copied.Type = rule.Type
            rule_copied.Payload = rule.Payload
            rule_copied.Tag = rule.Tag
            payload_copied.append(rule_copied)
        ruleset_copied.Payload = payload_copied
        return ruleset_copied

    def add(self, rule):
        if rule not in self.Payload:
            self.Payload.append(rule)

    def remove(self, rule):
        self.Payload.remove(rule)
