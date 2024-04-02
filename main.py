import logging.config
from os import environ

from workers import *

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("root")

if environ.get("DEBUG"):
    logger.setLevel("DEBUG")

reject_exclude.build("reject and exclude ruleset")
domestic_domain.build("domestic ruleset")
domestic_cidr.build("domestic CIDR ruleset")
telegram_cidr.build("Telegram CIDR ruleset")
v2fly.build("v2fly community rulesets")
custom.build("custom rulesets")
personal.build()
