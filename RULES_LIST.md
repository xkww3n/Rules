# 规则列表

## 广告服务与跟踪器拦截
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/reject.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/reject.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/reject.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/reject.txt>

- 自动生成 + 人工修订
- 拦截在中国与日本常见的广告提供商和跟踪服务商的服务域名。
- **不**拦截这些服务商面向其接入客户的域名（如：官网、控制台）。如果两者相同，将不会拦截。
- 应当放在**所有非拦截类规则列表之前**
- 数据来源：
  - [AdGuard](https://github.com/AdguardTeam/AdguardFilters)
  - [banbendalao / ADgk](https://github.com/banbendalao/ADgk/)
  - [EasyList China](https://github.com/easylist/easylistchina)
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)
  - [もちフィルタ](https://eeii0a5l.github.io/mochifilter_homepage/mochi.html)

### 排除项
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

## 中国大陆网络服务
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/geolocation-cn.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/geolocation-cn.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/geolocation-cn.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/geolocation-cn.txt>

- 自动生成 + 人工修订
- 包含各大中国大陆网络服务提供商的域名。
- 对于由 [CNNIC](https://www.cnnic.net.cn/) 管理的 TLD（如 `.cn`、`.中国`），无论其对应的服务是否在中国大陆境内运营，都将视为中国大陆服务。
- 不包含跨国网络服务提供商对中国大陆提供服务的域名（如微软的 `o365cn.com`）。
  - 这是因为，如果将这些域名视为中国大陆服务，用户到服务商的流量就会出现两条不同的路径——部分经代理转发，部分直接到达服务器，这无论对于用户体验还是故障排除都不利；且一些服务商会因为 IP 地址变更而注销用户的会话，导致用户需要频繁地重新验证凭据。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

## 特定网站/服务

### Apple Music
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/apple-music.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/apple-music.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/apple-music.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/apple-music.txt>

- 手动维护
- 包含 Apple Music 和 iTunes Store 的服务域名。

### 巴哈姆特
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/bahamut.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/bahamut.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/bahamut.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/bahamut.txt>

- 自动生成
- 包含巴哈姆特主站和巴哈姆特动画疯的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### 哔哩哔哩
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/bilibili.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/bilibili.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/bilibili.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/bilibili.txt>

- 手动维护
- 包含哔哩哔哩面向中国、东南亚和除此上述两者之外地区的服务域名。
  - 不含合作 CDN 域名（如与 Akamai 合作的 `upos-hz-mirrorakam.akamaized.net`）

### 思杰马克丁
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/cjmarketing.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/cjmarketing.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/cjmarketing.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/cjmarketing.txt>

- 手动维护
- 包含苏州思杰马克丁软件有限公司的公司官网、软件商城和其伪造的各个软件的“中国官网”用于进行**拦截**。
- 请参阅：[《揭开软件行业毒瘤思杰马克丁的虚伪面纱》](https://bbs.kafan.cn/thread-2091351-1-1.html)

### DMM
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/dmm.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/dmm.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/dmm.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/dmm.txt>

- 自动生成
- 包含 DMM 主站和 R18 站点（Fanza）的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### Google FCM
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/googlefcm.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/googlefcm.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/googlefcm.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/googlefcm.txt>

- 自动生成
- 包含 Firebase Cloud Messaging 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### Microsoft
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/microsoft.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/microsoft.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/microsoft.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/microsoft.txt>

- 自动生成
- 包含微软旗下网络服务的域名。
  - 不含 GitHub 的服务域名，因为该服务在中国大陆的连通性与微软的其他服务可能不同。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### niconico 动画
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/niconico.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/niconico.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/niconico.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/niconico.txt>

- 自动生成
- 包含 niconico 动画的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### OpenAI (ChatGPT)
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/openai.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/openai.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/openai.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/openai.txt>

- 自动生成
- 包含 OpenAI 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### PayPal
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/paypal.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/paypal.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/paypal.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/paypal.txt>

- 自动生成
- 包含 PayPal 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### 网速测试服务
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/speedtests.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/speedtests.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/speedtests.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/speedtests.txt>

- 手动维护
- 包含 [Ookla Speedtest](https://www.speedtest.net/), [Fast.com by Netflix](https://fast.com/) 和 [Cloudflare Internet Speed Test](https://speed.cloudflare.com/) 的服务域名。

### Steam
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/steam.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/steam.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/steam.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/steam.txt>

- 手动维护
- 包含 Steam（**非**中国大陆的蒸汽平台）的网络服务
  - **不**含资源 CDN

### YouTube
Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/youtube.txt>

Surge 3 规则集：<https://rules.xkww3n.cyou/surge/youtube.txt>

Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/youtube.txt>

Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/youtube.txt>

- 自动生成
- 包含 YouTube 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### 游戏
- 手动维护
- 提供以下游戏的分流规则（**包含**资源 CDN）：
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
  - [绯染天空](https://heaven-burns-red.com/)
    - Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/heavenburnsred.txt>  
      Surge 3 规则集：<https://rules.xkww3n.cyou/surge/heavenburnsred.txt>  
      Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/heavenburnsred.txt>  
      Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/heavenburnsred.txt>  
  - [Love Live!学园偶像祭2 MIRACLE LIVE!（日文版）](https://lovelive-sif2.bushimo.jp/)
    - Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/loveliesif2-jp.txt>  
      Surge 3 规则集：<https://rules.xkww3n.cyou/surge/loveliesif2-jp.txt>  
      Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/loveliesif2-jp.txt>  
      Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/loveliesif2-jp.txt>  
  - [世界计划 缤纷舞台！ feat.初音未来（繁体中文版）](https://www.tw-pjsekai.com/)
    - Clash Premium 规则集：<https://rules.xkww3n.cyou/clash/pjsk-tw.txt>  
      Surge 3 规则集：<https://rules.xkww3n.cyou/surge/pjsk-tw.txt>  
      Clash 传统规则：<https://rules.xkww3n.cyou/clash-compatible/pjsk-tw.txt>  
      Surge 传统规则：<https://rules.xkww3n.cyou/surge-compatible/pjsk-tw.txt>  