import logging
from time import time_ns

from requests import Session

import config
from Models.rule import Rule
from Models.ruleset import RuleSet
from Utils import ruleset


def generate():
    logging.info("Start generating Telegram CIDR ruleset.")
    start_time = time_ns()
    connection = Session()

    src_cidr = connection.get("https://core.telegram.org/resources/cidr.txt").text.splitlines()
    ruleset_cidr = RuleSet("IPCIDR", [])
    for line in src_cidr:
        if ":" not in line:
            ruleset_cidr.add(Rule("IPCIDR", line))
        else:
            ruleset_cidr.add(Rule("IPCIDR6", line))

    ruleset.batch_dump(ruleset_cidr, config.TARGETS, config.PATH_DIST, "telegram")

    end_time = time_ns()
    logging.info(f"Finished. Total time: {format((end_time - start_time) / 1e9, '.3f')}s\n")
