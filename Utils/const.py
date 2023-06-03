from pathlib import Path

TARGETS = ["text", "text-plus", "yaml", "surge-compatible", "clash-compatible"]
PATH_DOMAIN_LIST = Path("./domain-list-community/data/")
PATH_CUSTOM_BUILD = Path("./Source/")
PATH_CUSTOM_APPEND = Path("./Custom/Append/")
PATH_CUSTOM_REMOVE = Path("./Custom/Remove/")
PATH_DIST = Path("./dists/")

LIST_REJECT_URL = [
    # AdGuard Base Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt",
    # Easylist China
    "https://easylist-downloads.adblockplus.org/easylistchina.txt",
    # もちフィルタ
    "https://raw.githubusercontent.com/eEIi0A5L/adblock_filter/master/mochi_filter.txt",
    # AdGuard Mobile Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt",
    # ADgk
    "https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt",
]

# AdGuard DNS Filter Whitelist
LIST_EXCL_URL = [
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt",
]
