from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType


def make_ruleset(ruleset_type, rules=()):
    ruleset = RuleSet(ruleset_type)
    for rule in rules:
        ruleset.add(rule)
    return ruleset


class Test:
    def test_hash(self):
        test_ruleset_1 = make_ruleset(RuleSetType.Domain, [Rule(RuleType.DomainSuffix, "example.com")])
        test_ruleset_2 = make_ruleset(RuleSetType.Domain, [Rule(RuleType.DomainFull, "example.com")])
        test_dict = [make_ruleset(RuleSetType.Domain, [Rule(RuleType.DomainSuffix, "example.com")])]
        assert test_ruleset_1 in test_dict
        assert test_ruleset_2 not in test_dict

    def test_eq(self):
        test_ruleset_1 = make_ruleset(RuleSetType.Domain, [Rule(RuleType.DomainSuffix, "example.com")])
        test_ruleset_2 = make_ruleset(RuleSetType.Domain, [Rule(RuleType.DomainSuffix, "example.com")])
        test_ruleset_3 = make_ruleset(RuleSetType.Domain, [Rule(RuleType.DomainSuffix, "1example.com")])
        assert test_ruleset_1 == test_ruleset_2
        assert test_ruleset_1 != test_ruleset_3

    def test_len(self):
        test_rule_1 = Rule(RuleType.DomainSuffix, "a.example.com")
        test_rule_2 = Rule(RuleType.DomainSuffix, "b.example.com")
        test_rule_3 = Rule(RuleType.DomainSuffix, "c.example.com")
        test_payload = [test_rule_1, test_rule_2, test_rule_3]
        test_ruleset = make_ruleset(RuleSetType.Domain, test_payload)
        assert len(test_ruleset) == 3

    def test_or(self):
        test_rule_1 = Rule(RuleType.DomainSuffix, "a.example.com")
        test_rule_2 = Rule(RuleType.DomainSuffix, "b.example.com")
        test_rule_3 = Rule(RuleType.DomainSuffix, "c.example.com")

        test_ruleset_1 = make_ruleset(RuleSetType.Domain, [test_rule_1, test_rule_2])
        test_ruleset_2 = make_ruleset(RuleSetType.Domain, [test_rule_2, test_rule_3])
        test_ruleset_expected = make_ruleset(RuleSetType.Domain, [test_rule_1, test_rule_2, test_rule_3])
        assert test_ruleset_1 | test_ruleset_2 == test_ruleset_expected

    def test_contains(self):
        test_rule_1 = Rule(RuleType.DomainSuffix, "a.example.com")
        test_rule_2 = Rule(RuleType.DomainSuffix, "b.example.com")
        test_ruleset = make_ruleset(RuleSetType.Domain, [test_rule_1])
        assert test_rule_1 in test_ruleset
        assert test_rule_2 not in test_ruleset

    def test_iterable(self):
        test_payload = [Rule(RuleType.DomainSuffix, "1.example.com"),
                        Rule(RuleType.DomainSuffix, "2.example.com"),
                        Rule(RuleType.DomainSuffix, "3.example.com")]
        test_ruleset = make_ruleset(RuleSetType.Domain, test_payload)
        try:
            iter(test_ruleset)
        except TypeError:
            assert False
        assert True

    def test_add(self):
        test_rule = Rule(RuleType.DomainSuffix, "example.com")
        test_ruleset = RuleSet(RuleSetType.Domain)
        test_ruleset.add(test_rule)
        assert test_ruleset == make_ruleset(RuleSetType.Domain, [test_rule])

    def test_remove(self):
        test_rule_1 = Rule(RuleType.DomainSuffix, "a.example.com")
        test_rule_2 = Rule(RuleType.DomainSuffix, "b.example.com")
        test_ruleset = make_ruleset(RuleSetType.Domain, [test_rule_1, test_rule_2])
        test_ruleset.remove(test_rule_2)
        assert test_ruleset == make_ruleset(RuleSetType.Domain, [test_rule_1])

    def test_remove_many(self):
        test_rule_1 = Rule(RuleType.DomainSuffix, "a.example.com")
        test_rule_2 = Rule(RuleType.DomainSuffix, "b.example.com")
        test_rule_3 = Rule(RuleType.DomainSuffix, "c.example.com")
        test_ruleset = make_ruleset(RuleSetType.Domain, [test_rule_1, test_rule_2, test_rule_3])
        test_ruleset.remove_many([test_rule_1, test_rule_3])
        assert test_ruleset == make_ruleset(RuleSetType.Domain, [test_rule_2])

    def test_domain_ruleset_dedups_on_add(self):
        test_ruleset = RuleSet(RuleSetType.Domain)
        test_ruleset.add(Rule(RuleType.DomainFull, "a.example.com"))
        test_ruleset.add(Rule(RuleType.DomainSuffix, "example.com"))

        assert test_ruleset == make_ruleset(RuleSetType.Domain, [Rule(RuleType.DomainSuffix, "example.com")])

    def test_domain_ruleset_rejects_tags(self):
        test_ruleset = RuleSet(RuleSetType.Domain)
        try:
            test_ruleset.add(Rule(RuleType.DomainSuffix, "example.com", "TEST"))
        except ValueError:
            assert True
            return
        assert False
