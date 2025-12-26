from __future__ import annotations

import csv
import html
import re
import unicodedata
from pathlib import Path
from typing import List, Dict

DATA_FILE = Path("key.csv")
DOCS_DIR = Path("docs")
ASSETS_DIR = DOCS_DIR / "assets"
STORES_DIR = DOCS_DIR / "stores"


Store = Dict[str, str]


def load_stores() -> List[Store]:
    text = DATA_FILE.read_text(encoding="cp950")
    reader = csv.DictReader(text.splitlines())
    stores: List[Store] = []
    for row in reader:
        stores.append(
            {
                "map_url": row["Google地圖連結"].strip(),
                "name": row["店名"].strip(),
                "image_url": row["照片"].strip(),
                "rating": row["Google評論分數"].strip(),
                "address": row["地址"].strip(),
                "phone": row["聯絡電話"].strip(),
            }
        )
    return stores


def to_slug(name: str, index: int) -> str:
    # Keep a stable numeric prefix so URLs stay predictable even if names change.
    base = f"store-{index + 1}"
    normalized = unicodedata.normalize("NFKD", name)
    ascii_only = normalized.encode("ascii", "ignore").decode()
    safe_chars = "".join(ch for ch in ascii_only.lower() if ch.isalnum() or ch in {" ", "-"})
    cleaned = "-".join(part for part in re.split(r"[\s-]+", safe_chars) if part)
    return f"{base}-{cleaned}" if cleaned else base


def ensure_structure() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    STORES_DIR.mkdir(parents=True, exist_ok=True)


def write_css() -> None:
    css = """
    :root {
        --background: #0f172a;
        --card: #111827;
        --accent: #10b981;
        --text: #e5e7eb;
        --muted: #9ca3af;
        --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.45);
        --radius: 16px;
        --max-width: 1100px;
    }

    * { box-sizing: border-box; }

    body {
        margin: 0;
        font-family: "Inter", "Noto Sans TC", "Helvetica Neue", Arial, sans-serif;
        background: radial-gradient(circle at 10% 10%, rgba(16,185,129,0.12), transparent 35%),
                    radial-gradient(circle at 90% 20%, rgba(59,130,246,0.1), transparent 30%),
                    var(--background);
        color: var(--text);
        min-height: 100vh;
    }

    header {
        padding: 48px 24px 24px;
        text-align: center;
    }

    header h1 {
        margin: 0 0 12px;
        font-size: clamp(28px, 3vw, 40px);
        letter-spacing: 0.02em;
    }

    header p {
        margin: 0;
        color: var(--muted);
        font-size: 16px;
    }

    main {
        padding: 0 24px 48px;
        display: grid;
        gap: 20px;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        max-width: var(--max-width);
        margin: 0 auto;
    }

    .card, .store-page {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.92), rgba(17, 24, 39, 0.7));
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        overflow: hidden;
        backdrop-filter: blur(6px);
    }

    .card img, .hero img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        display: block;
    }

    .card-content {
        padding: 16px;
        display: grid;
        gap: 10px;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.16);
        color: var(--text);
        padding: 6px 12px;
        border-radius: 999px;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }

    .meta {
        display: grid;
        gap: 6px;
        color: var(--muted);
        line-height: 1.5;
        font-size: 14px;
    }

    a.button {
        text-decoration: none;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #10b981, #34d399);
        color: #0b1221;
        padding: 10px 14px;
        border-radius: 12px;
        font-weight: 700;
        letter-spacing: 0.01em;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.25);
    }

    a.button.secondary {
        background: transparent;
        color: var(--text);
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: none;
    }

    a.button:hover {
        transform: translateY(-2px);
    }

    .store-page {
        max-width: 900px;
        margin: 32px auto;
        padding-bottom: 24px;
    }

    .store-body {
        padding: 20px 24px 8px;
        display: grid;
        gap: 16px;
    }

    .hero {
        position: relative;
    }

    .hero h2 {
        position: absolute;
        left: 20px;
        bottom: 16px;
        margin: 0;
        padding: 10px 14px;
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.78);
        backdrop-filter: blur(4px);
        font-size: 22px;
    }

    .info-grid {
        display: grid;
        gap: 12px;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    }

    .info-card {
        padding: 14px 16px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        background: rgba(255, 255, 255, 0.02);
        display: grid;
        gap: 6px;
    }

    .info-card span.label {
        font-size: 13px;
        color: var(--muted);
        letter-spacing: 0.02em;
    }

    footer {
        text-align: center;
        color: var(--muted);
        padding: 20px 0 36px;
        font-size: 14px;
    }
    """
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    (ASSETS_DIR / "style.css").write_text(css.strip() + "\n", encoding="utf-8")


