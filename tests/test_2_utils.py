from pathlib import Path

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType
from utils import rule, ruleset


class TestLoad:
    def test_load_domain(self):
        test_src_path = Path("tests/src/custom_ruleset/")
        loaded_ruleset = ruleset.load(test_src_path/"domain.txt")
        assert loaded_ruleset == RuleSet(RuleSetType.Domain,
                                         [Rule(RuleType.DomainSuffix, "example.com"),
                                          Rule(RuleType.DomainFull, "example.com")])

    def test_load_ipcidr(self):
        test_src_path = Path("tests/src/custom_ruleset/")
        loaded_ruleset = ruleset.load(test_src_path/"ipcidr.txt")
        assert loaded_ruleset == RuleSet(RuleSetType.IPCIDR,
                                         [Rule(RuleType.IPCIDR, "11.4.5.14"),
                                          Rule(RuleType.IPCIDR6, "fc00:114::514")])

    def test_load_combined(self):
        test_src_path = Path("tests/src/custom_ruleset/")
        loaded_ruleset = ruleset.load(test_src_path/"combined.txt")
        assert loaded_ruleset == RuleSet(RuleSetType.Combined,
                                         [Rule(RuleType.DomainFull, "example.com"),
                                          Rule(RuleType.DomainSuffix, "example.com"),
                                          Rule(RuleType.IPCIDR, "11.4.5.14"),
                                          Rule(RuleType.IPCIDR6, "fc00:114::514"),
                                          Rule(RuleType.IPCIDR, "11.4.5.14", "no-resolve"),
                                          Rule(RuleType.IPCIDR6, "fc00:114::514", "no-resolve")])


