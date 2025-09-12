import logging.config
from importlib.util import spec_from_file_location, module_from_spec
from os import environ
from pathlib import Path

logging.config.fileConfig("logging.ini")
logger = logging.getLogger("root")

if environ.get("DEBUG"):
    logger.setLevel("DEBUG")

workers = sorted(Path("workers").glob("*.py"))  # Use glob instead of rglob, sorted for consistent order
for worker in workers:
    worker_name = worker.stem
    spec = spec_from_file_location(worker_name, worker)
    if spec is None:
        logger.warning(f"Could not load spec for worker {worker_name}")
        continue
    if spec.loader is None:
        logger.warning(f"No loader found for worker {worker_name}")
        continue
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    module.build()
