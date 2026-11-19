import logging
from enum import Enum
from ipaddress import IPv4Network, IPv6Network, collapse_addresses

from models.rule import Rule, RuleType


class RuleSetType(Enum):
    Domain = 1
    IPCIDR = 2
    Combined = 3


class DomainTrieNode:
    def __init__(self):
        self.children: dict[str, DomainTrieNode] = {}
        self.suffix_rule = False
        self.full_rule = False
        self.subtree_rule_count = 0


class DomainTrie:
    def __init__(self):
        self.root = DomainTrieNode()

    def __len__(self):
        return self.root.subtree_rule_count

    def __iter__(self):
        return iter(self.to_rules())

    @staticmethod
    def _parts(payload: str) -> list[str]:
        return payload.split(".")[::-1]

    @staticmethod
    def _payload(parts: list[str]) -> str:
        return ".".join(parts[::-1])

    def insert(self, rule: Rule) -> None:
        self._validate_rule(rule)
        parts = self._parts(rule.payload)
        node = self.root
        path = [self.root]

        for part in parts:
            if node.suffix_rule:
                self._mark_domain_covered(rule)
                return
            if part not in node.children:
                node.children[part] = DomainTrieNode()
            node = node.children[part]
            path.append(node)

        if node.suffix_rule and rule.type == RuleType.DomainSuffix:
            self._mark_domain_duplicate(rule)
            return
        if node.suffix_rule:
            self._mark_domain_covered(rule)
            return

        if rule.type == RuleType.DomainSuffix:
            self._insert_suffix(rule, node, path)
        elif rule.type == RuleType.DomainFull:
            self._insert_full(rule, node, path)

    def find_covering(self, rule: Rule) -> Rule | None:
        self._validate_rule(rule)
        node = self.root
        parts = self._parts(rule.payload)
        traversed = []

        for part in parts:
            if node.suffix_rule:
                return Rule(RuleType.DomainSuffix, self._payload(traversed))
            if part not in node.children:
                return None
            node = node.children[part]
            traversed.append(part)

        if node.suffix_rule:
            return Rule(RuleType.DomainSuffix, rule.payload)
        if rule.type == RuleType.DomainFull and node.full_rule:
            return Rule(RuleType.DomainFull, rule.payload)
        return None

    def contains_exact(self, rule: Rule) -> bool:
        self._validate_rule(rule)
        node = self.root
        for part in self._parts(rule.payload):
            if part not in node.children:
                return False
            node = node.children[part]

        if rule.type == RuleType.DomainSuffix:
            return node.suffix_rule
        if rule.type == RuleType.DomainFull:
            return node.full_rule
        return False

    def to_rules(self) -> list[Rule]:
        result = []

        def walk(node: DomainTrieNode, parts: list[str]) -> None:
            if node.suffix_rule:
                result.append(Rule(RuleType.DomainSuffix, self._payload(parts)))
                return
            if node.full_rule:
                result.append(Rule(RuleType.DomainFull, self._payload(parts)))
            for part in sorted(node.children):
                walk(node.children[part], parts + [part])

        for part in sorted(self.root.children):
            walk(self.root.children[part], [part])
        return result

    def _insert_suffix(self, rule: Rule, node: DomainTrieNode, path: list[DomainTrieNode]) -> None:
        covered_count = node.subtree_rule_count
        if covered_count:
            logging.debug(f'Remove {covered_count} domain rules: included in "{rule}".')

        node.suffix_rule = True
        node.full_rule = False
        node.subtree_rule_count = 1
        for ancestor in path[:-1]:
            ancestor.subtree_rule_count += 1 - covered_count

    def _insert_full(self, rule: Rule, node: DomainTrieNode, path: list[DomainTrieNode]) -> None:
        if node.full_rule:
            self._mark_domain_duplicate(rule)
            return

        node.full_rule = True
        for item in path:
            item.subtree_rule_count += 1

    def _mark_domain_duplicate(self, rule: Rule) -> None:
        logging.debug(f'Remove "{rule}": exact duplicate.')

    def _mark_domain_covered(self, rule: Rule) -> None:
        logging.debug(f'Remove "{rule}": included in an existing domain suffix rule.')

    @staticmethod
    def _validate_rule(rule: Rule) -> None:
        if rule.type not in {RuleType.DomainSuffix, RuleType.DomainFull}:
            raise ValueError(f"{rule.type.value} rule found in a domain trie.")
        if rule.tag:
            raise ValueError(f'Tagged rule "{rule}" found in a domain trie.')