class TestDump:
    def test_dump_domain(self):
        test_dist = Path("tests/dists/")
        ruleset_domain = ruleset.load(Path("tests/src/custom_ruleset/domain.txt"))
        ruleset.batch_dump(ruleset_domain, config.TARGETS, test_dist, "domain")

        assert (test_dist/"text"/"domain.txt").exists()
        with open(test_dist/"text"/"domain.txt", mode="r") as f:
            assert f.read() == (".example.com\n"
                                "example.com\n")

        assert (test_dist/"text-plus"/"domain.txt").exists()
        with open(test_dist/"text-plus"/"domain.txt", mode="r") as f:
            assert f.read() == ("+.example.com\n"
                                "example.com\n")

        assert (test_dist/"quantumult"/"domain.txt").exists()
        with open(test_dist/"quantumult"/"domain.txt", mode="r") as f:
            assert f.read() == ("host-suffix, example.com, policy\n"
                                "host, example.com, policy\n")

        assert (test_dist/"classical"/"domain.txt").exists()
        with open(test_dist/"classical"/"domain.txt", mode="r") as f:
            assert f.read() == ("DOMAIN-SUFFIX,example.com\n"
                                "DOMAIN,example.com\n")

        assert (test_dist/"yaml"/"domain.yaml").exists()
        with open(test_dist/"yaml"/"domain.yaml", mode="r") as f:
            assert f.read() == ("payload:\n"
                                "  - '+.example.com'\n"
                                "  - 'example.com'\n")

        assert (test_dist/"geosite"/"domain").exists()
        with open(test_dist/"geosite"/"domain", mode="r") as f:
            assert f.read() == ("example.com\n"
                                "full:example.com\n")

        assert (test_dist/"sing-ruleset"/"domain.json").exists()
        with open(test_dist/"sing-ruleset"/"domain.json", mode="r") as f:
            assert f.read() == ('{\n'
                                '  "version": 1,\n'
                                '  "rules": [\n'
                                '    {\n'
                                '      "domain_suffix": [\n'
                                '        "example.com"\n'
                                '      ],\n'
                                '      "domain": [\n'
                                '        "example.com"\n'
                                '      ]\n'
                                '    }\n'
                                '  ]\n'
                                '}')

    def test_dump_ipcidr(self):
        test_dist = Path("tests/dists/")
        ruleset_ipcidr = ruleset.load(Path("tests/src/custom_ruleset/ipcidr.txt"))
        ruleset.batch_dump(ruleset_ipcidr, config.TARGETS, test_dist, "ipcidr")

        assert not (test_dist/"text-plus"/"ipcidr.txt").exists()
        assert not (test_dist/"geosite"/"ipcidr").exists()

        assert (test_dist/"text"/"ipcidr.txt").exists()
        with open(test_dist/"text"/"ipcidr.txt", mode="r") as f:
            assert f.read() == ("11.4.5.14\n"
                                "fc00:114::514\n")

        assert (test_dist/"quantumult"/"ipcidr.txt").exists()
        with open(test_dist/"quantumult"/"ipcidr.txt", mode="r") as f:
            assert f.read() == ("ip-cidr, 11.4.5.14, policy\n"
                                "ip6-cidr, fc00:114::514, policy\n")

        assert (test_dist/"classical"/"ipcidr.txt").exists()
        with open(test_dist/"classical"/"ipcidr.txt", mode="r") as f:
            assert f.read() == ("IP-CIDR,11.4.5.14\n"
                                "IP-CIDR6,fc00:114::514\n")

        assert (test_dist/"yaml"/"ipcidr.yaml").exists()
        with open(test_dist/"yaml"/"ipcidr.yaml", mode="r") as f:
            assert f.read() == ("payload:\n"
                                "  - '11.4.5.14'\n"
                                "  - 'fc00:114::514'\n")

        assert (test_dist/"sing-ruleset"/"ipcidr.json").exists()
        with open(test_dist/"sing-ruleset"/"ipcidr.json", mode="r") as f:
            assert f.read() == ('{\n'
                                '  "version": 1,\n'
                                '  "rules": [\n'
                                '    {\n'
                                '      "ip_cidr": [\n'
                                '        "11.4.5.14",\n'
                                '        "fc00:114::514"\n'
                                '      ]\n'
                                '    }\n'
                                '  ]\n'
                                '}')

    def test_dump_combined(self):
        test_dist = Path("tests/dists/")
        ruleset_combined = ruleset.load(Path("tests/src/custom_ruleset/combined.txt"))
        ruleset.batch_dump(ruleset_combined, config.TARGETS, test_dist, "combined")

        assert not (test_dist/"text"/"combined.txt").exists()
        assert not (test_dist/"text-plus"/"combined.txt").exists()
        assert not (test_dist/"geosite"/"combined").exists()

        assert (test_dist/"quantumult"/"combined.txt").exists()
        with open(test_dist/"quantumult"/"combined.txt", mode="r") as f:
            assert f.read() == ("host, example.com, policy\n"
                                "host-suffix, example.com, policy\n"
                                "ip-cidr, 11.4.5.14, policy\n"
                                "ip6-cidr, fc00:114::514, policy\n"
                                "ip-cidr, 11.4.5.14, policy, no-resolve\n"
                                "ip6-cidr, fc00:114::514, policy, no-resolve\n")

        assert (test_dist/"classical"/"combined.txt").exists()
        with open(test_dist/"classical"/"combined.txt", mode="r") as f:
            assert f.read() == ("DOMAIN,example.com\n"
                                "DOMAIN-SUFFIX,example.com\n"
                                "IP-CIDR,11.4.5.14\n"
                                "IP-CIDR6,fc00:114::514\n"
                                "IP-CIDR,11.4.5.14,no-resolve\n"
                                "IP-CIDR6,fc00:114::514,no-resolve\n")

        assert (test_dist/"yaml"/"combined.yaml").exists()
        with open(test_dist/"yaml"/"combined.yaml", mode="r") as f:
            assert f.read() == ("payload:\n"
                                "  - 'DOMAIN,example.com'\n"
                                "  - 'DOMAIN-SUFFIX,example.com'\n"
                                "  - 'IP-CIDR,11.4.5.14'\n"
                                "  - 'IP-CIDR6,fc00:114::514'\n"
                                "  - 'IP-CIDR,11.4.5.14,no-resolve'\n"
                                "  - 'IP-CIDR6,fc00:114::514,no-resolve'\n")

        assert (test_dist/"sing-ruleset"/"combined.json").exists()
        with open(test_dist/"sing-ruleset"/"combined.json", mode="r") as f:
            assert f.read() == ('{\n'
                                '  "version": 1,\n'
                                '  "rules": [\n'
                                '    {\n'
                                '      "domain": [\n'
                                '        "example.com"\n'
                                '      ],\n'
                                '      "domain_suffix": [\n'
                                '        "example.com"\n'
                                '      ],\n'
                                '      "ip_cidr": [\n'
                                '        "11.4.5.14",\n'
                                '        "fc00:114::514",\n'
                                '        "11.4.5.14",\n'
                                '        "fc00:114::514"\n'
                                '      ]\n'
                                '    }\n'
                                '  ]\n'
                                '}')


