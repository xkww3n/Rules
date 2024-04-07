import logging
from pathlib import Path

import config
from utils import ruleset
from utils.log_decorator import log


@log
def build():
    """
    custom rulesets
    """

    list_file_custom = Path.iterdir(config.PATH_SOURCE_CUSTOM)
    for filename in list_file_custom:
        if filename.is_file():
            logging.debug(f'Build "{filename.name}".')
            ruleset_custom = ruleset.load(filename)
            ruleset.batch_dump(ruleset_custom, config.TARGETS, config.PATH_DIST, filename.stem)
            logging.debug(f"Processed {len(ruleset_custom)} rules.")
