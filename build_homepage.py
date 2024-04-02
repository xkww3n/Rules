from datetime import datetime

import config


def template(urls: list) -> str:
    url_list = "".join(
        [f'<li><a href="{"https://rules.xkww3n.cyou/" + url}" target="_blank">{url}</a></li>\n' for url in urls]
    )
    build_date = str(datetime.utcnow()) + " UTC"
    return f"""
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
        <p>项目源代码托管于 <a href="https://github.com/xkww3n/Rules/">GitHub</a>，
        以 <a href="https://github.com/xkww3n/Rules/blob/main/LICENSE" target="_blank">MIT</a> 协议授权</p>
        <p>构建日期：{build_date}</p>
        <hr>
        <ul>
            {url_list}
        </ul>
    </main>
    </body>
    </html>
    """


blacklist = ["personal"]
dists_list = []
for filename in sorted(config.PATH_DIST.rglob("*")):
    if filename.is_file() and filename.parent.name not in blacklist:
        if filename.parent.name == "dists":
            dists_list.append(f"{filename.name}")
        elif "personal" in str(filename):
            pass
        else:
            dists_list.append(f"{filename.parent.name}/{filename.name}")
open(config.PATH_DIST/"index.html", mode='w', encoding="utf-8").write(template(dists_list))
