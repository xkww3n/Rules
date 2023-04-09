# 示例配置
以下配置仅供参考，你可能需要自行选择需要引用的列表，并将其与你自己的代理策略匹配。

Shdaowrocket 不提供在配置文件内指定引用远程规则的功能，只可在软件内手动指定，故不提供配置示例。

## Clash Premium
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

## Surge 3
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

## Quantumult X
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

## Loon
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