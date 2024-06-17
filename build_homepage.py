from datetime import datetime

import config


def template(urls: list) -> str:
    url_list = f'<li><a href="/{urls[0]}" target="_blank">{urls[0]}</a></li>\n'
    for url in urls[1:-2]:
        url_list += f'        <li><a href="/{url}" target="_blank">{url}</a></li>\n'
    url_list += f'        <li><a href="/{urls[-1]}" target="_blank">{urls[-1]}</a></li>'
    build_date = str(datetime.utcnow()) + " UTC"
    return \
        f"""\
<!DOCTYPE html>
<html lang="zh">
  <head>
    <meta charset="utf-8">
    <title>xkww3n's Rules</title>
    <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
  </head>
  <body>
    <main>
      <h1>xkww3n's Rules</h1>
      <p>由 <a href="https://www.xkww3n.cyou">xkww3n</a> 维护的，面向多个代理软件的规则集</p>
      <p>支持： Surge、Clash (Premium / Meta)、Stash、Choc、Quantumult (X)、Loon、Shadowrocket、LanceX 等</p>
      <p>
        项目源代码托管于 <a href="https://github.com/xkww3n/Rules/">GitHub</a>，
        以 <a href="https://github.com/xkww3n/Rules/blob/main/LICENSE" target="_blank">MIT</a> 协议授权
      </p>
      <p>构建日期：{build_date}</p>
      <hr>
      <ul>
        {url_list}
      </ul>
    </main>
  </body>
</html>
"""


blacklist = ["personal", "index"]
dists_list = []
for filename in sorted(config.PATH_DIST.rglob("*")):
    if filename.is_file() and not any(bl_name in str(filename) for bl_name in blacklist):
        if filename.parent.name == "dists":
            dists_list.append(f"{filename.name}")
        else:
            dists_list.append(f"{filename.parent.name}/{filename.name}")
open(config.PATH_DIST/"index.html", mode='w', encoding="utf-8").write(template(dists_list))
