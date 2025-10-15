import logging
from enum import Enum
from typing import Optional

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
        list_unique = self._dedup_domains_trie()
        
        self.payload = list_unique
    
    def _dedup_domains_trie(self):
        
        class TrieNode:
            def __init__(self):
                self.children: dict = {}
                self.is_suffix_rule: bool = False
                self.is_full_rule: bool = False
                self.original_rule: Optional[Rule] = None
        
        root = TrieNode()
        list_unique = []

        for rule in self.payload:
            if rule.type == RuleType.DomainSuffix:
                parts = rule.payload.split('.')[::-1]
                node = root
                is_redundant = False
                
                for i, part in enumerate(parts):
                    if node.is_suffix_rule:
                        logging.debug(f'Remove "{rule}": included in "{node.original_rule}".')
                        is_redundant = True
                        break
                    
                    if part not in node.children:
                        node.children[part] = TrieNode()
                    node = node.children[part]
                
                if not is_redundant:
                    node.is_suffix_rule = True
                    node.original_rule = rule
                    list_unique.append(rule)
                    
                    self._remove_covered_rules(node, rule)
                    
            elif rule.type == RuleType.DomainFull:
                parts = rule.payload.split('.')[::-1]
                node = root
                is_covered = False
                
                for part in parts:
                    if node.is_suffix_rule:
                        logging.debug(f'Remove "{rule}": included in "{node.original_rule}".')
                        is_covered = True
                        break
                    
                    if part in node.children:
                        node = node.children[part]
                    else:
                        break
                
                if not is_covered and node.is_suffix_rule:
                    logging.debug(f'Remove "{rule}": included in "{node.original_rule}".')
                    is_covered = True
                
                if not is_covered:
                    parts = rule.payload.split('.')[::-1]
                    node = root
                    for part in parts:
                        if part not in node.children:
                            node.children[part] = TrieNode()
                        node = node.children[part]
                    
                    if not node.is_full_rule:
                        node.is_full_rule = True
                        node.original_rule = rule
                        list_unique.append(rule)
        
        return list_unique
    
    def _remove_covered_rules(self, node, covering_rule):
        def traverse(current_node):
            if current_node.is_suffix_rule and current_node.original_rule != covering_rule:
                if current_node.original_rule in self.payload:
                    logging.debug(f'Remove "{current_node.original_rule}": included in "{covering_rule}".')
                    current_node.is_suffix_rule = False
            
            if current_node.is_full_rule:
                if current_node.original_rule in self.payload:
                    logging.debug(f'Remove "{current_node.original_rule}": included in "{covering_rule}".')
                    current_node.is_full_rule = False
            
            for child in current_node.children.values():
                traverse(child)
        
        for child in node.children.values():
            traverse(child)