def render_index(stores: List[Store]) -> str:
    cards = []
    for store in stores:
        cards.append(
            f"""
            <article class=\"card\">
                <img src=\"{html.escape(store['image_url'])}\" alt=\"{html.escape(store['name'])}\" loading=\"lazy\" />
                <div class=\"card-content\">
                    <div class=\"badge\">⭐ {html.escape(store['rating'])} Google 評分</div>
                    <h2>{html.escape(store['name'])}</h2>
                    <div class=\"meta\">
                        <div>📍 {html.escape(store['address'])}</div>
                        <div>📞 {html.escape(store['phone'])}</div>
                    </div>
                    <div style=\"display:flex; gap:10px; flex-wrap:wrap;\">
                        <a class=\"button\" href=\"stores/{store['slug']}/\">進入分店網站</a>
                        <a class=\"button secondary\" href=\"{html.escape(store['map_url'])}\" target=\"_blank\" rel=\"noopener\">查看地圖</a>
                    </div>
                </div>
            </article>
            """
        )

    return f"""
    <!doctype html>
    <html lang=\"zh-Hant\">
    <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
        <title>三重區鎖印行地圖 | Locksmith Directory</title>
        <link rel=\"stylesheet\" href=\"assets/style.css\" />
    </head>
    <body>
        <header>
            <h1>三重鎖印行地圖</h1>
            <p>依據 Google 地圖資料，每筆鎖印行都擁有獨立介紹頁面。</p>
        </header>
        <main>
            {"".join(cards)}
        </main>
        <footer>資料來源：key.csv（Big5 / CP950 編碼）</footer>
    </body>
    </html>
    """


def render_store(store: Store) -> str:
    return f"""
    <!doctype html>
    <html lang=\"zh-Hant\">
    <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
        <title>{html.escape(store['name'])} | 鎖印行介紹</title>
        <link rel=\"stylesheet\" href=\"../../assets/style.css\" />
    </head>
    <body>
        <div class=\"store-page\">
            <div class=\"hero\">
                <img src=\"{html.escape(store['image_url'])}\" alt=\"{html.escape(store['name'])}\" loading=\"lazy\" />
                <h2>{html.escape(store['name'])}</h2>
            </div>
            <div class=\"store-body\">
                <div class=\"badge\">⭐ {html.escape(store['rating'])} Google 評分</div>
                <div class=\"info-grid\">
                    <div class=\"info-card\">
                        <span class=\"label\">地址</span>
                        <div>{html.escape(store['address'])}</div>
                    </div>
                    <div class=\"info-card\">
                        <span class=\"label\">聯絡電話</span>
                        <div>{html.escape(store['phone'])}</div>
                    </div>
                    <div class=\"info-card\">
                        <span class=\"label\">Google 地圖</span>
                        <a class=\"button secondary\" href=\"{html.escape(store['map_url'])}\" target=\"_blank\" rel=\"noopener\">開啟地圖</a>
                    </div>
                </div>
                <div style=\"display:flex; gap:10px; flex-wrap:wrap;\">
                    <a class=\"button\" href=\"{html.escape(store['map_url'])}\" target=\"_blank\" rel=\"noopener\">導航到店</a>
                    <a class=\"button secondary\" href=\"../../index.html\">返回總覽</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


def build_site() -> None:
    ensure_structure()
    stores = load_stores()
    for index, store in enumerate(stores):
        slug = to_slug(store["name"], index)
        store["slug"] = slug
        page_dir = STORES_DIR / slug
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(render_store(store), encoding="utf-8")
    write_css()
    (DOCS_DIR / "index.html").write_text(render_index(stores), encoding="utf-8")

    # Remove any leftover folders from previous slug generation to keep the
    # published site tidy. We only remove directories that start with "store-"
    # and are not part of the current store set.
    valid = {store["slug"] for store in stores}
    for folder in STORES_DIR.iterdir():
        if folder.is_dir() and folder.name.startswith("store-") and folder.name not in valid:
            for child in folder.glob("**/*"):
                if child.is_file():
                    child.unlink()
            folder.rmdir()


if __name__ == "__main__":
    build_site()
    print(f"✅ Generated {len(load_stores())} store pages in {STORES_DIR.relative_to(Path('.'))}/")
