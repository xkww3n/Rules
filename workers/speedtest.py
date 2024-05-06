from json import loads as json_loads
from time import sleep

from requests import Session

import config
from models.rule import Rule
from models.ruleset import RuleSet
from utils.log_decorator import log
from utils.ruleset import dedup, batch_dump


@log
def build():
    """
    common internet speed testing servers ruleset
    """
    accepted_ccs = ["CN", "HK", "TW", "MO", "JP", "US", "SG", "GB", "TR"]
    search_keywords = [
        "China",
        "China Mobile",
        "China Unicom",
        "China Telecom",
        "联通",
        "电信",
        "5G",
        "Beijing",

        "Hong Kong",
        "Taiwan",
        "Macau",
        "Japan",
        "Singapore",

        "United Kingdom",
        "London",
        "Manchester",

        "United States",
        "New York",
        "Los Angeles",
        "Miami",
        "San Jose",
        "Dallas",
        "Seattle",
        "fdcservers",
        "GCI",
        "Hivelocity",

        "Turkey",
        "Posive",
        "DuruNet",
        "Turkcell",
        "Turk Telekom"
    ]

    connection = Session()
    speedtest_ruleset = RuleSet("Domain", [
        Rule("DomainSuffix", "ooklaserver.net"),
        Rule("DomainSuffix", "speed.cloudflare.com"),
        Rule("DomainSuffix", "fast.com")
    ])

    for keyword in search_keywords:
        url = f"https://www.speedtest.net/api/js/servers?engine=js&search={keyword}&limit=100"
        resp = connection.get(url).text
        sleep(0.5)  # Speedtest.net's private API interface has a rate limit
        servers_list = json_loads(resp)
        for server_info in servers_list:
            if server_info["cc"] not in accepted_ccs:
                continue
            server_domain = server_info["host"].split(":")[0]
            speedtest_rule = Rule("DomainFull", server_domain)
            speedtest_ruleset.add(speedtest_rule)

    dedup(speedtest_ruleset)
    batch_dump(speedtest_ruleset, config.TARGETS, config.PATH_DIST, "speedtest")
