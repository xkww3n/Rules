import logging.config
from os import environ

from workers import *

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("root")

if environ.get("DEBUG"):
    logger.setLevel("DEBUG")

reject_exclude.build()
domestic_domain.build()
domestic_cidr.build()
telegram_cidr.build()
v2fly.build()
custom.build()
personal.build()
