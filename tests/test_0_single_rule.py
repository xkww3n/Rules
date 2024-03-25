from pytest import raises

from models.rule import Rule


class Test:
    def test_type_checking_init(self):
        with raises(TypeError):
            Rule("NotAllowedType", "test_payload")
        with raises(ValueError):
            Rule("DomainSuffix", "[invalid_domain]")
        with raises(ValueError):
            Rule("DomainFull", "[invalid_domain]")
        with raises(ValueError):
            Rule("IPCIDR", "114514")
        with raises(ValueError):
            Rule("IPCIDR6", "1919810")
        with raises(ValueError):
            Rule("IPCIDR", "fc00:114::514")
        with raises(ValueError):
            Rule("IPCIDR6", "1.14.5.14")

    def test_type_checking_runtime(self):
        test_rule = Rule()
        with raises(TypeError):
            test_rule.set_type("NotAllowedType")

        test_rule.set_type("DomainSuffix")
        with raises(ValueError):
            test_rule.set_payload("[invalid_domain]")

        test_rule.set_type("DomainFull")
        with raises(ValueError):
            test_rule.set_payload("[invalid_domain]")

        test_rule.set_type("IPCIDR")
        with raises(ValueError):
            test_rule.set_payload("114514")

        test_rule.set_type("IPCIDR6")
        with raises(ValueError):
            test_rule.set_payload("1919810")

        test_rule.set_type("IPCIDR")
        with raises(ValueError):
            test_rule.set_payload("fc00:114::514")

        test_rule.set_type("IPCIDR6")
        with raises(ValueError):
            test_rule.set_payload("1.14.5.14")

    def test_to_str(self):
        test_rule = Rule("DomainSuffix", "example.com", "TEST")
        assert str(test_rule) == 'Type: "DomainSuffix", Payload: "example.com", Tag: TEST'

    def test_hash(self):
        test_rule_a = Rule("DomainSuffix", "example.com", "TEST")
        test_rule_b = Rule("DomainFull", "example.com", "TEST2")
        test_dict = [Rule("DomainSuffix", "example.com", "TEST")]
        assert test_rule_a in test_dict
        assert test_rule_b not in test_dict

    def test_eq(self):
        test_rule_a = Rule("DomainSuffix", "example.com", "TEST")
        test_rule_b = Rule("DomainSuffix", "example.com", "TEST")
        assert test_rule_a == test_rule_b

    def test_include(self):
        test_self_rule = Rule("DomainSuffix", "example.com", "TEST")
        test_rule_a = Rule("DomainSuffix", "a.example.com", "TEST")
        test_rule_b = Rule("DomainFull", "b.example.com", "TEST")
        test_rule_c = Rule("DomainFull", "example.com", "TEST")
        test_rule_d = Rule("DomainSuffix", "example.com", "TEST")
        test_rule_e = Rule("DomainFull", "1example.com", "TEST")
        assert test_self_rule.includes(test_rule_a)
        assert test_self_rule.includes(test_rule_b)
        assert test_self_rule.includes(test_rule_c)
        assert test_self_rule.includes(test_rule_d)
        assert not test_self_rule.includes(test_rule_e)
