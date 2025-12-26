from __future__ import annotations

import csv
import html
import re
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).parent
SOURCE = ROOT / "key.csv"
DOCS = ROOT / "docs"
STORES_DIR = DOCS / "stores"
ASSETS_DIR = DOCS / "assets"


def load_stores() -> List[Dict[str, str]]:
    with SOURCE.open("r", encoding="cp950", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    stores = []
    for index, row in enumerate(rows, start=1):
        stores.append(
            {
                "id": f"{index:02d}",
                "name": row["店名"].strip(),
                "map_url": row["Google地圖連結"].strip(),
                "photo_url": row["照片"].strip(),
                "rating": row["Google評論分數"].strip(),
                "address": row["地址"].strip(),
                "phone": row["聯絡電話"].strip(),
            }
        )
    return stores


def slugify(name: str, fallback: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower())
    base = base.strip("-")
    return base or fallback


def tel_link(phone: str) -> str:
    digits = re.sub(r"[^0-9+]+", "", phone)
    return f"tel:{digits}" if digits else "tel:"


def ensure_assets() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "style.css").write_text(
        """:root {\n"
        "  font-family: 'Noto Sans TC', 'Noto Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;\n"
        "  color: #0f172a;\n"
        "  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);\n"
        "}\n"
        "* { box-sizing: border-box; }\n"
        "body { margin: 0; line-height: 1.6; }\n"
        "a { color: #2563eb; text-decoration: none; }\n"
        "a:hover { text-decoration: underline; }\n"
        "header { text-align: center; padding: 3rem 1rem 2rem; }\n"
        "h1 { margin: 0 0 0.5rem; font-size: clamp(2rem, 5vw, 2.8rem); }\n"
        "p.lead { margin: 0; color: #334155; font-size: 1.1rem; }\n"
        "main { max-width: 1100px; margin: 0 auto; padding: 0 1rem 3rem; }\n"
        ".grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; }\n"
        ".card { background: #fff; border-radius: 14px; overflow: hidden; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08); display: flex; flex-direction: column; min-height: 100%; }\n"
        ".card img { width: 100%; height: 170px; object-fit: cover; }\n"
        ".card__body { padding: 1rem 1.1rem 1.4rem; display: flex; flex-direction: column; gap: 0.35rem; flex: 1; }\n"
        ".badge { display: inline-flex; align-items: center; gap: 0.35rem; background: #eef2ff; color: #4338ca; padding: 0.15rem 0.6rem; border-radius: 999px; font-weight: 600; width: fit-content; }\n"
        ".meta { color: #475569; font-size: 0.98rem; }\n"
        ".actions { margin-top: auto; display: flex; gap: 0.5rem; flex-wrap: wrap; }\n"
        ".button { display: inline-flex; align-items: center; justify-content: center; gap: 0.4rem; padding: 0.65rem 0.9rem; border-radius: 10px; border: 1px solid #cbd5e1; background: #f8fafc; color: inherit; font-weight: 600; transition: transform 120ms ease, box-shadow 120ms ease; }
        .button:hover { transform: translateY(-1px); box-shadow: 0 8px 18px rgba(15, 23, 42, 0.12); }
        .button.primary { background: linear-gradient(120deg, #2563eb, #4f46e5); color: #fff; border: none; }
        .button.secondary { background: #fff; }
        .pill { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.4rem 0.65rem; border-radius: 999px; background: #ecfeff; color: #0f172a; border: 1px solid #bae6fd; font-weight: 600; }
        .store-header { max-width: 960px; margin: 0 auto; padding: 3rem 1rem 0; }
        .store-main { max-width: 960px; margin: 0 auto 3rem; padding: 1.5rem 1rem 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; align-items: start; }
        .hero { border-radius: 18px; overflow: hidden; box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12); }
        .hero img { width: 100%; height: 100%; object-fit: cover; }
        .store-card { background: #fff; border-radius: 16px; padding: 1.2rem 1.4rem; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08); display: flex; flex-direction: column; gap: 0.6rem; }
        .breadcrumbs { display: inline-flex; gap: 0.5rem; align-items: center; color: #475569; font-weight: 600; text-decoration: none; }
        .breadcrumbs:hover { color: #2563eb; }
        footer { text-align: center; padding: 2rem 1rem 3rem; color: #475569; }
        """,
        encoding="utf-8",
    )


