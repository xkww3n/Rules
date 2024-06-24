from pytest import raises

from models.rule import Rule, RuleType


class Test:
    def test_type_checking_init(self):
        with raises(ValueError):
            Rule(RuleType.DomainSuffix, "[invalid_domain]")
        with raises(ValueError):
            Rule(RuleType.DomainFull, "[invalid_domain]")
        with raises(ValueError):
            Rule(RuleType.IPCIDR, "114514")
        with raises(ValueError):
            Rule(RuleType.IPCIDR6, "1919810")
        with raises(ValueError):
            Rule(RuleType.IPCIDR, "fc00:114::514")
        with raises(ValueError):
            Rule(RuleType.IPCIDR6, "1.14.5.14")

    def test_type_checking_runtime(self):
        with raises(ValueError):
            Rule(RuleType.DomainSuffix, "[invalid_domain]")

        with raises(ValueError):
            Rule(RuleType.DomainFull, "[invalid_domain]")

        with raises(ValueError):
            Rule(RuleType.IPCIDR, "114514")

        with raises(ValueError):
            Rule(RuleType.IPCIDR6, "1919810")

        with raises(ValueError):
            Rule(RuleType.IPCIDR, "fc00:114::514")

        with raises(ValueError):
            Rule(RuleType.IPCIDR6, "1.14.5.14")

    def test_to_str(self):
        test_rule = Rule(RuleType.DomainSuffix, "example.com", "TEST")
        assert str(test_rule) == "DomainSuffix: example.com (TEST)"

    def test_hash(self):
        test_rule_1 = Rule(RuleType.DomainSuffix, "example.com", "TEST")
        test_rule_2 = Rule(RuleType.DomainFull, "example.com", "TEST2")
        test_dict = [Rule(RuleType.DomainSuffix, "example.com", "TEST")]
        assert test_rule_1 in test_dict
        assert test_rule_2 not in test_dict

    def test_eq(self):
        test_rule_1 = Rule(RuleType.DomainSuffix, "example.com", "TEST")
        test_rule_2 = Rule(RuleType.DomainSuffix, "example.com", "TEST")
        assert test_rule_1 == test_rule_2

    def test_include(self):
        test_self_rule = Rule(RuleType.DomainSuffix, "example.com", "TEST")
        test_rule_1 = Rule(RuleType.DomainSuffix, "a.example.com", "TEST")
        test_rule_2 = Rule(RuleType.DomainFull, "b.example.com", "TEST")
        test_rule_3 = Rule(RuleType.DomainFull, "example.com", "TEST")
        test_rule_4 = Rule(RuleType.DomainSuffix, "example.com", "TEST")
        test_rule_5 = Rule(RuleType.DomainFull, "1example.com", "TEST")
        assert test_self_rule.includes(test_rule_1)
        assert test_self_rule.includes(test_rule_2)
        assert test_self_rule.includes(test_rule_3)
        assert test_self_rule.includes(test_rule_4)
        assert not test_self_rule.includes(test_rule_5)
