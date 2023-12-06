from pathlib import Path

from Utils import const, rule, ruleset


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

    def test_load_domain(self):
        test_src_path = Path("./src/custom_ruleset/")
        loaded_ruleset = ruleset.load(test_src_path / "domain.txt")
        assert loaded_ruleset == ruleset.RuleSet("Domain",
                                                 [rule.Rule("DomainSuffix", "example.com"),
                                                  rule.Rule("DomainFull", "example.com")])

    def test_load_ipcidr(self):
        test_src_path = Path("./src/custom_ruleset/")
        loaded_ruleset = ruleset.load(test_src_path / "ipcidr.txt")
        assert loaded_ruleset == ruleset.RuleSet("IPCIDR",
                                                 [rule.Rule("IPCIDR", "11.4.5.14"),
                                                  rule.Rule("IPCIDR6", "fc00:114::514")])

    def test_load_combined(self):
        test_src_path = Path("./src/custom_ruleset/")
        loaded_ruleset = ruleset.load(test_src_path / "combined.txt")
        assert loaded_ruleset == ruleset.RuleSet("Combined",
                                                 [rule.Rule("DomainFull", "example.com"),
                                                  rule.Rule("DomainSuffix", "example.com"),
                                                  rule.Rule("IPCIDR", "11.4.5.14"),
                                                  rule.Rule("IPCIDR6", "fc00:114::514")])

    def test_patch(self):
        test_src_patch = Path("./src/patch/")
        test_ruleset = ruleset.RuleSet("Domain", [rule.Rule("DomainFull", "example.com")])
        ruleset.patch(test_ruleset, "patch", test_src_patch)
        assert test_ruleset == ruleset.RuleSet("Domain", [rule.Rule("DomainSuffix", "example.com")])

    def test_dump_domain(self):
        test_dist = Path("./dists/")
        ruleset_domain = ruleset.load(Path("./src/custom_ruleset/domain.txt"))
        ruleset.batch_dump(ruleset_domain, const.TARGETS, test_dist, "domain")

        assert (test_dist/"text"/"domain.txt").exists()
        with open(test_dist/"text"/"domain.txt", mode="r") as f:
            assert f.read() == (".example.com\n"
                                "example.com\n")

        assert (test_dist/"text-plus"/"domain.txt").exists()
        with open(test_dist/"text-plus"/"domain.txt", mode="r") as f:
            assert f.read() == ("+.example.com\n"
                                "example.com\n")

        assert (test_dist/"clash-compatible"/"domain.txt").exists()
        with open(test_dist/"clash-compatible"/"domain.txt", mode="r") as f:
            assert f.read() == ("DOMAIN-SUFFIX,example.com,Policy\n"
                                "DOMAIN,example.com,Policy\n")

        assert (test_dist/"surge-compatible"/"domain.txt").exists()
        with open(test_dist/"surge-compatible"/"domain.txt", mode="r") as f:
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
                                '        ".example.com"\n'
                                '      ],\n'
                                '      "domain": [\n'
                                '        "example.com"\n'
                                '      ]\n'
                                '    }\n'
                                '  ]\n'
                                '}')

    def test_dump_ipcidr(self):
        test_dist = Path("./dists/")
        ruleset_ipcidr = ruleset.load(Path("./src/custom_ruleset/ipcidr.txt"))
        ruleset.batch_dump(ruleset_ipcidr, const.TARGETS, test_dist, "ipcidr")

        assert not (test_dist/"text-plus"/"ipcidr.txt").exists()
        assert not (test_dist/"geosite"/"ipcidr").exists()

        assert (test_dist/"text"/"ipcidr.txt").exists()
        with open(test_dist/"text"/"ipcidr.txt", mode="r") as f:
            assert f.read() == ("11.4.5.14\n"
                                "fc00:114::514\n")

        assert (test_dist/"clash-compatible"/"ipcidr.txt").exists()
        with open(test_dist/"clash-compatible"/"ipcidr.txt", mode="r") as f:
            assert f.read() == ("IP-CIDR,11.4.5.14,Policy\n"
                                "IP-CIDR6,fc00:114::514,Policy\n")

        assert (test_dist/"surge-compatible"/"ipcidr.txt").exists()
        with open(test_dist/"surge-compatible"/"ipcidr.txt", mode="r") as f:
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
        test_dist = Path("./dists/")
        ruleset_combined = ruleset.load(Path("./src/custom_ruleset/combined.txt"))
        ruleset.batch_dump(ruleset_combined, const.TARGETS, test_dist, "combined")

        assert not (test_dist/"text"/"combined.txt").exists()
        assert not (test_dist/"text-plus"/"combined.txt").exists()
        assert not (test_dist/"geosite"/"combined").exists()

        assert (test_dist/"clash-compatible"/"combined.txt").exists()
        with open(test_dist/"clash-compatible"/"combined.txt", mode="r") as f:
            assert f.read() == ("DOMAIN,example.com,Policy\n"
                                "DOMAIN-SUFFIX,example.com,Policy\n"
                                "IP-CIDR,11.4.5.14,Policy\n"
                                "IP-CIDR6,fc00:114::514,Policy\n")

        assert (test_dist/"surge-compatible"/"combined.txt").exists()
        with open(test_dist/"surge-compatible"/"combined.txt", mode="r") as f:
            assert f.read() == ("DOMAIN,example.com\n"
                                "DOMAIN-SUFFIX,example.com\n"
                                "IP-CIDR,11.4.5.14\n"
                                "IP-CIDR6,fc00:114::514\n")

        assert (test_dist/"yaml"/"combined.yaml").exists()
        with open(test_dist/"yaml"/"combined.yaml", mode="r") as f:
            assert f.read() == ("payload:\n"
                                "  - 'DOMAIN,example.com'\n"
                                "  - 'DOMAIN-SUFFIX,example.com'\n"
                                "  - 'IP-CIDR,11.4.5.14'\n"
                                "  - 'IP-CIDR6,fc00:114::514'\n")

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
                                '        ".example.com"\n'
                                '      ],\n'
                                '      "ip_cidr": [\n'
                                '        "11.4.5.14",\n'
                                '        "fc00:114::514"\n'
                                '      ]\n'
                                '    }\n'
                                '  ]\n'
                                '}')
