from __future__ import annotations

import csv
import html
import os
import re
from pathlib import Path
from typing import Dict, List

DATA_PATH = Path("key.csv")
OUTPUT_DIR = Path("docs")
ASSETS_DIR = OUTPUT_DIR / "assets"
STORES_DIR = OUTPUT_DIR / "stores"
ENCODING = "cp950"


def load_stores() -> List[Dict[str, str]]:
    text = DATA_PATH.read_text(encoding=ENCODING)
    reader = csv.DictReader(text.splitlines())
    stores: List[Dict[str, str]] = []

    for index, row in enumerate(reader, start=1):
        rating_text = row.get("Google評論分數", "").strip()
        try:
            rating_value = float(rating_text)
        except ValueError:
            rating_value = None

        store = {
            "id": index,
            "slug": f"store-{index}",
            "name": row.get("店名", "").strip(),
            "map_url": row.get("Google地圖連結", "").strip(),
            "photo_url": row.get("照片", "").strip(),
            "rating_text": rating_text,
            "rating_value": rating_value,
            "address": row.get("地址", "").strip(),
            "phone": row.get("聯絡電話", "").strip(),
        }
        stores.append(store)
    return stores


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def rel_asset_path(current_file: Path, filename: str) -> str:
    rel = os.path.relpath(ASSETS_DIR / filename, current_file.parent)
    return Path(rel).as_posix()


def render_layout(title: str, description: str, body: str, current_file: Path) -> str:
    stylesheet = rel_asset_path(current_file, "style.css")
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(description)}">
  <link rel="stylesheet" href="{stylesheet}">
</head>
<body>
  <header class="site-header">
    <div class="content">
      <div class="brand">
        <div class="dot"></div>
        <div>
          <p class="eyebrow">三重鎖印行指南</p>
          <p class="brand__title">Key Stores Directory</p>
        </div>
      </div>
      <nav class="actions">
        <a class="nav-link" href="{Path(os.path.relpath(OUTPUT_DIR, current_file.parent)).as_posix()}/">首頁</a>
      </nav>
    </div>
  </header>
  <main class="content">
    {body}
  </main>
  <footer class="site-footer">
    <div class="content footer__content">
      <div>
        <p class="eyebrow">GitHub Pages</p>
        <p class="muted">此靜態網站由 <code>generate_site.py</code> 依照鎖印行列表自動產生。</p>
      </div>
      <a class="nav-link" href="#top">回到頂部</a>
    </div>
  </footer>
</body>
</html>
"""


def rating_badge(store: Dict[str, str]) -> str:
    if not store["rating_text"]:
        return ""
    stars = ""
    if store["rating_value"]:
        filled = int(store["rating_value"])
        half_star = store["rating_value"] - filled >= 0.5
        stars = "★" * filled + ("☆" if half_star else "")
    return f'<span class="rating">★ {html.escape(store["rating_text"])} {stars}</span>'


def build_index(stores: List[Dict[str, str]]) -> None:
    cards = []
    for store in stores:
        link = Path("stores") / store["slug"] / "index.html"
        cards.append(
            f"""
      <article class="store-card">
        <div class="store-card__media">
          <img src="{html.escape(store['photo_url'])}" alt="{html.escape(store['name'])}">
        </div>
        <div class="store-card__body">
          <p class="eyebrow">第 {store['id']} 筆</p>
          <h3>{html.escape(store['name'])}</h3>
          <p class="muted">{html.escape(store['address'])}</p>
          <div class="store-card__footer">
            {rating_badge(store)}
            <a class="button" href="{link.as_posix()}">查看獨立網站</a>
          </div>
        </div>
      </article>
"""
        )

    body = f"""
  <section class="hero">
    <div>
      <p class="eyebrow">資料來源</p>
      <h1>三重鎖印行 GitHub Pages</h1>
      <p class="lead">為 {len(stores)} 間鎖印行自動生成專屬網站，方便分享、導航與聯絡。</p>
      <div class="pill-group">
        <span class="pill">自動化建置</span>
        <span class="pill">Google 地圖連結</span>
        <span class="pill">地址與電話</span>
      </div>
    </div>
  </section>
  <section class="grid">
    {''.join(cards)}
  </section>
"""

    content = render_layout(
        "三重鎖印行 GitHub Pages",
        "為每一間鎖印行建立 GitHub Pages 獨立網站，方便導航與聯絡。",
        body,
        OUTPUT_DIR / "index.html",
    )
    write_file(OUTPUT_DIR / "index.html", content)


def build_store_page(store: Dict[str, str]) -> None:
    current_file = STORES_DIR / store["slug"] / "index.html"
    phone_digits = re.sub(r"\D+", "", store["phone"])
    tel_link = f"tel:{phone_digits}" if phone_digits else ""

    body = f"""
  <section class="store-hero">
    <div>
      <p class="eyebrow">鎖印行獨立網站</p>
      <h1>{html.escape(store['name'])}</h1>
      <p class="lead">地址：{html.escape(store['address'])}</p>
      <div class="pill-group">
        {rating_badge(store)}
        {'<span class="pill">聯絡電話：' + html.escape(store['phone']) + '</span>' if store['phone'] else ''}
      </div>
      <div class="button-row">
        <a class="button primary" target="_blank" rel="noopener" href="{html.escape(store['map_url'])}">在 Google 地圖查看</a>
        {'<a class="button secondary" href="' + tel_link + '">立即撥打</a>' if tel_link else ''}
        <a class="button ghost" href="../../">返回所有店家</a>
      </div>
    </div>
    <div class="store-hero__media">
      <img src="{html.escape(store['photo_url'])}" alt="{html.escape(store['name'])}">
    </div>
  </section>
  <section class="store-details">
    <h2>店家資訊</h2>
    <dl class="detail-list">
      <dt>Google 地圖</dt>
      <dd><a class="nav-link" target="_blank" rel="noopener" href="{html.escape(store['map_url'])}">前往連結</a></dd>
      <dt>地址</dt>
      <dd>{html.escape(store['address'])}</dd>
      <dt>電話</dt>
      <dd>{html.escape(store['phone']) if store['phone'] else '未提供'}</dd>
      <dt>Google 評論分數</dt>
      <dd>{html.escape(store['rating_text']) if store['rating_text'] else '未提供'}</dd>
    </dl>
  </section>
