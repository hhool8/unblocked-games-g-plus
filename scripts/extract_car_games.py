#!/usr/bin/env python3
"""
extract_car_games.py
Parses category/car.html, reads each game's English description,
then writes two outputs into scripts/:
  car_games.csv              – slug, name, image, description, link
  car_games_googlesite.html  – self-contained embed for Google Sites
                               (Insert → Embed → Embed code → paste)
"""
import re, csv, html as html_lib
from pathlib import Path

BASE        = Path(__file__).parent.parent
CAT_FILE    = BASE / "category" / "car.html"
GAME_DIR    = BASE / "game"
SCRIPTS_DIR = Path(__file__).parent
IMG_PREFIX  = "https://unblocked-games-g-plus.poki2.online"
PLAY_PREFIX = "https://unblocked-games-g-plus.poki2.online/play"
LINK_PREFIX = "https://sites.google.com/view/unblocked-games-g-site"
OUT_CSV     = SCRIPTS_DIR / "car_games.csv"
OUT_HTML    = SCRIPTS_DIR / "car_games_googlesite.html"

RE_CARD      = re.compile(r'<a class="card" href="/game/([^"]+)">(.*?)</a>', re.DOTALL)
RE_IMG       = re.compile(r'src="([^"]+)"')
RE_NAME      = re.compile(r'<h3>(.*?)</h3>')
RE_DESC_DIV  = re.compile(r'class="description pb-2">\s*<h3[^>]*>.*?</h3>\s*<p>(.*?)</p>', re.DOTALL)
RE_META_DESC = re.compile(r'<meta\s+name="description"\s+content="([^"]+)"', re.I)

# ── 1. Extract data ──────────────────────────────────────────────────────────
cat_html = CAT_FILE.read_text(encoding="utf-8")
results  = []

for slug_html, body in RE_CARD.findall(cat_html):
    slug    = slug_html.replace(".html", "")
    img_m   = RE_IMG.search(body)
    name_m  = RE_NAME.search(body)
    img_url = IMG_PREFIX + (img_m.group(1) if img_m else "")
    name    = (name_m.group(1) if name_m else slug).upper()

    game_file = GAME_DIR / slug_html
    desc = ""
    if game_file.exists():
        ghtml = game_file.read_text(encoding="utf-8", errors="ignore")
        dm = RE_DESC_DIV.search(ghtml)
        if dm:
            desc = dm.group(1).strip()
        else:
            mm = RE_META_DESC.search(ghtml)
            if mm:
                desc = mm.group(1).strip()

    results.append({
        "slug":        slug,
        "name":        name,
        "image":       img_url,
        "description": desc,
        "play_url":    f"{PLAY_PREFIX}/{slug_html}",
        "link":        f"{LINK_PREFIX}/{slug}",
    })

# ── 2. Write CSV ─────────────────────────────────────────────────────────────
with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["slug", "name", "image", "description", "play_url", "link"])
    w.writeheader()
    w.writerows(results)

# ── 3. Build Google-Sites-embeddable HTML ────────────────────────────────────
cards_html = ""
for r in results:
    clean_desc = " ".join(r["description"].split())
    cards_html += (
        f'\n<article class="gc">'
        f'<a href="{r["link"]}">'  # open in same window
        f'<img src="{r["image"]}" alt="{html_lib.escape(r["name"])}" loading="lazy" width="180" height="180">'
        f'<div class="gi">'
        f'<h3>{html_lib.escape(r["name"])}</h3>'
        f'<p>{html_lib.escape(clean_desc)}</p>'
        f'</div></a></article>'
    )

page = (
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    '<title>Car Games \u2013 Unblocked Games G+</title>\n'
    '<style>\n'
    '*{box-sizing:border-box;margin:0;padding:0}\n'
    'body{font-family:Arial,Helvetica,sans-serif;background:#f4f6fb;padding:14px}\n'
    'h1.cat{text-align:center;font-size:20px;font-weight:800;color:#1a237e;'
    'text-transform:uppercase;letter-spacing:.6px;margin-bottom:16px}\n'
    '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:14px}\n'
    '.gc{background:#fff;border-radius:12px;overflow:hidden;'
    'box-shadow:0 2px 8px rgba(0,0,0,.10);transition:transform .18s,box-shadow .18s}\n'
    '.gc:hover{transform:translateY(-5px);box-shadow:0 8px 22px rgba(0,0,0,.18)}\n'
    '.gc a{display:block;text-decoration:none;color:inherit}\n'
    '.gc img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}\n'
    '.gi{padding:8px 10px 12px}\n'
    '.gi h3{font-size:13px;font-weight:700;color:#1a237e;margin-bottom:5px;'
    'white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n'
    '.gi p{font-size:11px;color:#555;line-height:1.55;'
    'display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}\n'
    '</style>\n</head>\n<body>\n'
    '<h1 class="cat">&#x1F697; Car Games</h1>\n'
    '<div class="grid">'
    + cards_html +
    '\n</div>\n</body>\n</html>\n'
)

OUT_HTML.write_text(page, encoding="utf-8")

# ── 4. Summary ───────────────────────────────────────────────────────────────
csv_kb  = OUT_CSV.stat().st_size  / 1024
html_kb = OUT_HTML.stat().st_size / 1024
limit   = "OK \u2705" if html_kb < 100 else "OVER LIMIT \u26a0\ufe0f"

print(f"\u2713 {len(results)} car games extracted")
print(f"  CSV  ({csv_kb:.1f} KB)  \u2192  {OUT_CSV}")
print(f"  HTML ({html_kb:.1f} KB / 100 KB limit \u2192 {limit})  \u2192  {OUT_HTML}")
print()
print(f"{'No.':<4} {'slug':<45} {'play_url'}")
print("-" * 100)
for i, r in enumerate(results, 1):
    print(f"{i:<4} {r['slug']:<45} {r['play_url']}")
