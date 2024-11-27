from pathlib import Path

TARGETS = ["text", "text-plus", "yaml", "surge-compatible", "clash-compatible", "geosite", "sing-ruleset"]
PATH_SOURCE_GEOSITE = Path("domain-list-community/data/")
PATH_SOURCE_CUSTOM = Path("source/")
PATH_SOURCE_PATCH = Path("source/patches/")
PATH_DIST = Path("dists/")

LIST_REJECT_URL = [
    # AdGuard Base Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt",
    # AdGuard Mobile Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt",
    # AdGuard third-party
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers_firstparty.txt",
    # AdGuard CNAME
    "https://raw.githubusercontent.com/AdguardTeam/cname-trackers/master/data/combined_disguised_ads_justdomains.txt",
    # EasyList China
    "https://easylist-downloads.adblockplus.org/easylistchina.txt",
    # EasyList third-party
    "https://raw.githubusercontent.com/easylist/easylist/master/easylist/easylist_thirdparty.txt",
    # EasyList adult third-party
    "https://raw.githubusercontent.com/easylist/easylist/master/easylist_adult/adult_thirdparty.txt",
    # もちフィルタ
    "https://raw.githubusercontent.com/eEIi0A5L/adblock_filter/master/mochi_filter.txt",
    # AWAvenue 秋风广告规则
    "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
    # d3Host List by d3ward
    "https://raw.githubusercontent.com/d3ward/toolz/master/src/d3host.adblock",
    # NextDNS native-tracking-domains
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/alexa",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/apple",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/huawei",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/roku",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/samsung",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/sonos",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/windows",
    "https://raw.githubusercontent.com/nextdns/native-tracking-domains/main/domains/xiaomi",
    # NoCoin
    "https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt",
    # CoinBlockerLists
    "https://zerodot1.gitlab.io/CoinBlockerLists/list_browser_AdBlock.txt"
]

# AdGuard DNS Filter Whitelist
LIST_EXCL_URL = [
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt"
]

URL_DOMESTIC_IP_V4 = "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china.txt"
URL_DOMESTIC_IP_V6 = "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china6.txt"
