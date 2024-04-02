import logging

from requests import Session

import config
from models.rule import Rule
from models.ruleset import RuleSet
from utils import ruleset
from workers.log_decoration import log


@log
def build():
    connection = Session()

    src_cidr = connection.get(config.URL_DOMESTIC_IP_V4).text.splitlines()
    ruleset_cidr = RuleSet("IPCIDR", [])
    for line in src_cidr:
        if not line.startswith("#"):
            ruleset_cidr.add(Rule("IPCIDR", line))
    logging.info(f"Processed {len(ruleset_cidr)} domestic IPv4 rules.")

    ruleset.batch_dump(ruleset_cidr, config.TARGETS, config.PATH_DIST, "domestic_ip")

    src_cidr6 = connection.get(config.URL_DOMESTIC_IP_V6).text.splitlines()
    ruleset_cidr6 = RuleSet("IPCIDR", [])
    for line in src_cidr6:
        ruleset_cidr6.add(Rule("IPCIDR6", line))
    logging.info(f"Processed {len(ruleset_cidr6)} domestic IPv6 rules.")

    ruleset.batch_dump(ruleset_cidr6, config.TARGETS, config.PATH_DIST, "domestic_ip6")
