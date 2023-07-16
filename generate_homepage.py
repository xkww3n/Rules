from datetime import datetime

from Utils import const


def template(urls: list) -> str:
    url_list = "".join(
        [f'<li><a href="{url}" target="_blank">{url}</a></li>\n' for url in urls]
    )
    build_date = str(datetime.utcnow()) + " UTC"
    return f"""
    <!DOCTYPE html>
    <html lang="en">
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
        <p>项目源代码托管于 <a href="https://github.com/xkww3n/Rules/">GitHub</a>，以 <a href="https://github.com/xkww3n/Rules/blob/main/LICENSE" target="_blank">MIT</a> 协议授权</p>
        <p>构建日期：{build_date}</p>
        <hr>
        <ul>
            {url_list}
        </ul>
    </main>
    </body>
    </html>
    """


blacklist = ["surge", "clash", "personal"]
dists_list = []
for filename in (
    sorted((const.PATH_DIST/"text").rglob("**/*.txt"))
    + sorted((const.PATH_DIST/"text-plus").rglob("**/*.txt"))
    + sorted((const.PATH_DIST/"yaml").rglob("**/*.txt"))
    + sorted((const.PATH_DIST/"surge-compatible").rglob("**/*.txt"))
    + sorted((const.PATH_DIST/"clash-compatible").rglob("**/*.txt"))
):
    if filename.parent.name not in blacklist:
        dists_list.append(f"{filename.parent.name}/{filename.name}")
open(const.PATH_DIST/"index.html", mode='w').write(template(dists_list))
