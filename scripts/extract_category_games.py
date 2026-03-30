#!/usr/bin/env python3
"""
extract_category_games.py
Generalized version of extract_car_games.py.
For each category listed in CATEGORIES, reads category/{cat}.html,
fetches English descriptions from game/{slug}.html, then writes:
  {cat}_games.csv              – slug, name, image, description, play_url, link
  {cat}_games_googlesite.html  – self-contained embed for Google Sites

Usage:
  python3 scripts/extract_category_games.py              # process all categories
  python3 scripts/extract_category_games.py clicker io   # process specific categories
"""
import re, csv, sys, html as html_lib
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────────────────
BASE        = Path(__file__).parent.parent
GAME_DIR    = BASE / "game"
SCRIPTS_DIR = Path(__file__).parent
IMG_PREFIX  = "https://unblocked-games-g-plus.poki2.online"
PLAY_PREFIX = "https://unblocked-games-g-plus.poki2.online/play"
LINK_PREFIX = "https://sites.google.com/view/unblocked-games-g-site"

CATEGORIES = [
    "clicker", "fighting", "io", "kids", "multiplayer",
    "new", "parkour", "platform", "puzzle", "racing",
    "running", "school", "shooting", "skill", "soccer",
    "stickman", "trending", "two-player",
]

CATEGORY_LABELS = {
    "clicker":    "🖱️ Clicker Games",
    "fighting":   "🥊 Fighting Games",
    "io":         "🌐 IO Games",
    "kids":       "🧒 Kids Games",
    "multiplayer":"👥 Multiplayer Games",
    "new":        "🆕 New Games",
    "parkour":    "🏃 Parkour Games",
    "platform":   "🕹️ Platform Games",
    "puzzle":     "🧩 Puzzle Games",
    "racing":     "🏎️ Racing Games",
    "running":    "👟 Running Games",
    "school":     "🏫 School Games",
    "shooting":   "🎯 Shooting Games",
    "skill":      "⭐ Skill Games",
    "soccer":     "⚽ Soccer Games",
    "stickman":   "🦯 Stickman Games",
    "trending":   "🔥 Trending Games",
    "two-player": "👫 Two Player Games",
}

RE_CARD      = re.compile(r'<a class="card" href="/game/([^"]+)">(.*?)</a>', re.DOTALL)
RE_IMG       = re.compile(r'src="([^"]+)"')
RE_NAME      = re.compile(r'<h3>(.*?)</h3>')
RE_DESC_DIV  = re.compile(r'class="description pb-2">\s*<h3[^>]*>.*?</h3>\s*<p>(.*?)</p>', re.DOTALL)
RE_META_DESC = re.compile(r'<meta\s+name="description"\s+content="([^"]+)"', re.I)

CSV_FIELDS = ["slug", "name", "image", "description", "play_url", "link"]


def extract(category: str) -> list[dict]:
    cat_file = BASE / "category" / f"{category}.html"
    if not cat_file.exists():
        print(f"  [SKIP] {cat_file} not found")
        return []

    cat_html = cat_file.read_text(encoding="utf-8")
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

    return results


def write_csv(results: list[dict], out_path: Path) -> None:
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(results)


def write_html(results: list[dict], category: str, out_path: Path) -> None:
    label = CATEGORY_LABELS.get(category, category.replace("-", " ").title() + " Games")

    cards_html = ""
    for r in results:
        clean_desc = " ".join(r["description"].split())
        cards_html += (
            f'\n<article class="gc">'
            f'<a href="{r["link"]}">'
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
        f'<title>{label} \u2013 Unblocked Games G+</title>\n'
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
        f'<h1 class="cat">{label}</h1>\n'
        '<div class="grid">'
        + cards_html +
        '\n</div>\n</body>\n</html>\n'
    )

    out_path.write_text(page, encoding="utf-8")


def process(category: str) -> None:
    print(f"\n[{category}]")
    results = extract(category)
    if not results:
        return

    out_csv  = SCRIPTS_DIR / f"{category}_games.csv"
    out_html = SCRIPTS_DIR / f"{category}_games_googlesite.html"

    write_csv(results, out_csv)
    write_html(results, category, out_html)

    csv_kb  = out_csv.stat().st_size  / 1024
    html_kb = out_html.stat().st_size / 1024
    limit   = "OK \u2705" if html_kb < 100 else "OVER LIMIT \u26a0\ufe0f"
    print(f"  {len(results)} games  |  CSV {csv_kb:.1f} KB  |  HTML {html_kb:.1f} KB / 100 KB {limit}")


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    targets = sys.argv[1:] if len(sys.argv) > 1 else CATEGORIES
    for cat in targets:
        process(cat)
    print("\nDone.")
