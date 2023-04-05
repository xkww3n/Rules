# Rules
一套由 xkww3n 搜集、整理与维护的，适用于大多数主流代理软件的规则列表。

本仓库含两个分支——*main* 和 *gh-pages*，其中前者包含用于生成规则列表的脚本（*generate.py*）以及部分自定义内容（*Custom* 和 *Source* 文件夹），后者包含生成的规则列表。

本仓库提供四种格式的规则列表：
- [Clash Premium](https://github.com/Dreamacro/clash/wiki/Clash-Premium-Features) 规则集
  - 同时适用于兼容 Clash Premium 规则集格式的代理软件，如 [Clash Meta](https://github.com/MetaCubeX/Clash.Meta/) 和 [Stash](https://stash.ws/).
- [Surge 3](https://nssurge.com/) 规则集
  - 同时适用于兼容 Surge 3 规则集的代理软件，如 [Surfboard](https://getsurfboard.com/).
- Clash 传统规则
  - 适用于兼容传统 Clash 规则的代理软件，如 [Clash FOSS](https://github.com/Dreamacro/clash), [Quantumult](https://quantumult.app/) [(X)](https://quantumult.app/x/) 和 [Shadowrocket](https://apps.apple.com/us/app/shadowrocket/id932747118).
- Surge 传统规则
  - 适用于兼容传统 Surge 规则的代理软件，如 Surge 2 和 [Loon](https://www.nsloon.com/).

## 规则列表

### 广告服务与跟踪器拦截
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/reject.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/reject.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/reject.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/reject.txt>

- 自动生成
- 拦截在中国与日本常见的广告提供商和跟踪服务商的服务域名。
- **不**拦截这些服务商面向其接入客户的域名（如：官网、控制台）。如果两者相同，将不会拦截。
- 应当放在**所有非拦截类规则列表之前**
- 数据来源：
  - [AdGuard](https://github.com/AdguardTeam/AdguardFilters)
  - [banbendalao / ADgk](https://github.com/banbendalao/ADgk/)
  - [EasyList China](https://github.com/easylist/easylistchina)
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)
  - [もちフィルタ](https://eeii0a5l.github.io/mochifilter_homepage/mochi.html)

#### 排除项
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/exclude.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/exclude.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/exclude.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/exclude.txt>

- 自动生成
- 包含一些不应被拦截规则拦截的域名。
  - 如：拦截规则拦截了 `googleadservices.com` 域名，这个域名的许多子域名都被用于推送广告，因此将这个域名纳入拦截列表完全合理。但是，`www.googleadservices.com` 这个子域名用于 Google 搜索引擎中广告条目的跳转，不应被拦截；所以，此域名被纳入排除规则中。
- 应当放在**拦截规则列表之前**。
- 数据来源：
  - [AdGuard](https://github.com/AdguardTeam/AdguardFilters)

### 中国大陆网络服务
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/geolocation-cn.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/geolocation-cn.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/geolocation-cn.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/geolocation-cn.txt>

- 自动生成
- 包含各大中国大陆网络服务提供商的域名。
- 对于由 [CNNIC](https://www.cnnic.net.cn/) 管理的 TLD（如 `.cn`、`.中国`），无论其对应的服务是否在中国大陆境内运营，都将视为中国大陆服务。
- 不包含跨国网络服务提供商对中国大陆提供服务的域名（如微软的 `o365cn.com`）。
  - 这是因为，如果将这些域名视为中国大陆服务，用户到服务商的流量就会出现两条不同的路径——部分经代理转发，部分直接到达服务器，这无论对于用户体验还是故障排除都不利；且一些服务商会因为 IP 地址变更而注销用户的会话，导致用户需要频繁地重新验证凭据。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### 特定网站/服务

#### Apple Music
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/apple-music.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/apple-music.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/apple-music.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/apple-music.txt>

- 手动维护
- 包含 Apple Music 和 iTunes Store 的服务域名。

#### 巴哈姆特
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/bahamut.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/bahamut.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/bahamut.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/bahamut.txt>

- 自动生成
- 包含巴哈姆特主站和巴哈姆特动画疯的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### 哔哩哔哩
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/bilibili.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/bilibili.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/bilibili.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/bilibili.txt>

- 手动维护
- 包含哔哩哔哩面向中国、东南亚和除此上述两者之外地区的服务域名。
  - 不含合作 CDN 域名（如与 Akamai 合作的 `upos-hz-mirrorakam.akamaized.net`）

#### 思杰马克丁
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/cjmarketing.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/cjmarketing.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/cjmarketing.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/cjmarketing.txt>

- 手动维护
- 包含苏州思杰马克丁软件有限公司的公司官网、软件商城和其伪造的各个软件的“中国官网”用于进行**拦截**。
- 请参阅：[《揭开软件行业毒瘤思杰马克丁的虚伪面纱》](https://bbs.kafan.cn/thread-2091351-1-1.html)

#### DMM
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/dmm.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/dmm.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/dmm.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/dmm.txt>

- 自动生成
- 包含 DMM 主站和 R18 站点（Fanza）的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### Google FCM
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/googlefcm.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/googlefcm.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/googlefcm.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/googlefcm.txt>

- 自动生成
- 包含 Firebase Cloud Messaging 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### Microsoft
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/microsoft.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/microsoft.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/microsoft.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/microsoft.txt>

- 自动生成
- 包含微软旗下网络服务的域名。
  - 不含 GitHub 的服务域名，因为该服务在中国大陆的连通性与微软的其他服务可能不同。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### niconico 动画 / ニコニコ動画
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/niconico.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/niconico.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/niconico.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/niconico.txt>

- 自动生成
- 包含 niconico 动画的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### OpenAI (ChatGPT)
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/openai.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/openai.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/openai.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/openai.txt>

- 自动生成
- 包含 OpenAI 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### PayPal
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/paypal.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/paypal.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/paypal.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/paypal.txt>

- 自动生成
- 包含 PayPal 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### 网速测试服务
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/speedtests.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/speedtests.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/speedtests.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/speedtests.txt>

- 手动维护
- 包含 [Ookla Speedtest](https://www.speedtest.net/), [Fast.com by Netflix](https://fast.com/) 和 [Cloudflare Internet Speed Test](https://speed.cloudflare.com/) 的服务域名。

#### YouTube
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/youtube.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/youtube.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/youtube.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/youtube.txt>

- 自动生成
- 包含 YouTube 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### 游戏
提供以下游戏的分流规则：
  - [碧蓝航线（英文版）](https://azurlane.yo-star.com/)
    - Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/azurlane-en.txt>  
      Surge 3 规则集：<https://rules.xkww3n.cyou/surge/azurlane-en.txt>  
      Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/azurlane-en.txt>  
      Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/azurlane-en.txt>  
  - [BanG Dream！少女乐团派对！（日文版）](https://bang-dream.bushimo.jp/)
    - Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/bangdream-jp.txt>  
      Surge 3 规则集：<https://rules.xkww3n.cyou/surge/bangdream-jp.txt>  
      Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/bangdream-jp.txt>  
      Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/bangdream-jp.txt>  
  - [原神（国际版）](https://genshin.hoyoverse.com/)
    - Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/genshin.txt>  
      Surge 3 规则集：<https://rules.xkww3n.cyou/surge/genshin.txt>  
      Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/genshin.txt>  
      Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/genshin.txt>  
  - ~~[Love Live! 学园偶像祭（英文版）](https://lovelive-sif-global.bushimo.jp/)~~
    - ~~Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/loveliesif-en.txt>~~  
      ~~Surge 3 规则集：<https://rules.xkww3n.cyou/surge/loveliesif-en.txt>~~  
      ~~Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/loveliesif-en.txt>~~  
      ~~Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/loveliesif-en.txt>~~  
  - [世界计划 缤纷舞台！ feat.初音未来（繁体中文版）](https://www.tw-pjsekai.com/)
    - Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/pjsk-tw.txt>  
      Surge 3 规则集：<https://rules.xkww3n.cyou/surge/pjsk-tw.txt>  
      Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/pjsk-tw.txt>  
      Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/pjsk-tw.txt>  

## 示例配置
以下配置仅供参考，你可能需要自行选择需要引用的列表，并将其与你自己的代理策略匹配。

Shdaowrocket 不提供在配置文件内指定引用远程规则的功能，只可在软件内手动指定，故不提供配置示例。

### Clash Premium
```yaml
rules:
- RULE-SET,CJMarketing,REJECT
- RULE-SET,Reject,REJECT
- RULE-SET,Exclude,Final
- RULE-SET,CN,DIRECT
- RULE-SET,Microsoft,Proxy
- RULE-SET,niconico,JP
- RULE-SET,BanG Dream,Gaming

rule-providers:
  CJMarketing:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/cjmarketing.txt
    path: ./Rules/CJMarketing
    interval: 86400
  Reject:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/reject.txt
    path: ./Rules/Reject
    interval: 86400
  Exclude:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/exclude.txt
    path: ./Rules/Exclude
    interval: 86400
  CN:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/geolocation-cn.txt
    path: ./Rules/CN
    interval: 86400
  Microsoft:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/microsoft.txt
    path: ./Rules/Microsoft
    interval: 86400
  niconico:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/niconico.txt
    path: ./Rules/niconico
    interval: 86400
  BanG Dream:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/bangdream-jp.txt
    path: ./Rules/BanG Dream
    interval: 86400
```

### Surge 3
```
[Rule]
DOMAIN-SET,https://rules.xkww3n.cyou/surge/cjmarketing.txt,REJECT
DOMAIN-SET,https://rules.xkww3n.cyou/surge/reject.txt,REJECT
DOMAIN-SET,https://rules.xkww3n.cyou/surge/exclude.txt,Final
DOMAIN-SET,https://rules.xkww3n.cyou/surge/geolocation-cn.txt,DIRECT
DOMAIN-SET,https://rules.xkww3n.cyou/surge/microsoft.txt,Proxy
DOMAIN-SET,https://rules.xkww3n.cyou/surge/niconico.txt,JP
DOMAIN-SET,https://rules.xkww3n.cyou/surge/bangdream-jp.txt,Gaming
```

### Quantumult X
该软件需要使用 Clash 传统规则。

**每个策略组都必须指定 `force-policy` 字段！**

```
[filter_remote]
https://rules.xkww3n.cyou/clash-compatible/cjmarketing.txt,tag=CJMarketing,force-policy=Reject,enabled=true
https://rules.xkww3n.cyou/clash-compatible/reject.txt,tag=Reject,force-policy=Reject,enabled=true
https://rules.xkww3n.cyou/clash-compatible/exclude.txt,tag=Exclude,force-policy=Final,enabled=true
https://rules.xkww3n.cyou/clash-compatible/geolocation-cn.txt,tag=CN,force-policy=Direct,enabled=true
https://rules.xkww3n.cyou/clash-compatible/microsoft.txt,tag=Microsoft,force-policy=Proxy,enabled=true
https://rules.xkww3n.cyou/clash-compatible/niconico.txt,tag=niconico,force-policy=JP,enabled=true
https://rules.xkww3n.cyou/clash-compatible/bangdream-jp.txt,tag=BanG Dream,force-policy=Gaming,enabled=true
```

### Loon
该软件需要使用 Surge 传统规则。

```
[Remote Rule]
https://rules.xkww3n.cyou/surge-compatible/cjmarketing.txt,policy=REJECT,tag=CJMarketing,enabled=true
https://rules.xkww3n.cyou/surge-compatible/reject.txt,policy=REJECT,tag=Reject,enabled=true
https://rules.xkww3n.cyou/surge-compatible/exclude.txt,policy=Final,tag=Exclude,enabled=true
https://rules.xkww3n.cyou/surge-compatible/geolocation-cn.txt,policy=DIRECT,tag=CN,enabled=true
https://rules.xkww3n.cyou/surge-compatible/microsoft.txt,policy=Proxy,tag=Microsoft,enabled=true
https://rules.xkww3n.cyou/surge-compatible/niconico.txt,policy=JP,tag=niconico,enabled=true
https://rules.xkww3n.cyou/surge-compatible/bangdream-jp.txt,policy=Gaming,tag=BanG Dream,enabled=true
```

## 许可证
如无特别声明，本项目的一切内容均使用 MIT 许可证授权。
