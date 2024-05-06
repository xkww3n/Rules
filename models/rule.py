from ipaddress import ip_network, IPv4Network, IPv6Network

from utils.rule import is_domain


class Rule:
    Type: str  # DomainSuffix / DomainFull / IPCIDR / IPCIDR6
    Payload: str
    Tag: str

    def __init__(self, rule_type: str = "", payload: str = "", tag: str = ""):
        if rule_type or payload:
            self.set_type(rule_type)
            self.set_payload(payload)
            self.set_tag(tag)
        else:
            self.Type = ""
            self.Payload = ""
            self.Tag = tag

    def __str__(self):
        return f'{self.Type}: {self.Payload}{f" ({self.Tag})" if self.Tag else ""}'

    def __hash__(self):
        return hash((self.Type, self.Payload, self.Tag))

    def __eq__(self, other):
        return self.Type == other.Type and self.Payload == other.Payload and self.Tag == other.Tag

    def set_type(self, rule_type: str):
        allowed_type = ("DomainSuffix", "DomainFull", "IPCIDR", "IPCIDR6")
        if rule_type not in allowed_type:
            raise TypeError(f"Unsupported type: {rule_type}")
        self.Type = rule_type

    def set_payload(self, payload: str):
        if "Domain" in self.Type:
            if not is_domain(payload):
                raise ValueError(f"Invalid domain: {payload}")
        elif "IP" in self.Type:
            try:
                ip_type = ip_network(payload)
            except ValueError:
                raise ValueError(f"Invalid IP address: {payload}")
            if self.Type == "IPCIDR6" and type(ip_type) is IPv4Network:
                raise ValueError(f"IPv4 address stored in IPv6 type: {payload}")
            elif self.Type == "IPCIDR" and type(ip_type) is IPv6Network:
                raise ValueError(f"IPv6 address stored in IPv4 type: {payload}")
        self.Payload = payload

    def set_tag(self, tag: str = ""):
        self.Tag = tag

    def includes(self, other):
        if self.Type == "DomainSuffix":
            if self.Payload == other.Payload:
                return True
            return other.Payload.endswith("." + self.Payload)
        elif self.Type == "DomainFull":
            return self == other
