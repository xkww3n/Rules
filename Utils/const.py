from pathlib import Path


TARGETS = ["text", "text-plus", "yaml", "surge-compatible", "clash-compatible"]
PATH_DOMAIN_LIST = Path("./domain-list-community/data/")
PATH_CUSTOM_BUILD = Path("./Source/")
PATH_CUSTOM_APPEND = Path("./Custom/Append/")
PATH_CUSTOM_REMOVE = Path("./Custom/Remove/")
PATH_DIST = Path("./dists/")

## AdGuard Base Filter
URL_BASE = "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt"
## Easylist China
URL_CN = "https://easylist-downloads.adblockplus.org/easylistchina.txt"
## もちフィルタ
URL_JP = "https://raw.githubusercontent.com/eEIi0A5L/adblock_filter/master/mochi_filter.txt"
## AdGuard Mobile Filter
URL_MOBILE = "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt"
## ADgk
URL_CN_EXTEND = "https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt"
## AdGuard DNS Filter Whitelist
URL_EXCLUSIONS_1 = "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt"
URL_EXCLUSIONS_2 = "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt"
