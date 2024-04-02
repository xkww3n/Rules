import config
from utils import geosite
from workers.log_decoration import log


@log
def build():
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
