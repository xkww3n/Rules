import logging
from pathlib import Path
from time import time_ns

import config
from utils import ruleset


def generate():
    logging.info("Start generating custom rulesets.")
    start_time = time_ns()
    list_file_custom = Path.iterdir(config.PATH_SOURCE_CUSTOM)
    for filename in list_file_custom:
        if filename.is_file():
            logging.debug(f'Start generating "{filename.name}".')
            ruleset_custom = ruleset.load(filename)
            ruleset.batch_dump(ruleset_custom, config.TARGETS, config.PATH_DIST, filename.stem)
            logging.debug(f"Generated {len(ruleset_custom)} rules.")
    end_time = time_ns()
    logging.info(f"Finished. Total time: {format((end_time - start_time) / 1e9, '.3f')}s\n")
