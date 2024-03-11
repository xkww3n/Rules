import logging
from pathlib import Path

import config
from Utils import ruleset


def generate():
    # There's no personal classical type ruleset. So no logic about that.
    list_file_personal = Path.iterdir(config.PATH_SOURCE_CUSTOM/"personal")
    for filename in list_file_personal:
        logging.debug(f'Start generating "{filename.name}".')
        ruleset_personal = ruleset.load(filename)
        ruleset.batch_dump(ruleset_personal, ["text", "text-plus", "yaml", "surge-compatible", "clash-compatible"],
                           config.PATH_DIST/"personal", filename.stem)
