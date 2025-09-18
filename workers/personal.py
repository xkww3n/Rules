import logging
from pathlib import Path

import config
from utils.ruleset import batch_dump
from utils.ruleset import load as ruleset_load


def build():
    # There's no personal classical type ruleset. So no logic about that.
    list_file_personal = Path.glob(config.PATH_SOURCE_CUSTOM/"personal", "*.txt")
    for filename in list_file_personal:
        logging.debug(f'Build "{filename.name}".')
        ruleset_personal = ruleset_load(filename)
        batch_dump(ruleset_personal, ["text", "text-plus", "yaml", "classical", "quantumult"],
                   config.PATH_DIST/"personal", filename.stem)
