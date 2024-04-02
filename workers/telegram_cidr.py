from requests import Session

import config
from models.rule import Rule
from models.ruleset import RuleSet
from utils import ruleset
from workers.log_decoration import log


@log
def build():
    connection = Session()

    src_cidr = connection.get("https://core.telegram.org/resources/cidr.txt").text.splitlines()
    ruleset_cidr = RuleSet("IPCIDR", [])
    for line in src_cidr:
        if ":" not in line:
            ruleset_cidr.add(Rule("IPCIDR", line))
        else:
            ruleset_cidr.add(Rule("IPCIDR6", line))

    ruleset.batch_dump(ruleset_cidr, config.TARGETS, config.PATH_DIST, "telegram")
