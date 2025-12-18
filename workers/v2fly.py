import config
from utils.geosite import batch_gen
from utils.log_decorator import log


@log
def build():
    """
    v2fly community rulesets
    """

    categories = [
        "anthropic",
        "bahamut",
        "bing",
        "dmm",
        "google",
        "googlefcm",
        "google-deepmind",
        "microsoft",
        "niconico",
        "openai",
        "paypal",
        "youtube",
        "line",
        "instagram"
    ]
    exclusions = [
        "github",  # GitHub's domains are included in "microsoft", but its connectivity mostly isn't as high as
                   # Microsoft.
        "bing",  # Bing has a more restricted ver for Mainland China.
    ]
    batch_gen(categories, config.TARGETS, exclusions)
