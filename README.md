# Rules
[![Generate](https://github.com/xkww3n/Rules/actions/workflows/main.yml/badge.svg)](https://github.com/xkww3n/Rules/actions/workflows/main.yml)

由 xkww3n 维护的，面向多个代理软件的规则集；注重自动更新、精细化分流及最小化规则体积。每日正午 12:00（UTC）自动更新。

本仓库提供以下格式的规则集：
- 纯文本规则集（Surge 标准，点号通配符）
  - 适用于 [Surge](https://nssurge.com/)（v3 及更新的版本）、[Stash](https://stash.ws/) 和 [Surfboard](https://getsurfboard.com)。
- 纯文本规则集（Clash 标准，加号通配符）
  - 适用于 Clash Premium（2023.04.13 及更新的版本）和 Clash Meta（v1.14.4 及更新的版本）。
- YAML 规则集
  - 适用于 Clash Premium、Clash Meta 和 [Stash](https://stash.ws/)。
- Clash 传统规则集
  - 适用于兼容传统 Clash 规则的代理软件，如 [Quantumult](https://quantumult.app/) [(X)](https://quantumult.app/x/)。
- Surge 传统规则集
  - 适用于兼容传统 Surge 规则的代理软件，如低于 v3 版本的 Surge、[Loon](https://www.nsloon.com/)、[Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118) 和 [LanceX](https://shadowboat.app/lancex/)。
- V2Ray GeoSite/GeoIP 数据库
  - 适用于 [V2Ray](https://www.v2fly.org/)。
    - GeoSite 数据库：<https://rules.xkww3n.cyou/geosite.dat>
    - GeoIP 数据库：<https://rules.xkww3n.cyou/geoip.dat>
- ~~sing-box GeoSite/GeoIP 数据库~~ 该类型已在 sing-box v1.8.0 中被弃用，请改用规则集。参阅：<https://sing-box.sagernet.org/migration/>
  - ~~适用于 [sing-box](https://sing-box.sagernet.org/)。~~
    - ~~GeoSite 数据库：<https://rules.xkww3n.cyou/geosite.db>~~
    - ~~GeoIP 数据库：<https://rules.xkww3n.cyou/geoip.db>~~
- sing-box 规则集
  - 适用于 [sing-box](https://sing-box.sagernet.org/)。
- MaxMind MMDB 数据库
  - GeoIP 数据库：<https://rules.xkww3n.cyou/geoip.mmdb>

## 文档
请查看[本项目的 GitHub Wiki](https://github.com/xkww3n/Rules/wiki)

## 许可证
如无特别声明，本项目的一切内容均使用 MIT 许可证授权。

## 鸣谢
本项目离不开其他优质开源项目的支持，在此对这些项目表示感谢：
- [AdGuard Content Blocking Filters](https://github.com/AdguardTeam/AdguardFilters/)
- [EasyList](https://easylist.to)
- [もちフィルタ](https://eeii0a5l.github.io/mochifilter_homepage/mochi.html)
- [ADgk](https://github.com/banbendalao/ADgk)
- [-AWAvenue 秋风广告规则（AWAvenue-Adblock-Rule）-](https://github.com/TG-Twilight/AWAvenue-Adblock-Rule)
- [乘风广告过滤规则](https://github.com/xinggsf/Adblock-Plus-Rule/)
- [d3Host List by d3ward](https://github.com/d3ward/toolz/blob/master/src/d3host.adblock)
- [Domain list community](https://github.com/v2fly/domain-list-community)
- [dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)
- [chnroutes2 (better-aggregated chnroutes)](https://github.com/misakaio/chnroutes2/)
- [中国运营商IP地址库](https://github.com/gaoyifan/china-operator-ip)
- [aggregate6](https://github.com/job/aggregate6)
- [python-abp](https://hg.adblockplus.org/python-abp/)
- [Loyalsoldier / domain-list-custom](https://github.com/Loyalsoldier/domain-list-custom/)
- [Loyalsoldier / geoip](https://github.com/Loyalsoldier/geoip/)
- [SagerNet / sing-geosite](https://github.com/sagernet/sing-geosite/)
- [SagerNet / sing-geoip](https://github.com/sagernet/sing-geoip/)
