# Rules
一套由 xkww3n 搜集、整理与维护的，适用于兼容 [Clash Premium](https://github.com/Dreamacro/clash) 和 [Surge](https://nssurge.com/) 格式之代理软件的规则列表。

本仓库含两个分支——*main* 和 *gh-pages*，其中前者包含用于生成规则列表的脚本（generate.py）以及部分自定义内容（Custom 和 Source 文件夹），后者包含生成的规则列表。

## 规则列表

### 广告服务与跟踪器拦截
Surge:

```

DOMAIN-SET,https://rules.xkww3n.cyou/surge/reject.txt,REJECT

```

Clash Premium:

```

rules:

- RULE-SET,Reject,REJECT

rule-providers:

  Reject:

    type: http

    behavior: domain

    url: https://rules.xkww3n.cyou/clash/reject.txt

    path: ./Rules/Reject

    interval: 86400

```

- 自动生成
- 拦截在中国与日本常见的广告提供商和跟踪服务商的服务域名。
- **不**拦截这些服务商面向其接入客户的域名（如：官网、控制台）。如果两者相同，将不会拦截。
- 应当放在**所有非拦截类规则列表之前**
- 数据来源：
  - [AdGuard](https://github.com/AdguardTeam/AdguardFilters)
  - [banbendalao / ADgk](https://github.com/banbendalao/ADgk/)
  - [EasyList China](https://github.com/easylist/easylistchina)
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### 排除项
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/exclude.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,Exclude,*your policy*

rule-providers:
  Exclude:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/exclude.txt
    path: ./Rules/Exclude
    interval: 86400
```

- 自动生成
- 包含一些不应被拦截规则拦截的域名。
  - 如：拦截规则拦截了 `googleadservices.com` 域名，这个域名的许多子域名都被用于推送广告，因此将这个域名纳入拦截列表完全合理。但是，`www.googleadservices.com` 这个子域名用于 Google 搜索引擎中广告条目的跳转，不应被拦截；所以，此域名被纳入排除规则中。
- 应当放在**拦截规则列表之前**。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### 中国大陆网络服务
Surge:

```

DOMAIN-SET,https://rules.xkww3n.cyou/surge/geolocation-cn.txt,*your policy*

```

Clash Premium:

```

rules:

- RULE-SET,CN,*your policy*

rule-providers:

  CN:

    type: http

    behavior: domain

    url: https://rules.xkww3n.cyou/clash/geolocation-cn.txt

    path: ./Rules/CN

    interval: 86400

```

- 自动生成
- 包含各大中国大陆网络服务提供商的域名。
- 对于由 [CNNIC](https://www.cnnic.net.cn/) 管理的 TLD（如 `.cn`、`.中国`），无论其对应的服务是否在中国境内运营，都将视为中国服务。
- 不包含跨国网络服务提供商对中国大陆提供服务的域名（如微软的 `o365cn.com`）。
  - 这是因为，如果将这些域名视为中国大陆服务，用户到服务商的流量就会出现两条不同的路径——部分经代理转发，部分直接到达服务器，这无论对于用户体验还是故障排除都不利；且一些服务商会因为 IP 地址变更而注销用户的会话，导致用户需要频繁地重新验证凭据。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

### 特定网站/服务

#### Apple Music
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/apple-music.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,Apple Music,*your policy*

rule-providers:
  Apple Music:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/apple-music.txt
    path: ./Rules/Apple Music
    interval: 86400
```

- 手动维护
- 包含 Apple Music 和 iTunes Store 的服务域名。

#### 巴哈姆特
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/bahamut.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,Bahamut,*your policy*

rule-providers:
  Bahamut:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/bahamut.txt
    path: ./Rules/Bahamut
    interval: 86400
```

- 自动生成
- 包含巴哈姆特主站和巴哈姆特动画疯的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### 哔哩哔哩
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/bilibili.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,Bilibili,*your policy*

rule-providers:
  Bilibili:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/bilibili.txt
    path: ./Rules/Bilibili
    interval: 86400
```

- 手动维护
- 包含哔哩哔哩面向中国、东南亚和除此上述两者之外地区的服务域名。
  - 不含合作 CDN 域名（如与 Akamai 合作的 `upos-hz-mirrorakam.akamaized.net`）

#### 思杰马克丁
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/cjmarketing.txt,REJECT
```

Clash Premium:

```
rules:
- RULE-SET,CJMarketing,REJECT

rule-providers:
  Bilibili:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/cjmarketing.txt
    path: ./Rules/Apple Music
    interval: 86400
```

- 手动维护
- 包含苏州思杰马克丁软件有限公司的公司官网、软件商城和其伪造的各个软件的“中国官网”用于进行**拦截**。
- 请参阅：[《揭开软件行业毒瘤思杰马克丁的虚伪面纱》](https://bbs.kafan.cn/thread-2091351-1-1.html)

#### DMM
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/dmm.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,DMM,*your policy*

rule-providers:
  DMM:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/dmm.txt
    path: ./Rules/DMM
    interval: 86400
```

- 自动生成
- 包含 DMM 主站和 R18 站点（Fanza）的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### Google FCM
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/googlefcm.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,Google FCM,*your policy*

rule-providers:
  Google FCM:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/googlefcm.txt
    path: ./Rules/Google FCM
    interval: 86400
```

- 自动生成
- 包含 Firebase Cloud Messaging 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### Microsoft
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/microsoft.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,Microsoft,*your policy*

rule-providers:
  Microsoft:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/microsoft.txt
    path: ./Rules/Microsoft
    interval: 86400
```

- 自动生成
- 包含微软旗下网络服务的域名。
  - 不含 GitHub 的服务域名，因为该服务在中国大陆的连通性与微软的其他服务可能不同。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### niconico 动画 / ニコニコ動画
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/dmm.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,DMM,*your policy*

rule-providers:
  DMM:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/dmm.txt
    path: ./Rules/DMM
    interval: 86400
```

- 自动生成
- 包含 niconico 动画的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### PayPal
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/paypal.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,Bilibili,*your policy*

rule-providers:
  PayPal:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/paypal.txt
    path: ./Rules/PayPal
    interval: 86400
```

- 自动生成
- 包含 PayPal 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### 网速测试服务
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/speedtests.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,SpeedTests,*your policy*

rule-providers:
  SpeedTests:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/speedtests.txt
    path: ./Rules/SpeedTests
    interval: 86400
```

- 手动维护
- 包含 [Ookla Speedtest](https://www.speedtest.net/), [Fast.com by Netflix](https://fast.com/) 和 [Cloudflare Internet Speed Test](https://speed.cloudflare.com/) 的服务域名。

#### YouTube
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/youtube.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,YouTube,*your policy*

rule-providers:
  YouTube:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/youtube.txt
    path: ./Rules/YouTube
    interval: 86400
```

- 自动生成
- 包含 YouTube 的服务域名。
- 数据来源：
  - [v2fly / domain-list-community](https://github.com/v2fly/domain-list-community/)

#### 游戏
Surge:

```
DOMAIN-SET,https://rules.xkww3n.cyou/surge/*game code*.txt,*your policy*
```

Clash Premium:

```
rules:
- RULE-SET,*game code*,*your policy*

rule-providers:
  Bahamut:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/clash/*game code*.txt
    path: ./Rules/*game name*
    interval: 86400
```

  - [碧蓝航线（英文版）](https://azurlane.yo-star.com/)`azurlane-en`
  - [BanG Dream！少女乐团派对！（日文版）](https://bang-dream.bushimo.jp/)`bangdream-jp`
  - [原神（国际版）](https://genshin.hoyoverse.com/)`genshin`
  - [Love Live! 学园偶像祭（英文版）](https://lovelive-sif-global.bushimo.jp/)`lovelovesif-en`
  - [世界计划 缤纷舞台！ feat.初音未來（繁体中文版）](https://www.tw-pjsekai.com/)`pjsk-tw`

## 许可证
如无特别声明，本项目的一切内容均使用 MIT 许可证授权。
