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
  --bg: #f7f9fb;
  --panel: #ffffff;
  --text: #0f172a;
  --muted: #475569;
  --accent: #0ea5e9;
  --accent-2: #22c55e;
  --border: #e2e8f0;
  --shadow: 0 12px 30px rgba(14, 165, 233, 0.12);
  font-family: "Noto Sans TC", "Microsoft JhengHei", system-ui, -apple-system, sans-serif;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background:
    radial-gradient(120% 120% at 15% 20%, rgba(14, 165, 233, 0.08), transparent 45%),
    radial-gradient(80% 100% at 80% 0%, rgba(34, 197, 94, 0.08), transparent 40%),
    var(--bg);
  color: var(--text);
}

a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

header {
  padding: 56px 20px 36px;
  text-align: center;
  background:
    radial-gradient(120% 160% at 20% 20%, rgba(14, 165, 233, 0.18), transparent 50%),
    radial-gradient(120% 160% at 80% 0%, rgba(34, 197, 94, 0.18), transparent 55%),
    linear-gradient(135deg, #f8fbff 0%, #eef7ff 100%);
  position: relative;
  overflow: hidden;
}

main {
  max-width: 1100px;
  padding: 0 20px 64px;
  margin: 0 auto;
}

h1, h2, h3 { margin: 0 0 8px; letter-spacing: 0.2px; }

.header-content { max-width: 820px; margin: 0 auto; position: relative; z-index: 1; }

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(14, 165, 233, 0.12);
  color: #0369a1;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  font-size: 0.82rem;
}

.lead { color: var(--muted); margin: 12px auto 24px; max-width: 880px; line-height: 1.7; font-size: 1.04rem; }

.hero-meta {
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 12px;
  background: #fff;
  color: var(--muted);
  border: 1px solid var(--border);
  box-shadow: 0 4px 14px rgba(14, 165, 233, 0.1);
  font-weight: 600;
}

.pill.secondary { background: #0ea5e9; color: #f8fafc; border-color: transparent; }

.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 0 18px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 22px;
}

.card {
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  border: 1px solid rgba(226, 232, 240, 0.7);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  min-height: 100%;
  transition: transform 150ms ease, box-shadow 150ms ease, border-color 150ms ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(14, 165, 233, 0.14);
  border-color: rgba(14, 165, 233, 0.3);
}

.card img {
  width: 100%;
  height: 190px;
  object-fit: cover;
  filter: saturate(1.08);
}

.card-body { padding: 16px 16px 20px; display: flex; flex-direction: column; gap: 10px; }
.card h3 { font-size: 1.08rem; }
.card .meta { color: var(--muted); font-size: 0.95rem; line-height: 1.5; }
.card .actions { margin-top: auto; display: flex; gap: 10px; flex-wrap: wrap; }

.button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 13px;
  border-radius: 12px;
  background: var(--accent);
  color: white;
  font-weight: 600;
  font-size: 0.95rem;
  border: 1px solid transparent;
  transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
}

.button:hover { transform: translateY(-1px); box-shadow: 0 10px 18px rgba(14, 165, 233, 0.18); text-decoration: none; }
.button.secondary { background: #0b8fd2; }

.store-hero {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 20px;
  align-items: start;
  margin-top: 12px;
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
  padding: 18px;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 12px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid var(--border);
}

.info-row .label { color: var(--muted); font-weight: 700; }
.info-row .value { color: var(--text); font-weight: 700; }
.info-row a.value { color: var(--accent); font-weight: 700; }

.info-panel .actions { margin-top: 8px; display: flex; gap: 10px; flex-wrap: wrap; }

.back-link { margin-top: 24px; display: inline-flex; align-items: center; gap: 8px; }

@media (max-width: 720px) {
  .store-hero { grid-template-columns: 1fr; }
  .info-row { align-items: flex-start; }
  .info-row .value { text-align: right; }
}
''',
        encoding='utf-8',
    )


def build_index(stores: List[Dict[str, str]]) -> None:
    store_count = len(stores)
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
            f"<p class='meta'>評論分數：{rating}</p>"
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
  <title>三重鎖印行導覽｜GitHub Pages</title>
  <link rel='stylesheet' href='assets/style.css'>
</head>
<body>
  <header>
    <div class='header-content'>
      <p class='eyebrow'>三重鎖匠指南</p>
      <h1>三重鎖印行導覽</h1>
      <p class='lead'>三重地區的鎖印行，拯救打不開門的您</p>
      <div class='hero-meta'>
        <span class='pill'>一次看遍 {store_count} 家鎖印行</span>
        <span class='pill secondary'>快速找到就近的求助據點</span>
      </div>
    </div>
  </header>
  <main>
    <div class='section-heading'>
      <div>
        <p class='eyebrow'>鎖印行列表</p>
        <h2>鄰近推薦</h2>
      </div>
    </div>
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
  <title>{name}｜三重鎖印行導覽</title>
  <link rel='stylesheet' href='../assets/style.css'>
</head>
<body>
  <header>
    <div class='header-content'>
      <p class='eyebrow'>三重鎖印行導覽</p>
      <h1>{name}</h1>
    </div>
  </header>
  <main>
    <section class='store-hero'>
      <img src='{image}' alt='{name} 的照片'>
      <div class='info-panel'>
        <div class='info-row'>
          <span class='label'>評論分數</span>
          <span class='value'>{rating}</span>
        </div>
        <div class='info-row'>
          <span class='label'>地址</span>
          <a class='value' href='{map_link}' target='_blank' rel='noopener'>{address}</a>
        </div>
        <div class='info-row'>
          <span class='label'>聯絡電話</span>
          <a class='value' href='tel:{phone_link}'>{phone_display}</a>
        </div>
        <div class='info-row'>
          <span class='label'>地圖</span>
          <a class='value' href='{map_link}' target='_blank' rel='noopener'>在 Google 地圖查看</a>
        </div>
        <div class='actions'>
          <a class='button' href='tel:{phone_link}'>立即撥打</a>
          <a class='button secondary' href='{map_link}' target='_blank' rel='noopener'>查看地圖路線</a>
        </div>
      </div>
    </section>
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
