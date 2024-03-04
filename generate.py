import logging.config

from Workers import *

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("root")

reject_exclude.generate()
domestic_domain.generate()
domestic_cidr.generate()
telegram_cidr.generate()
v2fly.generate()
personal.generate()
