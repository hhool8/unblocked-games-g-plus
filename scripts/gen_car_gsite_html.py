#!/usr/bin/env python3
"""
gen_car_gsite_html.py
Parses category/car.html, reads each game page for its English description,
then writes scripts/car_games_googlesite.html — a self-contained page that
can be pasted directly into Google Sites via Insert → Embed → Embed code.

Output fields per game
  slug       : kebab-case identifier
  name       : display title (title-cased)
  image      : https://unblocked-games-g-plus.poki2.online/assets/…
  description: English text from the game page <div class="description">
  link       : https://sites.google.com/view/unblocked-games-g-site/{slug}.html
"""
import re, html as html_lib
from pathlib import Path

BASE        = Path(__file__).parent.parent
CAT_FILE    = BASE / "category" / "car.html"
GAME_DIR    = BASE / "game"
IMG_PREFIX  = "https://unblocked-games-g-plus.poki2.online"
LINK_PREFIX = "https://sites.google.com/view/unblocked-games-g-site"
OUT         = Path(__file__).parent / "car_games_googlesite.html"

# ── 1. Extract game cards from car.html ─────────────────────────────────────
cat_html = CAT_FILE.read_text(encoding="utf-8")
cards = re.findall(
    r'<a class="card" href="/game/([^"]+)">(.*?)</a>',
    cat_html, re.DOTALL
)

RE_IMG  = re.compile(r'src="([^"]+)"')
RE_NAME = re.compile(r'<h3>(.*?)</h3>')
RE_DESC_BLOCK = re.compile(
    r'class="description pb-2">\s*<h3[^>]*>.*?</h3>\s*<p>(.*?)</p>',
    re.DOTALL
)
RE_META_DESC = re.compile(r'<meta\s+name="description"\s+content="([^"]+)"', re.I)

results = []
for slug_html, body in cards:
    slug    = slug_html.replace(".html", "")
    img_rel = RE_IMG.search(body)
    name_m  = RE_NAME.search(body)
    img_url = IMG_PREFIX + (img_rel.group(1) if img_rel else "")
    name    = (name_m.group(1) if name_m else slug).title()

    game_file = GAME_DIR / slug_html
    desc = ""
    if game_file.exists():
        ghtml = game_file.read_text(encoding="utf-8", errors="ignore")
        dm = RE_DESC_BLOCK.search(ghtml)
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
        "link":        f"{LINK_PREFIX}/{slug_html}",
    })

# ── 2. Build card HTML ───────────────────────────────────────────────────────
cards_html = ""
for r in results:
    clean_desc = " ".join(r["description"].split())   # collapse whitespace
    cards_html += (
        f'\n<article class="gc">'
        f'<a href="{r["link"]}" target="_blank" rel="noopener noreferrer">'
        f'<img src="{r["image"]}" alt="{html_lib.escape(r["name"])}" '
        f'loading="lazy" width="180" height="180">'
        f'<div class="gi">'
        f'<h3>{html_lib.escape(r["name"])}</h3>'
        f'<p>{html_lib.escape(clean_desc)}</p>'
        f'</div>'
        f'</a></article>'
    )

# ── 3. Wrap in full standalone HTML ─────────────────────────────────────────
page = (
    '<!DOCTYPE html>\n'
    '<html lang="en">\n'
    '<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
    '<title>Car Games – Unblocked Games G+</title>\n'
    '<style>\n'
    '*{box-sizing:border-box;margin:0;padding:0}\n'
    'body{font-family:Arial,Helvetica,sans-serif;background:#f4f6fb;padding:14px}\n'
    'h1.cat{text-align:center;font-size:20px;font-weight:800;color:#1a237e;\n'
    '  text-transform:uppercase;letter-spacing:.6px;margin-bottom:16px}\n'
    '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(168px,1fr));gap:14px}\n'
    '.gc{background:#fff;border-radius:12px;overflow:hidden;\n'
    '  box-shadow:0 2px 8px rgba(0,0,0,.10);\n'
    '  transition:transform .18s,box-shadow .18s}\n'
    '.gc:hover{transform:translateY(-5px);box-shadow:0 8px 22px rgba(0,0,0,.18)}\n'
    '.gc a{display:block;text-decoration:none;color:inherit}\n'
    '.gc img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block}\n'
    '.gi{padding:8px 10px 12px}\n'
    '.gi h3{font-size:13px;font-weight:700;color:#1a237e;margin-bottom:5px;\n'
    '  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}\n'
    '.gi p{font-size:11px;color:#555;line-height:1.55;\n'
    '  display:-webkit-box;-webkit-line-clamp:4;\n'
    '  -webkit-box-orient:vertical;overflow:hidden}\n'
    '</style>\n'
    '</head>\n'
    '<body>\n'
    '<h1 class="cat">&#x1F697; Car Games</h1>\n'
    '<div class="grid">'
    + cards_html +
    '\n</div>\n'
    '</body>\n'
    '</html>\n'
)

OUT.write_text(page, encoding="utf-8")

size_kb = OUT.stat().st_size / 1024
limit_ok = "OK ✅" if size_kb < 100 else "OVER LIMIT ⚠️"
print(f"✓ {len(results)} car games  ({size_kb:.1f} KB / 100 KB limit → {limit_ok})")
print(f"  → {OUT}")
print()
print("How to embed in Google Sites:")
print("  Insert → Embed → 'Embed code' tab → paste full file content → Next → Insert")
print()
for i, r in enumerate(results, 1):
    print(f"  {i:>2}. {r['slug']:<45} {r['name']}")
