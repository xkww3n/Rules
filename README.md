# Rules

[![Generate](https://github.com/xkww3n/Rules/actions/workflows/main.yml/badge.svg)](https://github.com/xkww3n/Rules/actions/workflows/main.yml)

由 xkww3n 维护的，面向多个代理软件的规则集；注重自动更新、精细化分流及最小化规则体积。每日正午 12:00（UTC）自动更新。

本仓库提供以下格式的规则集：

- 纯文本规则集（Surge 标准，点号通配符）
    - 适用于 [Surge](https://nssurge.com/)（v3
      及更新的版本）、[Stash](https://stash.ws/)、[Surfboard](https://getsurfboard.com)
      和 [Egern](https://apps.apple.com/us/app/egern/id1616105820)。
- 纯文本规则集（Clash 标准，加号通配符）
    - 适用于 Clash Premium（2023.04.13 及更新的版本）和 Clash Meta（v1.14.4 及更新的版本）。
- YAML 规则集
    - 适用于 Clash Premium、Clash Meta 和 [Stash](https://stash.ws/)。
- Quantumult 规则集
    - 适用于 [Quantumult](https://quantumult.app/) 和 [Quantumult X](https://quantumult.app/x/)。
- 传统规则集
    - 适用于兼容传统 Surge 规则的代理软件，如低于 v3 版本的
      Surge、[Loon](https://www.nsloon.com/)、[Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118)
      和 [LanceX](https://shadowboat.app/lancex/)。
- V2Ray GeoSite/GeoIP 数据库
    - 适用于 [V2Ray](https://www.v2fly.org/)。
    - GeoSite 数据库：<https://rules.xkww3n.cyou/geosite.dat>
    - GeoIP 数据库：<https://cdn.xkww3n.cyou/geoip.dat>（<https://rules.xkww3n.cyou/geoip.dat> 会重定向至此），使用 IPinfo Lite 数据生成
        - 小体积简化版：<https://rules.xkww3n.cyou/geoip_lite.dat>，使用 MaxMind GeoLite 与其他数据源混合生成
- ~~sing-box GeoSite/GeoIP 数据库~~ 该类型已在 sing-box v1.8.0 中被弃用，请改用规则集。参阅：<https://sing-box.sagernet.org/migration/>
- sing-box 规则集
    - 适用于 [sing-box](https://sing-box.sagernet.org/)。
- MaxMind MMDB 数据库
    - GeoIP 数据库：<https://cdn.xkww3n.cyou/geoip.mmdb>（<https://rules.xkww3n.cyou/geoip.mmdb> 会重定向至此），使用 IPinfo Lite 数据生成
    - 小体积简化版：<https://rules.xkww3n.cyou/geoip_lite.mmdb>，使用 MaxMind GeoLite 与其他数据源混合生成


## 文档

请查看[本项目的 GitHub Wiki](https://github.com/xkww3n/Rules/wiki)

## 许可证

如无特别声明，本项目的一切内容均使用 MIT 许可证授权。

## 致谢

本项目离不开其他优质开源项目的支持，请前往 [本项目的 GitHub Wiki](https://github.com/xkww3n/Rules/wiki/致谢) 查看致谢名单。
