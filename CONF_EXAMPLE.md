# 示例配置
以下配置仅供参考，你可能需要自行选择需要引用的列表，并将其与你自己的代理策略匹配。

## Clash Premium
致 Stash 用户：Stash 的规则集配置格式和 Clash Premium **不同**，请继续向下阅读以查看 Stash 规则集的配置方法。

适用于 **2023.04.13** 及更新版本：

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
    format: text
    url: https://rules.xkww3n.cyou/text-plus/cjmarketing.txt
    path: ./Rules/CJMarketing
    interval: 86400
  Reject:
    type: http
    behavior: domain
    format: text
    url: https://rules.xkww3n.cyou/text-plus/reject.txt
    path: ./Rules/Reject
    interval: 86400
  Exclude:
    type: http
    behavior: domain
    format: text
    url: https://rules.xkww3n.cyou/text-plus/exclude.txt
    path: ./Rules/Exclude
    interval: 86400
  CN:
    type: http
    behavior: domain
    format: text
    url: https://rules.xkww3n.cyou/text-plus/domestic.txt
    path: ./Rules/CN
    interval: 86400
  Microsoft:
    type: http
    behavior: domain
    format: text
    url: https://rules.xkww3n.cyou/text-plus/microsoft.txt
    path: ./Rules/Microsoft
    interval: 86400
  niconico:
    type: http
    behavior: domain
    format: text
    url: https://rules.xkww3n.cyou/text-plus/niconico.txt
    path: ./Rules/niconico
    interval: 86400
  BanG Dream:
    type: http
    behavior: domain
    format: text
    url: https://rules.xkww3n.cyou/text-plus/bangdream-jp.txt
    path: ./Rules/BanG Dream
    interval: 86400
```

适用于 **2023.04.13 以前**的版本：

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
    url: https://rules.xkww3n.cyou/yaml/cjmarketing.txt
    path: ./Rules/CJMarketing
    interval: 86400
  Reject:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/yaml/reject.txt
    path: ./Rules/Reject
    interval: 86400
  Exclude:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/yaml/exclude.txt
    path: ./Rules/Exclude
    interval: 86400
  CN:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/yaml/domestic.txt
    path: ./Rules/CN
    interval: 86400
  Microsoft:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/yaml/microsoft.txt
    path: ./Rules/Microsoft
    interval: 86400
  niconico:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/yaml/niconico.txt
    path: ./Rules/niconico
    interval: 86400
  BanG Dream:
    type: http
    behavior: domain
    url: https://rules.xkww3n.cyou/yaml/bangdream-jp.txt
    path: ./Rules/BanG Dream
    interval: 86400
```

## Stash
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
    behavior: domain-text
    url: https://rules.xkww3n.cyou/text/cjmarketing.txt
    path: ./Rules/CJMarketing
    interval: 86400
  Reject:
    type: http
    behavior: domain-text
    url: https://rules.xkww3n.cyou/text/reject.txt
    path: ./Rules/Reject
    interval: 86400
  Exclude:
    type: http
    behavior: domain-text
    url: https://rules.xkww3n.cyou/text/exclude.txt
    path: ./Rules/Exclude
    interval: 86400
  CN:
    type: http
    behavior: domain-text
    url: https://rules.xkww3n.cyou/text/domestic.txt
    path: ./Rules/CN
    interval: 86400
  Microsoft:
    type: http
    behavior: domain-text
    url: https://rules.xkww3n.cyou/text/microsoft.txt
    path: ./Rules/Microsoft
    interval: 86400
  niconico:
    type: http
    behavior: domain-text
    url: https://rules.xkww3n.cyou/text/niconico.txt
    path: ./Rules/niconico
    interval: 86400
  BanG Dream:
    type: http
    behavior: domain-text
    url: https://rules.xkww3n.cyou/text/bangdream-jp.txt
    path: ./Rules/BanG Dream
    interval: 86400
```

## Surge 3 / Shadowrocket
```
[Rule]
DOMAIN-SET,https://rules.xkww3n.cyou/text/cjmarketing.txt,REJECT
DOMAIN-SET,https://rules.xkww3n.cyou/text/reject.txt,REJECT
DOMAIN-SET,https://rules.xkww3n.cyou/text/exclude.txt,Final
DOMAIN-SET,https://rules.xkww3n.cyou/text/domestic.txt,DIRECT
DOMAIN-SET,https://rules.xkww3n.cyou/text/microsoft.txt,Proxy
DOMAIN-SET,https://rules.xkww3n.cyou/text/niconico.txt,JP
DOMAIN-SET,https://rules.xkww3n.cyou/text/bangdream-jp.txt,Gaming
```

## Quantumult X
该软件需要使用 Clash 传统规则。

**每个策略组都必须指定 `force-policy` 字段！**

```
[filter_remote]
https://rules.xkww3n.cyou/clash-compatible/cjmarketing.txt,tag=CJMarketing,force-policy=Reject,enabled=true
https://rules.xkww3n.cyou/clash-compatible/reject.txt,tag=Reject,force-policy=Reject,enabled=true
https://rules.xkww3n.cyou/clash-compatible/exclude.txt,tag=Exclude,force-policy=Final,enabled=true
https://rules.xkww3n.cyou/clash-compatible/domestic.txt,tag=CN,force-policy=Direct,enabled=true
https://rules.xkww3n.cyou/clash-compatible/microsoft.txt,tag=Microsoft,force-policy=Proxy,enabled=true
https://rules.xkww3n.cyou/clash-compatible/niconico.txt,tag=niconico,force-policy=JP,enabled=true
https://rules.xkww3n.cyou/clash-compatible/bangdream-jp.txt,tag=BanG Dream,force-policy=Gaming,enabled=true
```

## Loon
该软件需要使用 Surge 传统规则。

```
[Remote Rule]
https://rules.xkww3n.cyou/surge-compatible/cjmarketing.txt,policy=REJECT,tag=CJMarketing,enabled=true
https://rules.xkww3n.cyou/surge-compatible/reject.txt,policy=REJECT,tag=Reject,enabled=true
https://rules.xkww3n.cyou/surge-compatible/exclude.txt,policy=Final,tag=Exclude,enabled=true
https://rules.xkww3n.cyou/surge-compatible/domestic.txt,policy=DIRECT,tag=CN,enabled=true
https://rules.xkww3n.cyou/surge-compatible/microsoft.txt,policy=Proxy,tag=Microsoft,enabled=true
https://rules.xkww3n.cyou/surge-compatible/niconico.txt,policy=JP,tag=niconico,enabled=true
https://rules.xkww3n.cyou/surge-compatible/bangdream-jp.txt,policy=Gaming,tag=BanG Dream,enabled=true
```
