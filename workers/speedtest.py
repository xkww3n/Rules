import logging
from json import loads as json_loads
from concurrent.futures import ThreadPoolExecutor

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType
from utils.log_decorator import log
from utils.ruleset import batch_dump


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
    retry_strategy = Retry(
        total=4,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=2,
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
    connection.mount('https://', adapter)

    speedtest_ruleset = RuleSet(RuleSetType.Domain, [
        Rule(RuleType.DomainSuffix, "speedtest.net"),
        Rule(RuleType.DomainSuffix, "speedtestcustom.com"),
        Rule(RuleType.DomainSuffix, "ooklaserver.net"),
        Rule(RuleType.DomainSuffix, "speed.cloudflare.com")
    ])

    def process_keyword(keyword):
        logging.debug(f'Using keyword "{keyword}"')
        url = f"https://www.speedtest.net/api/js/servers?engine=js&search={keyword}&limit=100"
        resp = connection.get(url).text
        servers_list = json_loads(resp)

        acceptable_servers = [
            server_info for server_info in servers_list 
            if server_info["cc"] in accepted_ccs
        ]
        logging.debug(f"Retrieved {len(servers_list)} servers, {len(acceptable_servers)} acceptable.")

        new_rules = []
        for server_info in acceptable_servers:
            server_domain = server_info["host"].split(":")[0]
            new_rules.append(Rule(RuleType.DomainFull, server_domain))
            logging.debug(f'Added "{server_domain}"')

        return new_rules

    with ThreadPoolExecutor(max_workers=min(len(search_keywords), 10)) as executor:
        all_rules = executor.map(process_keyword, search_keywords)
        
        for rules in all_rules:
            for rule in rules:
                speedtest_ruleset.add(rule)

    speedtest_ruleset.dedup()
    batch_dump(speedtest_ruleset, config.TARGETS, config.PATH_DIST, "speedtest")
    logging.info(f"{len(speedtest_ruleset)} speed testing rules generated.")
