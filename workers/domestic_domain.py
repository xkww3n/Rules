import logging

from requests import Session

import config
from models.rule import Rule
from utils.geosite import parse
from utils.log_decorator import log
from utils.ruleset import patch, dedup, batch_dump


@log
def build():
    """
    domestic ruleset
    """

    connection = Session()

    ruleset_domestic = parse(config.PATH_SOURCE_GEOSITE/"geolocation-cn", None, ["!cn"])
    logging.info(f"Imported {len(ruleset_domestic)} domestic rules from v2fly geolocation-cn list.")

    for item in ruleset_domestic.deepcopy():
        tld_overseas = (".hk", ".kr", ".my", ".sg", ".au", ".tw", ".in", ".ru", ".us", ".fr", ".th", ".id", ".jp")
        if any(item.Payload.endswith(os_tld) for os_tld in tld_overseas):
            ruleset_domestic.remove(item)
            logging.debug(f"{item} removed for having a overseas TLD.")

    # Import dnsmasq-china-list
    raw = connection.get(
        "https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/apple.china.conf").text
    for line in raw.replace("server=/", "").replace("/114.114.114.114", "").splitlines():
        ruleset_domestic.add(Rule("DomainFull", line))

    ruleset_domestic = patch(ruleset_domestic, "domestic")

    # Add all domestic TLDs to domestic rules, then perform deduplication.
    ruleset_domestic_tlds = parse(config.PATH_SOURCE_GEOSITE/"tld-cn")
    logging.info(f"Imported {len(ruleset_domestic_tlds)} domestic TLDs.")
    ruleset_domestic |= ruleset_domestic_tlds
    dedup(ruleset_domestic)
    logging.info(f"Processed {len(ruleset_domestic)} domestic rules.")
    batch_dump(ruleset_domestic, config.TARGETS, config.PATH_DIST, "domestic")
