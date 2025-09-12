import logging
from pathlib import Path

import config
from utils.log_decorator import log
from utils.ruleset import batch_dump
from utils.ruleset import load as ruleset_load


@log
def build():
    """
    custom rulesets
    """

    list_file_custom = Path.iterdir(config.PATH_SOURCE_CUSTOM)
    for filename in list_file_custom:
        if not filename.is_file():
            continue
        logging.debug(f'Build "{filename.name}".')
        ruleset_custom = ruleset_load(filename)
        batch_dump(ruleset_custom, config.TARGETS, config.PATH_DIST, filename.stem)
        logging.debug(f"{len(ruleset_custom)} rules generated.")
