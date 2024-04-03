import importlib.util as iu
import logging.config
from os import environ
from pathlib import Path

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("root")

if environ.get("DEBUG"):
    logger.setLevel("DEBUG")

workers = Path("workers").rglob("*.py")
for worker in workers:
    worker_name = worker.stem
    spec = iu.spec_from_file_location(worker_name, Path("workers")/worker.name)
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.build()
