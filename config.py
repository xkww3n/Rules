from pathlib import Path

TARGETS = ["text", "text-plus", "yaml", "classical", "quantumult", "geosite", "sing-ruleset"]
PATH_SOURCE_GEOSITE = Path("domain-list-community/data/")
PATH_SOURCE_CUSTOM = Path("source/")
PATH_SOURCE_PATCH = Path("source/patches/")
PATH_DIST = Path("dists/")

LIST_REJECT_URL = [
    # AdGuard Base Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers_firstparty.txt",
    # AdGuard Mobile Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt",
    # AdGuard Japanese
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/JapaneseFilter/sections/adservers.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/JapaneseFilter/sections/adservers_firstparty.txt",
    # AdGuard Tracking Protection Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/SpywareFilter/sections/tracking_servers_firstparty.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/SpywareFilter/sections/mobile.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/SpywareFilter/sections/tracking_servers.txt",
    # AdGuard DNS Additional Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/rules.txt",
    # EasyList China
    "https://easylist-downloads.adblockplus.org/easylistchina.txt",
    # EasyList
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_adservers.txt",
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_adservers_popup.txt",
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_thirdparty.txt",
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_thirdparty_popup.txt",
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_specific_block.txt",
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist/easylist_specific_block_popup.txt",
    # EasyList adult
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist_adult/adult_thirdparty.txt",
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist_adult/adult_thirdparty_popup.txt",
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist_adult/adult_adservers_popup.txt",
    "https://raw.githubusercontent.com/easylist/easylist/refs/heads/master/easylist_adult/adult_specific_block.txt",
    # AWAvenue 秋风广告规则
    "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Adguard-Only.Ads.txt",
    # NoCoin
    "https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt",
]

# AdGuard DNS Filter Whitelist
LIST_EXCL_URL = [
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt",
]

URL_DOMESTIC_IP_V4 = "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china.txt"
URL_DOMESTIC_IP_V6 = "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china6.txt"
