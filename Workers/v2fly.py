import logging
from time import time_ns

import config
from Utils import geosite


def generate():
    logging.info("Start generating v2fly community rulesets.")
    start_time = time_ns()

    categories = [
        "bahamut",
        "bing",
        "dmm",
        "googlefcm",
        "microsoft",
        "niconico",
        "openai",
        "paypal",
        "youtube",
    ]
    exclusions = [
        "github",  # GitHub's domains are included in "microsoft", but its connectivity mostly isn't as high as
        # Microsoft.
        "bing",  # Bing has a more restricted ver for Mainland China.
    ]
    geosite.batch_gen(categories, config.TARGETS, exclusions)

    end_time = time_ns()
    logging.info(f"Finished. Total time: {format((end_time - start_time) / 1e9, '.3f')}s\n")
