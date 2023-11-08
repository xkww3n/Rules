from Utils import rule


class Tests:
    def test_hash(self):
        test_ruleset_a = rule.RuleSet("Domain",
                                      [rule.Rule("DomainSuffix", "example.com", "TEST")])
        test_ruleset_b = rule.RuleSet("Domain",
                                      [rule.Rule("DomainFull", "example.com", "TEST2")])
        test_dict = [rule.RuleSet("Domain",
                                  [rule.Rule("DomainSuffix", "example.com", "TEST")])]
        assert test_ruleset_a in test_dict
        assert test_ruleset_b not in test_dict

    def test_eq(self):
        test_ruleset_a = rule.RuleSet("Domain",
                                      [rule.Rule("DomainSuffix", "example.com", "TEST")])
        test_ruleset_b = rule.RuleSet("Domain",
                                      [rule.Rule("DomainSuffix", "example.com", "TEST")])
        test_ruleset_c = rule.RuleSet("Domain",
                                      [rule.Rule("DomainSuffix", "1example.com", "TEST")])
        assert test_ruleset_a == test_ruleset_b
        assert test_ruleset_a != test_ruleset_c

    def test_len(self):
        test_rule_a = rule.Rule("DomainSuffix", "a.example.com", "TEST1")
        test_rule_b = rule.Rule("DomainSuffix", "b.example.com", "TEST2")
        test_rule_c = rule.Rule("DomainSuffix", "c.example.com", "TEST3")
        test_payload = [test_rule_a, test_rule_b, test_rule_c]
        test_ruleset = rule.RuleSet("Domain", test_payload)
        assert len(test_ruleset) == 3

    def test_or(self):
        test_rule_a = rule.Rule("DomainSuffix", "a.example.com", "TEST1")
        test_rule_b = rule.Rule("DomainSuffix", "b.example.com", "TEST2")
        test_rule_c = rule.Rule("DomainSuffix", "c.example.com", "TEST3")

        test_ruleset_a = rule.RuleSet("Domain", [test_rule_a, test_rule_b])
        test_ruleset_b = rule.RuleSet("Domain", [test_rule_b, test_rule_c])
        test_ruleset_expected = rule.RuleSet("Domain", [test_rule_a, test_rule_b, test_rule_c])
        assert test_ruleset_a | test_ruleset_b == test_ruleset_expected

    def test_contains(self):
        test_rule_a = rule.Rule("DomainSuffix", "a.example.com", "TEST1")
        test_rule_b = rule.Rule("DomainSuffix", "b.example.com", "TEST2")
        test_ruleset = rule.RuleSet("Domain", [test_rule_a])
        assert test_rule_a in test_ruleset
        assert test_rule_b not in test_ruleset

    def test_iterable(self):
        test_payload = [rule.Rule("DomainSuffix", "1.example.com"),
                        rule.Rule("DomainSuffix", "2.example.com"),
                        rule.Rule("DomainSuffix", "3.example.com")]
        test_ruleset = rule.RuleSet("Domain", test_payload)
        try:
            iter(test_ruleset)
        except TypeError:
            assert False
        assert True

    def test_copy(self):
        test_ruleset = rule.RuleSet("Domain",
                                    [rule.Rule("DomainSuffix", "example.com", "TEST1")])
        assert test_ruleset.deepcopy() == test_ruleset

    def test_add(self):
        test_rule = rule.Rule("DomainSuffix", "example.com", "TEST")
        test_ruleset = rule.RuleSet("Domain", [])
        test_ruleset.add(test_rule)
        assert test_ruleset == rule.RuleSet("Domain", [test_rule])

    def test_remove(self):
        test_rule_a = rule.Rule("DomainSuffix", "a.example.com", "TEST1")
        test_rule_b = rule.Rule("DomainSuffix", "b.example.com", "TEST2")
        test_ruleset = rule.RuleSet("Domain", [test_rule_a, test_rule_b])
        test_ruleset.remove(test_rule_b)
        assert test_ruleset == rule.RuleSet("Domain", [test_rule_a])

    def test_sort(self):
        test_rule_a = rule.Rule("DomainSuffix", "a.example.com", "TEST1")
        test_rule_b = rule.Rule("DomainSuffix", "b.example.com", "TEST2")
        test_ruleset = rule.RuleSet("Domain", [test_rule_b, test_rule_a])
        test_ruleset.sort()
        assert test_ruleset == rule.RuleSet("Domain", [test_rule_a, test_rule_b])

    def test_dedup(self):
        test_rule_a = rule.Rule("DomainSuffix", "1example.com")
        test_rule_b = rule.Rule("DomainSuffix", "a.1example.com")
        test_rule_c = rule.Rule("DomainFull", "1example.com")
        test_rule_d = rule.Rule("DomainSuffix", "1example.tld")
        test_rule_e = rule.Rule("DomainSuffix", "a.1example.tld")
        test_rule_f = rule.Rule("DomainFull", "1example.tld")
        test_ruleset = rule.RuleSet("Domain",
                                    [test_rule_a, test_rule_b, test_rule_c, test_rule_d, test_rule_e, test_rule_f])
        test_ruleset.dedup()
        assert test_ruleset == rule.RuleSet("Domain", [test_rule_a, test_rule_d])
