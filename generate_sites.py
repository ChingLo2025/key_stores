"""Generate static pages for locksmith shops.

Reads shop records from ``key.csv`` (encoded in CP950) and outputs a static
site in ``docs/`` ready for GitHub Pages. Each shop receives its own page, and
an index page links to all of them.
"""
from __future__ import annotations

import csv
import html
import shutil
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "key.csv"
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
SHOPS_DIR = DOCS_DIR / "shops"


@dataclass
class Shop:
    name: str
    map_url: str
    rating: str
    address: str
    phone: str
    slug: str


def normalize_slug(index: int, name: str) -> str:
    """Return a URL-friendly slug that stays stable even with non-ASCII names."""
    ascii_only = "".join(
        char.lower() if char.isascii() and char.isalnum() else "-" for char in name
    )
    compact = "-".join(filter(None, ascii_only.split("-")))
    fallback = "shop"
    return f"{compact or fallback}-{index + 1}"


def load_shops() -> list[Shop]:
    with CSV_PATH.open("r", encoding="cp950") as csvfile:
        reader = csv.DictReader(csvfile)
        shops: list[Shop] = []
        for index, row in enumerate(reader):
            shops.append(
                Shop(
                    name=row["店名"].strip(),
                    map_url=row["google地圖連結"].strip(),
                    rating=row["Google分數"].strip(),
                    address=row["地址"].strip(),
                    phone=row["聯絡電話"].strip(),
                    slug=normalize_slug(index, row["店名"]),
                )
            )
    return shops


def ensure_directories() -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    if SHOPS_DIR.exists():
        shutil.rmtree(SHOPS_DIR)
    SHOPS_DIR.mkdir(parents=True, exist_ok=True)


def write_assets() -> None:
    style = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700&display=swap');
