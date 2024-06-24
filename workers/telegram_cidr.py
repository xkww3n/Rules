from requests import Session

import config
from models.rule import Rule, RuleType
from models.ruleset import RuleSet, RuleSetType
from utils.log_decorator import log
from utils.ruleset import batch_dump


@log
def build():
    """
    Telegram CIDR ruleset
    """

    connection = Session()

    src_cidr = connection.get("https://core.telegram.org/resources/cidr.txt").text.splitlines()
    ruleset_cidr = RuleSet(RuleSetType.IPCIDR, [])
    for line in src_cidr:
        if ":" not in line:
            ruleset_cidr.add(Rule(RuleType.IPCIDR, line))
        else:
            ruleset_cidr.add(Rule(RuleType.IPCIDR6, line))

    batch_dump(ruleset_cidr, config.TARGETS, config.PATH_DIST, "telegram")