class TestMisc:
    def test_is_ipv4addr(self):
        valid_ipaddr = "11.4.5.14"
        invalid_ipaddr_1 = "114.514"
        invalid_ipaddr_2 = "19.1.9.810"
        invalid_ipaddr_3 = "test.www.example.com"
        assert rule.is_ipv4addr(valid_ipaddr)
        assert not rule.is_ipv4addr(invalid_ipaddr_1)
        assert not rule.is_ipv4addr(invalid_ipaddr_2)
        assert not rule.is_ipv4addr(invalid_ipaddr_3)

    def test_is_domain(self):
        valid_domain = "www.example.com"
        invalid_domain_1 = "[invalid]"
        invalid_domain_2 = "-invalid.com"
        invalid_domain_3 = "*.example.com"
        invalid_domain_4 = "www.example.com/error"
        ipv4addr = "11.4.5.14"
        assert rule.is_domain(valid_domain)
        assert not rule.is_domain(invalid_domain_1)
        assert not rule.is_domain(invalid_domain_2)
        assert not rule.is_domain(invalid_domain_3)
        assert not rule.is_domain(invalid_domain_4)
        assert not rule.is_domain(ipv4addr)

    def test_patch(self):
        test_src_patch = Path("tests/src/patch/")
        test_ruleset = RuleSet(RuleSetType.Domain, [Rule(RuleType.DomainFull, "example.com")])
        ruleset.patch(test_ruleset, "patch", test_src_patch)
        assert test_ruleset == RuleSet(RuleSetType.Domain, [Rule(RuleType.DomainSuffix, "example.com")])

    def test_sort(self):
        test_rule_1 = Rule(RuleType.DomainSuffix, "a.example.com", "TEST1")
        test_rule_2 = Rule(RuleType.DomainSuffix, "b.example.com", "TEST2")
        test_ruleset = RuleSet(RuleSetType.Domain, [test_rule_2, test_rule_1])
        test_ruleset.sort()
        assert test_ruleset == RuleSet(RuleSetType.Domain, [test_rule_1, test_rule_2])

    def test_dedup(self):
        test_rule_1 = Rule(RuleType.DomainSuffix, "1.example.com")
        test_rule_2 = Rule(RuleType.DomainSuffix, "a.1.example.com")
        test_rule_3 = Rule(RuleType.DomainFull, "1.example.com")
        test_rule_4 = Rule(RuleType.DomainSuffix, "2.example.com")
        test_rule_5 = Rule(RuleType.DomainSuffix, "a.2.example.com")
        test_rule_6 = Rule(RuleType.DomainFull, "2.example.com")
        test_ruleset = RuleSet(RuleSetType.Domain,
                               [test_rule_1, test_rule_2, test_rule_3, test_rule_4, test_rule_5, test_rule_6])
        test_ruleset.dedup()
        assert test_ruleset == RuleSet(RuleSetType.Domain, [test_rule_1, test_rule_4])
