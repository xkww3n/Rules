from ipaddress import ip_network, IPv4Network, IPv6Network

from utils.rule import is_domain


class Rule:
    _type: str  # DomainSuffix / DomainFull / IPCIDR / IPCIDR6
    _payload: str
    _tag: str

    def __init__(self, rule_type: str = "", payload: str = "", tag: str = ""):
        self._type = ""
        self._payload = ""
        self._tag = tag
        if rule_type:
            self.type = rule_type
        if payload:
            self.payload = payload

    def __str__(self):
        return f'{self.type}: {self.payload}{f" ({self.tag})" if self.tag else ""}'

    def __hash__(self):
        return hash((self.type, self.payload, self.tag))

    def __eq__(self, other):
        return self.type == other.type and self.payload == other.payload and self.tag == other.tag

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, rule_type: str):
        allowed_types = ("DomainSuffix", "DomainFull", "IPCIDR", "IPCIDR6")
        if rule_type not in allowed_types:
            raise TypeError(f"Unsupported type: {rule_type}")
        self._type = rule_type

    @property
    def payload(self) -> str:
        return self._payload

    @payload.setter
    def payload(self, payload: str):
        if "Domain" in self.type:
            if not is_domain(payload):
                raise ValueError(f"Invalid domain: {payload}")
        elif "IP" in self.type:
            try:
                ip_type = ip_network(payload)
            except ValueError:
                raise ValueError(f"Invalid IP address: {payload}")
            if self.type == "IPCIDR6" and type(ip_type) is IPv4Network:
                raise ValueError(f"IPv4 address stored in IPv6 type: {payload}")
            elif self.type == "IPCIDR" and type(ip_type) is IPv6Network:
                raise ValueError(f"IPv6 address stored in IPv4 type: {payload}")
        self._payload = payload

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, tag: str):
        self._tag = tag

    def includes(self, other):
        if self.type == "DomainSuffix":
            if self.payload == other.payload:
                return True
            return other.payload.endswith("." + self.payload)
        elif self.type == "DomainFull":
            return self == other