def build_index(stores: List[Dict[str, str]]) -> None:
    cards = []
    for store in stores:
        cards.append(
            f"<article class='card'>"
            f"<img src='{html.escape(store['photo_url'])}' alt='{html.escape(store['name'])} 照片'>"
            "<div class='card__body'>"
            f"<span class='badge'>⭐ {html.escape(store['rating'])}</span>"
            f"<h2><a href='stores/{store['slug']}.html'>{html.escape(store['name'])}</a></h2>"
            f"<p class='meta'>{html.escape(store['address'])}</p>"
            f"<div class='actions'>"
            f"<a class='button primary' href='stores/{store['slug']}.html'>查看店家</a>"
            f"<a class='button secondary' href='{html.escape(store['map_url'])}' target='_blank' rel='noreferrer'>Google 地圖</a>"
            "</div>"
            "</div>"
            "</article>"
        )

    DOCS.mkdir(exist_ok=True)
    DOCS.joinpath("index.html").write_text(
        """<!doctype html>
<html lang='zh-Hant'>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>鎖印行地圖 | GitHub Pages</title>
    <link rel='stylesheet' href='assets/style.css'>
  </head>
  <body>
    <header>
      <p class='pill'>GitHub Pages 靜態網站</p>
      <h1>三重鎖印行索引</h1>
      <p class='lead'>每一筆資料都對應一個獨立的店家頁面，方便瀏覽與分享。</p>
    </header>
    <main>
      <div class='grid'>
"""
        + "\n".join(cards)
        + "\n      </div>\n    </main>\n    <footer>資料來源：key.csv · 透過 build.py 生成</footer>\n  </body>\n</html>\n",
        encoding="utf-8",
    )


def build_store_page(store: Dict[str, str]) -> None:
    STORES_DIR.mkdir(parents=True, exist_ok=True)
    STORES_DIR.joinpath(f"{store['slug']}.html").write_text(
        f"""<!doctype html>
<html lang='zh-Hant'>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>{html.escape(store['name'])} | 鎖印行</title>
    <link rel='stylesheet' href='../assets/style.css'>
  </head>
  <body>
    <div class='store-header'>
      <a class='breadcrumbs' href='../index.html'>← 回到總覽</a>
      <h1>{html.escape(store['name'])}</h1>
      <p class='lead'>Google 評論 {html.escape(store['rating'])} 分 · {html.escape(store['address'])}</p>
    </div>
    <div class='store-main'>
      <div class='hero'>
        <img src='{html.escape(store['photo_url'])}' alt='{html.escape(store['name'])} 店面照片'>
      </div>
      <div class='store-card'>
        <div class='badge'>店家資訊</div>
        <div class='meta'>
          <strong>地址：</strong>{html.escape(store['address'])}
        </div>
        <div class='meta'>
          <strong>電話：</strong><a href='{tel_link(store['phone'])}'>{html.escape(store['phone'])}</a>
        </div>
        <div class='meta'>
          <strong>Google 地圖：</strong><a href='{html.escape(store['map_url'])}' target='_blank' rel='noreferrer'>查看地圖</a>
        </div>
        <div class='actions'>
          <a class='button primary' href='{html.escape(store['map_url'])}' target='_blank' rel='noreferrer'>在地圖開啟</a>
          <a class='button secondary' href='../index.html'>回到索引</a>
        </div>
      </div>
    </div>
    <footer>以 GitHub Pages 供應 · 從 key.csv 自動生成</footer>
  </body>
</html>
""",
        encoding="utf-8",
    )


def main() -> None:
    stores = load_stores()
    ensure_assets()

    for store in stores:
        fallback = f"store-{store['id']}"
        store["slug"] = f"{store['id']}-{slugify(store['name'], fallback)}"

    build_index(stores)
    for store in stores:
        build_store_page(store)

    print(f"已完成 {len(stores)} 筆店家頁面，輸出至 {DOCS}/")


if __name__ == "__main__":
    main()