"""

    content = render_layout(
        f"{store['name']}｜鎖印行獨立網站",
        f"{store['name']} 的 GitHub Pages 店家資訊：{store['address']}",
        body,
        current_file,
    )
    write_file(current_file, content)


def build_assets() -> None:
    css = """
:root {
  --bg: #0b1021;
  --surface: #121832;
  --muted: #8ea0c2;
  --text: #e8edff;
  --accent: #7ce7fe;
  --accent-strong: #a9ff68;
  --border: #1f2747;
}

* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Inter", "Noto Sans TC", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: radial-gradient(circle at 10% 20%, rgba(124, 231, 254, 0.08), transparent 25%), radial-gradient(circle at 90% 10%, rgba(169, 255, 104, 0.08), transparent 25%), var(--bg);
  color: var(--text);
  line-height: 1.6;
}

a { color: var(--accent); text-decoration: none; }
img { max-width: 100%; display: block; border-radius: 14px; }
.content { width: min(1100px, 90vw); margin: 0 auto; }

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: rgba(11, 16, 33, 0.9);
  border-bottom: 1px solid var(--border);
  backdrop-filter: blur(12px);
}
.site-header .content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
}
.brand { display: grid; grid-template-columns: auto 1fr; gap: 10px; align-items: center; }
.brand__title { margin: 0; font-weight: 700; letter-spacing: 0.02em; }
.dot { width: 12px; height: 12px; background: linear-gradient(135deg, var(--accent), var(--accent-strong)); border-radius: 50%; box-shadow: 0 0 16px rgba(124, 231, 254, 0.7); }
.nav-link { color: var(--text); opacity: 0.9; font-weight: 600; }

.hero { padding: 64px 0 24px; }
.eyebrow { letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); font-size: 12px; margin: 0 0 6px; }
.lead { color: #cfd8f5; font-size: 18px; margin-top: 12px; }
.pill-group { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 16px; }
.pill { padding: 8px 12px; background: rgba(124, 231, 254, 0.08); border: 1px solid var(--border); border-radius: 999px; color: var(--text); }

.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; padding: 18px 0 64px; }
.store-card { background: rgba(18, 24, 50, 0.9); border: 1px solid var(--border); border-radius: 18px; overflow: hidden; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.28); display: flex; flex-direction: column; }
.store-card__media { aspect-ratio: 4 / 3; overflow: hidden; }
.store-card__media img { width: 100%; height: 100%; object-fit: cover; }
.store-card__body { padding: 16px; display: flex; flex-direction: column; gap: 8px; }
.store-card__body h3 { margin: 0; font-size: 20px; }
.store-card__footer { display: flex; align-items: center; justify-content: space-between; gap: 8px; flex-wrap: wrap; margin-top: 8px; }

.rating { background: rgba(169, 255, 104, 0.12); color: var(--accent-strong); border: 1px solid rgba(169, 255, 104, 0.4); padding: 6px 10px; border-radius: 12px; font-weight: 700; }
.muted { color: var(--muted); margin: 0; }

.button { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 14px; border-radius: 12px; border: 1px solid var(--border); color: var(--text); background: rgba(255, 255, 255, 0.02); font-weight: 700; transition: transform 0.15s ease, border-color 0.2s ease, box-shadow 0.2s ease; }
.button:hover { transform: translateY(-1px); border-color: var(--accent); box-shadow: 0 10px 30px rgba(124, 231, 254, 0.15); }
.button.primary { background: linear-gradient(135deg, var(--accent), var(--accent-strong)); color: #0b1021; border: none; }
.button.secondary { border-color: rgba(124, 231, 254, 0.6); color: var(--accent); }
.button.ghost { background: transparent; }
.button-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }

.store-hero { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; padding: 56px 0 32px; align-items: center; }
.store-hero__media { background: linear-gradient(135deg, rgba(124, 231, 254, 0.1), rgba(169, 255, 104, 0.05)); padding: 14px; border-radius: 18px; border: 1px solid var(--border); box-shadow: 0 30px 80px rgba(0, 0, 0, 0.25); }

.store-details { background: rgba(18, 24, 50, 0.7); border: 1px solid var(--border); border-radius: 18px; padding: 20px; margin-bottom: 48px; }
.store-details h2 { margin-top: 0; }
.detail-list { display: grid; grid-template-columns: 140px 1fr; gap: 8px 16px; margin: 0; }
.detail-list dt { color: var(--muted); font-weight: 600; }
.detail-list dd { margin: 0; }

.site-footer { border-top: 1px solid var(--border); padding: 16px 0 32px; color: var(--muted); background: rgba(11, 16, 33, 0.85); }
.footer__content { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }

@media (max-width: 640px) {
  .content { width: 92vw; }
  .detail-list { grid-template-columns: 1fr; }
}
"""
    write_file(ASSETS_DIR / "style.css", css.strip() + "\n")


def main() -> None:
    stores = load_stores()
    build_assets()
    build_index(stores)
    for store in stores:
        build_store_page(store)


if __name__ == "__main__":
    main()
