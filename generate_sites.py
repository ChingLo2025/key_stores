import csv
import html
import re
from pathlib import Path
from typing import Dict, List

DATA_FILE = Path('key.csv')
DOCS_DIR = Path('docs')
ASSETS_DIR = DOCS_DIR / 'assets'
STORE_DIR = DOCS_DIR / 'stores'
ENCODING = 'big5hkscs'


def slugify(name: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", name.strip())
    slug = re.sub(r"-+", "-", cleaned).strip('-')
    return slug or 'store'


def load_rows() -> List[Dict[str, str]]:
    with DATA_FILE.open(encoding=ENCODING, newline='') as handle:
        reader = csv.DictReader(handle)
        rows = [dict(row) for row in reader]
    return rows


def ensure_directories() -> None:
    for path in (DOCS_DIR, ASSETS_DIR, STORE_DIR):
        path.mkdir(parents=True, exist_ok=True)


def write_css() -> None:
    style_path = ASSETS_DIR / 'style.css'
    style_path.write_text(
        r''':root {
  --bg: #f9fafb;
  --panel: #ffffff;
  --text: #1f2937;
  --muted: #4b5563;
  --accent: #0f766e;
  --border: #e5e7eb;
  --shadow: 0 10px 25px rgba(15, 118, 110, 0.08);
  font-family: "Noto Sans TC", "Microsoft JhengHei", system-ui, -apple-system, sans-serif;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

header {
  padding: 32px 20px 8px;
  text-align: center;
}

main {
  max-width: 1100px;
  padding: 0 20px 48px;
  margin: 0 auto;
}

h1, h2, h3 { margin: 0 0 8px; }

.lead { color: var(--muted); margin: 0 auto 24px; max-width: 800px; line-height: 1.6; }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 18px;
}

.card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.card-body { padding: 14px 14px 18px; display: flex; flex-direction: column; gap: 8px; }
.card h3 { font-size: 1.05rem; }
.card .meta { color: var(--muted); font-size: 0.95rem; }
.card .actions { margin-top: auto; display: flex; gap: 10px; flex-wrap: wrap; }

.button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 12px;
  background: var(--accent);
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
}

.button.secondary { background: #0ea5e9; }

.store-hero {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 20px;
  align-items: start;
}

.store-hero img {
  width: 100%;
  border-radius: 16px;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

.info-panel {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px;
  box-shadow: var(--shadow);
}

.info-panel p { margin: 8px 0; }
.info-panel strong { display: inline-block; width: 120px; color: var(--muted); }

.back-link { margin-top: 24px; display: inline-flex; align-items: center; gap: 8px; }

@media (max-width: 720px) {
  .store-hero { grid-template-columns: 1fr; }
  .info-panel strong { width: auto; margin-right: 10px; }
}
''',
        encoding='utf-8',
    )


def build_index(stores: List[Dict[str, str]]) -> None:
    cards = []
    for store in stores:
        slug = store['slug']
        name = html.escape(store['店名'])
        rating = html.escape(store.get('Google評論分數', ''))
        address = html.escape(store.get('地址', ''))
        image = html.escape(store.get('照片', ''))
        cards.append(
            f"<article class='card'>"
            f"<img src='{image}' alt='{name} 的照片'>"
            f"<div class='card-body'>"
            f"<h3>{name}</h3>"
            f"<p class='meta'>Google 評分：{rating}</p>"
            f"<p class='meta'>{address}</p>"
            f"<div class='actions'>"
            f"<a class='button' href='stores/{slug}.html'>查看詳情</a>"
            f"<a class='button secondary' href='{html.escape(store.get('Google地圖連結', ''))}' target='_blank' rel='noopener'>在 Google 地圖查看</a>"
            f"</div>"
            f"</div>"
            f"</article>"
        )

    content = f"""<!doctype html>
<html lang='zh-Hant'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>鎖印行地圖｜GitHub Pages</title>
  <link rel='stylesheet' href='assets/style.css'>
</head>
<body>
  <header>
    <h1>鎖印行地圖</h1>
    <p class='lead'>依照資料表為每一家鎖印行建立了獨立的介紹頁面，方便透過 GitHub Pages 快速瀏覽與分享。</p>
  </header>
  <main>
    <section class='grid'>
      {''.join(cards)}
    </section>
  </main>
</body>
</html>"""
    (DOCS_DIR / 'index.html').write_text(content, encoding='utf-8')


def sanitize_phone(phone: str) -> str:
    digits = re.sub(r"[^0-9+]", "", phone)
    return digits or phone


def build_store_page(store: Dict[str, str]) -> None:
    name = html.escape(store['店名'])
    slug = store['slug']
    map_link = html.escape(store.get('Google地圖連結', ''))
    address = html.escape(store.get('地址', ''))
    phone = store.get('聯絡電話', '')
    phone_display = html.escape(phone)
    phone_link = html.escape(sanitize_phone(phone))
    rating = html.escape(store.get('Google評論分數', ''))
    image = html.escape(store.get('照片', ''))

    content = f"""<!doctype html>
<html lang='zh-Hant'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>{name}｜鎖印行地圖</title>
  <link rel='stylesheet' href='../assets/style.css'>
</head>
<body>
  <header>
    <h1>{name}</h1>
    <p class='lead'>這個頁面使用資料表中的資訊建立，提供位置、聯絡方式與 Google 地圖連結。</p>
  </header>
  <main>
    <div class='store-hero'>
      <img src='{image}' alt='{name} 的照片'>
      <div class='info-panel'>
        <p><strong>Google 評論分數</strong>{rating}</p>
        <p><strong>地址</strong><a href='{map_link}' target='_blank' rel='noopener'>{address}</a></p>
        <p><strong>聯絡電話</strong><a href='tel:{phone_link}'>{phone_display}</a></p>
        <p><strong>Google 地圖</strong><a href='{map_link}' target='_blank' rel='noopener'>在地圖開啟</a></p>
      </div>
    </div>
    <a class='back-link' href='../index.html'>← 返回所有鎖印行</a>
  </main>
</body>
</html>"""

    (STORE_DIR / f"{slug}.html").write_text(content, encoding='utf-8')


def main() -> None:
    ensure_directories()
    write_css()
    stores = load_rows()
    for store in stores:
        store['slug'] = slugify(store.get('店名', 'store'))
    build_index(stores)
    for store in stores:
        build_store_page(store)
    print(f"Generated {len(stores)} store pages in {STORE_DIR}/")


if __name__ == '__main__':
    main()
