from pytest import raises

from Utils import rule


class Tests:
    def test_type_checking_init(self):
        with raises(TypeError):
            rule.Rule("NotAllowedType", "test_payload")
        with raises(ValueError):
            rule.Rule("DomainSuffix", "[invalid_domain]")
        with raises(ValueError):
            rule.Rule("DomainFull", "[invalid_domain]")
        with raises(ValueError):
            rule.Rule("IPCIDR", "114514")
        with raises(ValueError):
            rule.Rule("IPCIDR6", "1919810")

    def test_type_checking_runtime(self):
        test_rule = rule.Rule()
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

    def test_to_str(self):
        test_rule = rule.Rule("DomainSuffix", "example.com", "TEST")
        assert str(test_rule) == 'Type: "DomainSuffix", Payload: "example.com", Tag: TEST'

    def test_hash(self):
        test_rule_a = rule.Rule("DomainSuffix", "example.com", "TEST")
        test_rule_b = rule.Rule("DomainFull", "example.com", "TEST2")
        test_dict = [rule.Rule("DomainSuffix", "example.com", "TEST")]
        assert test_rule_a in test_dict
        assert test_rule_b not in test_dict

    def test_eq(self):
        test_rule_a = rule.Rule("DomainSuffix", "example.com", "TEST")
        test_rule_b = rule.Rule("DomainSuffix", "example.com", "TEST")
        assert test_rule_a == test_rule_b

    def test_include(self):
        test_self_rule = rule.Rule("DomainSuffix", "example.com", "TEST")
        test_rule_a = rule.Rule("DomainSuffix", "a.example.com", "TEST")
        test_rule_b = rule.Rule("DomainFull", "b.example.com", "TEST")
        test_rule_c = rule.Rule("DomainFull", "example.com", "TEST")
        test_rule_d = rule.Rule("DomainSuffix", "example.com", "TEST")
        test_rule_e = rule.Rule("DomainFull", "1example.com", "TEST")
        assert test_self_rule.includes(test_rule_a)
        assert test_self_rule.includes(test_rule_b)
        assert test_self_rule.includes(test_rule_c)
        assert test_self_rule.includes(test_rule_d)
        assert not test_self_rule.includes(test_rule_e)
