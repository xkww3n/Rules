from pathlib import Path

TARGETS = ["text", "text-plus", "yaml", "surge-compatible", "clash-compatible", "geosite", "sing-ruleset"]
PATH_SOURCE_GEOSITE = Path("domain-list-community/data/")
PATH_SOURCE_CUSTOM = Path("source/")
PATH_SOURCE_PATCH = Path("source/patches/")
PATH_DIST = Path("dists/")

LIST_REJECT_URL = [
    # AdGuard Base Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/BaseFilter/sections/adservers.txt",
    # Easylist China
    "https://easylist-downloads.adblockplus.org/easylistchina.txt",
    # もちフィルタ
    "https://raw.githubusercontent.com/eEIi0A5L/adblock_filter/master/mochi_filter.txt",
    # AdGuard Mobile Filter
    "https://raw.githubusercontent.com/AdguardTeam/AdguardFilters/master/MobileFilter/sections/adservers.txt",
    # AWAvenue 秋风广告规则
    "https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
    # 乘风 视频过滤规则
    "https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt",
    # d3Host List by d3ward
    "https://raw.githubusercontent.com/d3ward/toolz/master/src/d3host.adblock"
]

# AdGuard DNS Filter Whitelist
LIST_EXCL_URL = [
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exceptions.txt",
    "https://raw.githubusercontent.com/AdguardTeam/AdGuardSDNSFilter/master/Filters/exclusions.txt"
]

URL_DOMESTIC_IP_V4 = "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china.txt"
URL_DOMESTIC_IP_V6 = "https://raw.githubusercontent.com/gaoyifan/china-operator-ip/ip-lists/china6.txt"

RULE_TYPE_CONVERSION = {
    "DOMAIN": "DomainFull",
    "DOMAIN-SUFFIX": "DomainSuffix",
    "IP-CIDR": "IPCIDR",
    "IP-CIDR6": "IPCIDR6"
}
