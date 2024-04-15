from models.rule import Rule
from models.ruleset import RuleSet


class Test:
    def test_hash(self):
        test_ruleset_1 = RuleSet("Domain",
                                 [Rule("DomainSuffix", "example.com", "TEST")])
        test_ruleset_2 = RuleSet("Domain",
                                 [Rule("DomainFull", "example.com", "TEST2")])
        test_dict = [RuleSet("Domain",
                             [Rule("DomainSuffix", "example.com", "TEST")])]
        assert test_ruleset_1 in test_dict
        assert test_ruleset_2 not in test_dict

    def test_eq(self):
        test_ruleset_1 = RuleSet("Domain",
                                 [Rule("DomainSuffix", "example.com", "TEST")])
        test_ruleset_2 = RuleSet("Domain",
                                 [Rule("DomainSuffix", "example.com", "TEST")])
        test_ruleset_3 = RuleSet("Domain",
                                 [Rule("DomainSuffix", "1example.com", "TEST")])
        assert test_ruleset_1 == test_ruleset_2
        assert test_ruleset_1 != test_ruleset_3

    def test_len(self):
        test_rule_1 = Rule("DomainSuffix", "a.example.com", "TEST1")
        test_rule_2 = Rule("DomainSuffix", "b.example.com", "TEST2")
        test_rule_3 = Rule("DomainSuffix", "c.example.com", "TEST3")
        test_payload = [test_rule_1, test_rule_2, test_rule_3]
        test_ruleset = RuleSet("Domain", test_payload)
        assert len(test_ruleset) == 3

    def test_or(self):
        test_rule_1 = Rule("DomainSuffix", "a.example.com", "TEST1")
        test_rule_2 = Rule("DomainSuffix", "b.example.com", "TEST2")
        test_rule_3 = Rule("DomainSuffix", "c.example.com", "TEST3")

        test_ruleset_1 = RuleSet("Domain", [test_rule_1, test_rule_2])
        test_ruleset_2 = RuleSet("Domain", [test_rule_2, test_rule_3])
        test_ruleset_expected = RuleSet("Domain", [test_rule_1, test_rule_2, test_rule_3])
        assert test_ruleset_1 | test_ruleset_2 == test_ruleset_expected

    def test_contains(self):
        test_rule_1 = Rule("DomainSuffix", "a.example.com", "TEST1")
        test_rule_2 = Rule("DomainSuffix", "b.example.com", "TEST2")
        test_ruleset = RuleSet("Domain", [test_rule_1])
        assert test_rule_1 in test_ruleset
        assert test_rule_2 not in test_ruleset

    def test_iterable(self):
        test_payload = [Rule("DomainSuffix", "1.example.com"),
                        Rule("DomainSuffix", "2.example.com"),
                        Rule("DomainSuffix", "3.example.com")]
        test_ruleset = RuleSet("Domain", test_payload)
        try:
            iter(test_ruleset)
        except TypeError:
            assert False
        assert True

    def test_copy(self):
        test_ruleset = RuleSet("Domain",
                               [Rule("DomainSuffix", "example.com", "TEST1")])
        assert test_ruleset.deepcopy() == test_ruleset

    def test_add(self):
        test_rule = Rule("DomainSuffix", "example.com", "TEST")
        test_ruleset = RuleSet("Domain", [])
        test_ruleset.add(test_rule)
        assert test_ruleset == RuleSet("Domain", [test_rule])

    def test_remove(self):
        test_rule_1 = Rule("DomainSuffix", "a.example.com", "TEST1")
        test_rule_2 = Rule("DomainSuffix", "b.example.com", "TEST2")
        test_ruleset = RuleSet("Domain", [test_rule_1, test_rule_2])
        test_ruleset.remove(test_rule_2)
        assert test_ruleset == RuleSet("Domain", [test_rule_1])