class RuleSet:
    type: RuleSetType

    def __init__(self, ruleset_type: RuleSetType):
        self.type = ruleset_type
        if ruleset_type == RuleSetType.Domain:
            self._domain_trie = DomainTrie()
        elif ruleset_type == RuleSetType.IPCIDR:
            self._ipv4_networks: set[IPv4Network] = set()
            self._ipv6_networks: set[IPv6Network] = set()
        else:
            self._combined_rules: list[Rule] = []

    def __hash__(self):
        return hash((self.type, tuple(self)))

    def __eq__(self, other):
        if not isinstance(other, RuleSet):
            return False
        return self.type == other.type and list(self) == list(other)

    def __len__(self):
        if self.type == RuleSetType.Domain:
            return len(self._domain_trie)
        if self.type == RuleSetType.IPCIDR:
            return len(self._ipv4_networks) + len(self._ipv6_networks)
        return len(self._combined_rules)

    def __or__(self, other):
        if self.type != other.type:
            raise ValueError("Cannot merge rulesets with different types.")
        for rule in other:
            self.add(rule)
        return self

    def __contains__(self, item):
        if self.type == RuleSetType.Domain:
            return self._domain_trie.contains_exact(item)
        if self.type == RuleSetType.IPCIDR:
            self._validate_rule(item)
            if item.type is RuleType.IPCIDR:
                return IPv4Network(item.payload, strict=False) in self._ipv4_networks
            return IPv6Network(item.payload, strict=False) in self._ipv6_networks
        return item in self._combined_rules

    def __iter__(self):
        if self.type == RuleSetType.Domain:
            return iter(self._domain_trie)
        if self.type == RuleSetType.IPCIDR:
            return iter(self._ip_rules())
        return iter(self._combined_rules)

    def add(self, rule):
        self._validate_rule(rule)
        if self.type == RuleSetType.Domain:
            self._domain_trie.insert(rule)
            return
        if self.type == RuleSetType.IPCIDR:
            if rule.type is RuleType.IPCIDR:
                self._ipv4_networks.add(IPv4Network(rule.payload, strict=False))
            else:
                self._ipv6_networks.add(IPv6Network(rule.payload, strict=False))
            return
        if rule not in self._combined_rules:
            self._combined_rules.append(rule)

    def remove(self, rule):
        if self.type == RuleSetType.Domain:
            payload = list(self)
            payload.remove(rule)
            self._domain_trie = DomainTrie()
            for item in payload:
                self.add(item)
            return
        if self.type == RuleSetType.IPCIDR:
            self._validate_rule(rule)
            if rule.type is RuleType.IPCIDR:
                self._ipv4_networks.remove(IPv4Network(rule.payload, strict=False))
            else:
                self._ipv6_networks.remove(IPv6Network(rule.payload, strict=False))
            return
        self._combined_rules.remove(rule)

    def remove_many(self, rules):
        if not rules:
            return
        for rule in rules:
            self._validate_rule(rule)

        rules_to_remove = set(rules)
        if self.type == RuleSetType.Domain:
            payload = [rule for rule in self if rule not in rules_to_remove]
            self._domain_trie = DomainTrie()
            for item in payload:
                self.add(item)
            return
        if self.type == RuleSetType.IPCIDR:
            for rule in rules_to_remove:
                self.remove(rule)
            return
        self._combined_rules = [rule for rule in self._combined_rules if rule not in rules_to_remove]

    def find_covering(self, rule: Rule) -> Rule | None:
        if self.type != RuleSetType.Domain:
            raise TypeError("Only domain-type rulesets support domain coverage lookup.")
        return self._domain_trie.find_covering(rule)

    def dedup_ipcidr(self) -> None:
        if self.type != RuleSetType.IPCIDR:
            raise TypeError("Only IPCIDR-type rulesets support CIDR deduplication.")
        self._ipv4_networks, self._ipv6_networks = (
            set(collapse_addresses(self._ipv4_networks)),
            set(collapse_addresses(self._ipv6_networks)),
        )

    def _ip_rules(self) -> list[Rule]:
        return [
            *[
                Rule(RuleType.IPCIDR, network.with_prefixlen)
                for network in self._sorted_networks(self._ipv4_networks)
            ],
            *[
                Rule(RuleType.IPCIDR6, network.with_prefixlen)
                for network in self._sorted_networks(self._ipv6_networks)
            ],
        ]

    @staticmethod
    def _sorted_networks(networks):
        return sorted(networks, key=lambda network: (int(network.network_address), network.prefixlen))

    def _validate_rule(self, rule: Rule) -> None:
        if self.type == RuleSetType.Domain:
            if rule.type not in {RuleType.DomainSuffix, RuleType.DomainFull}:
                raise ValueError(f"{rule.type.value} rule found in a domain-type ruleset.")
            if rule.tag:
                raise ValueError(f'Tagged rule "{rule}" found in a domain-type ruleset.')
        elif self.type == RuleSetType.IPCIDR:
            if rule.type not in {RuleType.IPCIDR, RuleType.IPCIDR6}:
                raise ValueError(f"{rule.type.value} rule found in a IPCIDR-type ruleset.")
            if rule.tag:
                raise ValueError(f'Tagged rule "{rule}" found in a IPCIDR-type ruleset.')
