import logging.config
from importlib.util import spec_from_file_location, module_from_spec
from os import environ
from pathlib import Path

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("root")

if environ.get("DEBUG"):
    logger.setLevel("DEBUG")

workers = Path("workers").rglob("*.py")
for worker in workers:
    worker_name = worker.stem
    spec = spec_from_file_location(worker_name, Path("workers")/worker.name)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    module.build()
