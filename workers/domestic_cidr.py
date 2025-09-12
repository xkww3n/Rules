import logging

from requests import Session

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType
from utils.log_decorator import log
from utils.ruleset import batch_dump


@log
def build():
    """
    domestic CIDR ruleset
    """

    connection = Session()

    src_cidr = connection.get(config.URL_DOMESTIC_IP_V4).text.splitlines()
    ruleset_cidr = RuleSet(RuleSetType.IPCIDR, [])
    for line in src_cidr:
        if line.startswith("#"):
            continue
        ruleset_cidr.add(Rule(RuleType.IPCIDR, line))
    logging.info(f"{len(ruleset_cidr)} domestic IPv4 rules generated.")

    batch_dump(ruleset_cidr, config.TARGETS, config.PATH_DIST, "domestic_ip")

    src_cidr6 = connection.get(config.URL_DOMESTIC_IP_V6).text.splitlines()
    ruleset_cidr6 = RuleSet(RuleSetType.IPCIDR, [])
    for line in src_cidr6:
        ruleset_cidr6.add(Rule(RuleType.IPCIDR6, line))
    logging.info(f"{len(ruleset_cidr6)} domestic IPv6 rules generated.")

    batch_dump(ruleset_cidr6, config.TARGETS, config.PATH_DIST, "domestic_ip6")