:root {
    color: #0f172a;
    background: #f8fafc;
    font-family: 'Noto Sans TC', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
* { box-sizing: border-box; }
body { margin: 0; }
a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }
.header, .footer { background: white; border-bottom: 1px solid #e2e8f0; padding: 1.25rem 1.5rem; }
.footer { border-top: 1px solid #e2e8f0; border-bottom: none; text-align: center; color: #475569; }
.hero { max-width: 1100px; margin: 0 auto; }
.hero h1 { margin: 0; font-size: 1.8rem; }
.hero p { margin: 0.25rem 0 0; color: #475569; }
main { max-width: 1100px; margin: 0 auto; padding: 1.5rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; }
.card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem; box-shadow: 0 10px 25px rgba(15,23,42,0.05); }
.card h2 { margin: 0 0 0.5rem; font-size: 1.1rem; }
.meta { color: #475569; margin: 0.35rem 0; }
.badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 999px; background: #e0f2fe; color: #0369a1; font-weight: 700; font-size: 0.9rem; }
.actions { margin-top: 0.75rem; display: flex; gap: 0.5rem; flex-wrap: wrap; }
.button { display: inline-flex; align-items: center; justify-content: center; padding: 0.55rem 0.9rem; border-radius: 10px; font-weight: 600; background: #2563eb; color: white; border: none; }
.button.secondary { background: #e2e8f0; color: #0f172a; }
.button:hover { text-decoration: none; filter: brightness(0.95); }
.details { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.5rem; box-shadow: 0 10px 25px rgba(15,23,42,0.05); }
.details h1 { margin-top: 0; margin-bottom: 0.75rem; }
.details dl { display: grid; grid-template-columns: 120px 1fr; gap: 0.5rem 1rem; margin: 0 0 1rem; }
.details dt { font-weight: 700; color: #0f172a; }
.details dd { margin: 0; color: #334155; }
.breadcrumb { margin-bottom: 1rem; display: inline-flex; gap: 0.35rem; align-items: center; color: #475569; }
.breadcrumb a { color: inherit; }
    """
    (ASSETS_DIR / "style.css").write_text(style.strip() + "\n", encoding="utf-8")


def render_index(shops: list[Shop]) -> str:
    cards = []
    for shop in shops:
        cards.append(
            f"""
        <article class=\"card\">
            <h2>{html.escape(shop.name)}</h2>
            <p class=\"meta\">Google 評分：<span class=\"badge\">{html.escape(shop.rating)}</span></p>
            <p class=\"meta\">地址：{html.escape(shop.address)}</p>
            <p class=\"meta\">電話：{html.escape(shop.phone)}</p>
            <div class=\"actions\">
                <a class=\"button\" href=\"shops/{shop.slug}/\">查看網站</a>
                <a class=\"button secondary\" href=\"{html.escape(shop.map_url)}\" target=\"_blank\" rel=\"noopener\">Google 地圖</a>
            </div>
        </article>
        """
        )

    return f"""
<!doctype html>
<html lang=\"zh-Hant\">
<head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>三重鎖印行專頁彙整</title>
    <link rel=\"stylesheet\" href=\"assets/style.css\">
</head>
<body>
    <header class=\"header\">
        <div class=\"hero\">
            <h1>三重鎖印行專頁</h1>
            <p>自動從 key.csv 產生，共 {len(shops)} 間店家，每間店都有獨立頁面。</p>
        </div>
    </header>
    <main>
        <div class=\"grid\">
            {''.join(cards)}
        </div>
    </main>
    <div class=\"footer\">資料來源：key.csv · 透過 GitHub Pages 發佈</div>
</body>
</html>
"""


def render_shop_page(shop: Shop) -> str:
    return f"""
<!doctype html>
<html lang=\"zh-Hant\">
<head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>{html.escape(shop.name)} | 鎖印行專頁</title>
    <link rel=\"stylesheet\" href=\"../../assets/style.css\">
</head>
<body>
    <header class=\"header\">
        <div class=\"hero\">
            <div class=\"breadcrumb\"><a href=\"../../\">首頁</a> / <span>{html.escape(shop.name)}</span></div>
            <h1>{html.escape(shop.name)}</h1>
            <p>Google 評分 {html.escape(shop.rating)} · 服務資訊與位置</p>
        </div>
    </header>
    <main>
        <section class=\"details\">
            <h1>{html.escape(shop.name)}</h1>
            <p class=\"meta\">Google 評分：<span class=\"badge\">{html.escape(shop.rating)}</span></p>
            <dl>
                <dt>地址</dt><dd>{html.escape(shop.address)}</dd>
                <dt>電話</dt><dd>{html.escape(shop.phone)}</dd>
                <dt>Google 地圖</dt><dd><a href=\"{html.escape(shop.map_url)}\" target=\"_blank\" rel=\"noopener\">{html.escape(shop.map_url)}</a></dd>
            </dl>
            <div class=\"actions\">
                <a class=\"button\" href=\"{html.escape(shop.map_url)}\" target=\"_blank\" rel=\"noopener\">在 Google 地圖查看</a>
                <a class=\"button secondary\" href=\"../../\">返回店家列表</a>
            </div>
        </section>
    </main>
    <div class=\"footer\">此頁面由 key.csv 產生，適用於 GitHub Pages。</div>
</body>
</html>
"""


def write_index(shops: list[Shop]) -> None:
    (DOCS_DIR / "index.html").write_text(render_index(shops), encoding="utf-8")


def write_shops(shops: list[Shop]) -> None:
    for shop in shops:
        shop_dir = SHOPS_DIR / shop.slug
        shop_dir.mkdir(parents=True, exist_ok=True)
        (shop_dir / "index.html").write_text(render_shop_page(shop), encoding="utf-8")


def main() -> None:
    shops = load_shops()
    ensure_directories()
    write_assets()
    write_index(shops)
    write_shops(shops)
    print(f"Generated {len(shops)} shop pages in {DOCS_DIR}")


if __name__ == "__main__":
    main()
