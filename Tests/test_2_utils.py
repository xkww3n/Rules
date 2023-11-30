from Utils import rule
from pathlib import Path


class Tests:
    def test_is_ipv4addr(self):
        valid_ipaddr = "11.4.5.14"
        invalid_ipaddr_a = "114.514"
        invalid_ipaddr_b = "19.1.9.810"
        invalid_ipaddr_c = "test.www.example.com"
        assert rule.is_ipv4addr(valid_ipaddr)
        assert not rule.is_ipv4addr(invalid_ipaddr_a)
        assert not rule.is_ipv4addr(invalid_ipaddr_b)
        assert not rule.is_ipv4addr(invalid_ipaddr_c)

    def test_is_domain(self):
        valid_domain = "www.example.com"
        invalid_domain_a = "[invalid]"
        invalid_domain_b = "-invalid.tld"
        ipv4addr = "11.4.5.14"
        assert rule.is_domain(valid_domain)
        assert not rule.is_domain(invalid_domain_a)
        assert not rule.is_domain(invalid_domain_b)
        assert not rule.is_domain(ipv4addr)

    def test_custom_convert(self):
        test_src_path = Path("./src/custom_ruleset/")
        test_conv_ruleset = rule.custom_convert(test_src_path/"domain.txt")
        assert test_conv_ruleset == rule.RuleSet("Domain",
                                                 [rule.Rule("DomainSuffix", "example.com"),
                                                  rule.Rule("DomainFull", "example.com")])

        test_conv_ruleset = rule.custom_convert(test_src_path/"ipcidr.txt")
        assert test_conv_ruleset == rule.RuleSet("IPCIDR",
                                                 [rule.Rule("IPCIDR", "11.4.5.14"),])

        test_conv_ruleset = rule.custom_convert(test_src_path/"classic.txt")
        assert test_conv_ruleset == rule.RuleSet("Combined",
                                                 [rule.Rule("DomainFull", "example.com")])

    def test_patch(self):
        test_src_patch = Path("./src/patch/")
        test_ruleset = rule.RuleSet("Domain", [rule.Rule("DomainFull", "example.com")])
        rule.apply_patch(test_ruleset, "patch", test_src_patch)
        assert test_ruleset == rule.RuleSet("Domain", [rule.Rule("DomainSuffix", "example.com")])
