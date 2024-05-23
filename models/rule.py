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
        return f'{self._type}: {self._payload}{f" ({self._tag})" if self._tag else ""}'

    def __hash__(self):
        return hash((self._type, self._payload, self._tag))

    def __eq__(self, other):
        # noinspection PyProtectedMember
        return self._type == other._type and self._payload == other._payload and self._tag == other._tag

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
        if "Domain" in self._type:
            if not is_domain(payload):
                raise ValueError(f"Invalid domain: {payload}")
        elif "IP" in self._type:
            ip_type = ip_network(payload, strict=False)
            if self._type == "IPCIDR6" and isinstance(ip_type, IPv4Network):
                raise ValueError(f"IPv4 address stored in IPv6 type: {payload}")
            elif self._type == "IPCIDR" and isinstance(ip_type, IPv6Network):
                raise ValueError(f"IPv6 address stored in IPv4 type: {payload}")
        self._payload = payload

    @property
    def tag(self) -> str:
        return self._tag

    @tag.setter
    def tag(self, tag: str):
        self._tag = tag

    def includes(self, other):
        if self._type == "DomainSuffix":
            # noinspection PyProtectedMember
            if self._payload == other._payload:
                return True
            # noinspection PyProtectedMember
            return other._payload.endswith("." + self._payload)
        elif self._type == "DomainFull":
            return self == other
