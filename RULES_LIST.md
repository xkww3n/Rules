# 规则集列表
**⚠注意：规则集文件的路径或文件名在需要时可能会发生更改。更改后，旧路径/文件名将继续保留 30 天作为缓冲期。在此期间，建议尽早更新至新路径/文件名。30 天后，旧路径/名称将不再可用，代理软件试图更新时将会报错。⚠**

当前处于缓冲期的路径/文件名：

| 类型 | 旧                                    | 新                                   | 过期日期        |
|------|---------------------------------------|--------------------------------------|-----------------|
| 路径 | https://rules.xkww3n.cyou/ **surge/** | https://rules.xkww3n.cyou/ **text/** | 2023.6.14 UTC+8 |
| 路径 | https://rules.xkww3n.cyou/ **clash/** | https://rules.xkww3n.cyou/ **yaml/** | 2023.6.14 UTC+8 |

## 广告服务与跟踪器拦截
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/reject.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/reject.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/reject.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/reject.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/reject.txt>

- 自动生成
- 拦截在中国与日本常见的广告提供商和跟踪服务商的服务域名。
- **不**拦截这些服务商面向其接入客户的域名（如：官网、控制台）。如果两者相同，将不会拦截。
- 应当放在**所有非拦截类规则列表之前**
- 数据来源：
  - [本仓库](./Custom/)
  - [AdGuard](https://github.com/AdguardTeam/AdguardFilters)
  - [banbendalao / ADgk](https://github.com/banbendalao/ADgk/)
  - [EasyList China](https://github.com/easylist/easylistchina)
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)
  - [もちフィルタ](https://eeii0a5l.github.io/mochifilter_homepage/mochi.html)

### 排除项
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/exclude.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/exclude.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/exclude.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/exclude.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/exclude.txt>

- 自动生成
- 包含一些不应被拦截规则拦截的域名。
  - 如：拦截规则拦截了 `googleadservices.com` 域名，这个域名的许多子域名都被用于推送广告，因此将这个域名纳入拦截列表完全合理。但是，`www.googleadservices.com` 这个子域名用于 Google 搜索引擎中广告条目的跳转，不应被拦截；所以，此域名被纳入排除规则中。
- 应当放在**拦截规则列表之前**。
- 数据来源：
  - [本仓库](./Custom/)
  - [AdGuard](https://github.com/AdguardTeam/AdguardFilters)

## 中国大陆网络服务
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/domestic.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/domestic.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/domestic.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/domestic.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/domestic.txt>

- 自动生成
- 包含各大中国大陆网络服务提供商的域名。
- 对于由 [CNNIC](https://www.cnnic.net.cn/) 管理的 TLD（如 `.cn`、`.中国`），无论其对应的服务是否在中国大陆境内运营，都将视为中国大陆服务。
- 不包含跨国网络服务提供商对中国大陆提供服务的域名（如微软的 `o365cn.com`）。
  - 这是因为，如果将这些域名视为中国大陆服务，用户到服务商的流量就会出现两条不同的路径——部分经代理转发，部分直接到达服务器，这无论对于用户体验还是故障排除都不利；且一些服务商会因为 IP 地址变更而注销用户的会话，导致用户需要频繁地重新验证凭据。
- 数据来源：
  - [本仓库](./Custom/)
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

## 特定网站/服务

### Apple Music
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/apple-music.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/apple-music.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/apple-music.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/apple-music.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/apple-music.txt>

- 手动维护
- 包含 Apple Music 和 iTunes Store 的服务域名。

### 巴哈姆特
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/bahamut.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/bahamut.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/bahamut.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/bahamut.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/bahamut.txt>

- 自动生成
- 包含巴哈姆特主站和巴哈姆特动画疯的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### 微软必应搜索
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/bing.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/bing.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/bing.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/bing.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/bing.txt>

- 自动生成
- 包含微软必应搜索的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### 哔哩哔哩
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/bilibili.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/bilibili.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/bilibili.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/bilibili.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/bilibili.txt>

- 手动维护
- 包含哔哩哔哩面向中国、东南亚和除此上述两者之外地区的服务域名。
  - 不含合作 CDN 域名（如与 Akamai 合作的 `upos-hz-mirrorakam.akamaized.net`）

### 思杰马克丁
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/cjmarketing.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/cjmarketing.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/cjmarketing.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/cjmarketing.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/cjmarketing.txt>

- 手动维护
- 包含苏州思杰马克丁软件有限公司的公司官网、软件商城和其伪造的各个软件的“中国官网”用于进行**拦截**。
- 请参阅：[《揭开软件行业毒瘤思杰马克丁的虚伪面纱》](https://bbs.kafan.cn/thread-2091351-1-1.html)

### DMM
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/dmm.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/dmm.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/dmm.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/dmm.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/dmm.txt>

- 自动生成
- 包含 DMM 主站和 R18 站点（Fanza）的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### Google FCM
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/googlefcm.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/googlefcm.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/googlefcm.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/googlefcm.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/googlefcm.txt>

- 自动生成
- 包含 Firebase Cloud Messaging 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### Microsoft
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/microsoft.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/microsoft.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/microsoft.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/microsoft.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/microsoft.txt>

- 自动生成
- 包含微软旗下网络服务的域名。
  - 不含 GitHub 的服务域名，因为该服务在中国大陆的连通性与微软的其他服务可能不同。
  - 不含必应搜索的服务域名，因为该服务有针对中国大陆的特殊版本。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### niconico 动画
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/niconico.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/niconico.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/niconico.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/niconico.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/niconico.txt>

- 自动生成
- 包含 niconico 动画的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### OpenAI (ChatGPT)
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/openai.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/openai.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/openai.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/openai.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/openai.txt>

- 自动生成
- 包含 OpenAI 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### PayPal
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/paypal.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/paypal.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/paypal.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/paypal.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/paypal.txt>

- 自动生成
- 包含 PayPal 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### Steam
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/steam.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/steam.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/steam.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/steam.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/steam.txt>

- 手动维护
- 包含 Steam（**非**中国大陆的蒸汽平台）的网络服务
  - **不**含资源 CDN

### YouTube
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/youtube.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/youtube.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/youtube.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/youtube.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/youtube.txt>

- 自动生成
- 包含 YouTube 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### 游戏
- 手动维护
- 提供以下游戏的分流规则（**不含**资源 CDN）：
  - [碧蓝航线（英文版）](https://azurlane.yo-star.com/)
    - 纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/azurlane-en.txt>  
      纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/azurlane-en.txt>  
      YAML 规则集：<https://rules.xkww3n.cyou/yaml/azurlane-en.txt>  
      Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/azurlane-en.txt>  
      Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/azurlane-en.txt>  
  - [BanG Dream！少女乐团派对！（日文版）](https://bang-dream.bushimo.jp/)
    - 纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/bangdream-jp.txt>  
      纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/bangdream-jp.txt>  
      YAML 规则集：<https://rules.xkww3n.cyou/yaml/bangdream-jp.txt>  
      Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/bangdream-jp.txt>  
      Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/bangdream-jp.txt>  
  - [绯染天空](https://heaven-burns-red.com/)
    - 纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/heavenburnsred.txt>  
      纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/heavenburnsred.txt>  
      YAML 规则集：<https://rules.xkww3n.cyou/yaml/heavenburnsred.txt>  
      Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/heavenburnsred.txt>  
      Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/heavenburnsred.txt>  
  - [Love Live! 学园偶像祭2 MIRACLE LIVE!（日文版）](https://lovelive-sif2.bushimo.jp/)
    - 纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/lovelivesif2-jp.txt>  
      纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/lovelivesif2-jp.txt>  
      YAML 规则集：<https://rules.xkww3n.cyou/yaml/lovelivesif2-jp.txt>  
      Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/lovelivesif2-jp.txt>  
      Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/lovelivesif2-jp.txt>  

## IP 归属地检测服务
纯文本规则集（Surge 标准，点号通配符）：<https://rules.xkww3n.cyou/text/ipgeo.txt>

纯文本规则集（Clash 标准，加号通配符）：<https://rules.xkww3n.cyou/text-plus/ipgeo.txt>

YAML 规则集：<https://rules.xkww3n.cyou/yaml/ipgeo.txt>

Clash 传统规则集：<https://rules.xkww3n.cyou/clash-compatible/ipgeo.txt>

Surge 传统规则集：<https://rules.xkww3n.cyou/surge-compatible/ipgeo.txt>

- 手动维护
- 针对（主页、评论区等）公开展示用户 IP 归属地的网站，通过代理此规则内含的域名，可以实现更改对应网站检测到的 IP 归属地而（基本）不影响其他功能。
- 支持的网站：
  - [哔哩哔哩](https://www.bilibili.com/)
  - [小红书](https://www.xiaohongshu.com/)
