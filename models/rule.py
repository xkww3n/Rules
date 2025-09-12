from enum import Enum
from ipaddress import ip_network, IPv4Network, IPv6Network

from utils.rule import is_domain


class RuleType(Enum):
    DomainSuffix = "DOMAIN-SUFFIX"
    DomainFull = "DOMAIN"
    IPCIDR = "IP-CIDR"
    IPCIDR6 = "IP-CIDR6"


class Rule:
    type: RuleType
    tag: str
    payload: str

    def __init__(self, rule_type: RuleType, payload: str = "", tag: str = ""):
        self.type = rule_type
        self.tag = tag

        if rule_type in {RuleType.DomainSuffix, RuleType.DomainFull}:
            if not is_domain(payload):
                raise ValueError(f"Invalid domain: {payload}")
        else:
            ip_type = ip_network(payload, strict=False)
            if rule_type == RuleType.IPCIDR6 and isinstance(ip_type, IPv4Network):
                raise ValueError(f"IPv4 address stored in IPv6 type: {payload}")
            elif rule_type == RuleType.IPCIDR and isinstance(ip_type, IPv6Network):
                raise ValueError(f"IPv6 address stored in IPv4 type: {payload}")
        
        self.payload = payload

    def __str__(self):
        return f'{self.type.name}: {self.payload}{f" ({self.tag})" if self.tag else ""}'

    def __hash__(self):
        return hash((self.type, self.tag, self.payload))

    def __eq__(self, other):
        return self.type == other.type and self.tag == other.tag and self.payload == other.payload


    def includes(self, other):
        if self.type == RuleType.DomainSuffix:
            return self.payload == other.payload or other.payload.endswith("." + self.payload)
        elif self.type == RuleType.DomainFull:
            return self == other
