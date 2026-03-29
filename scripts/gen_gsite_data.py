#!/usr/bin/env python3
"""
gen_gsite_data.py
Outputs scripts/gsite_games.csv with slug, title, category, thumbnail, play_url
for building the Google Sites game pages.
"""
import re, csv
from pathlib import Path

BASE      = Path(__file__).parent.parent
GAME_DIR  = BASE / "game"
PLAY      = "https://ug66.poki2.online/play"
GITLAB    = "https://unblockedgames66.gitlab.io"
SITE_BASE = "https://sites.google.com/view/unblockedgames66ug66"

RE_TITLE = re.compile(r'<title>([^<|]+)', re.I)
RE_CAT   = re.compile(r'"genre"\s*:\s*\[\s*"([^"]+)"', re.I)

rows = []
for f in sorted(GAME_DIR.glob("*.html")):
    slug  = f.stem
    raw   = f.read_text(errors="ignore")
    m_t   = RE_TITLE.search(raw)
    m_c   = RE_CAT.search(raw)
    title = m_t.group(1).split(" - ")[0].strip() if m_t else slug
    cat   = m_c.group(1) if m_c else "Other"
    thumb = f"{GITLAB}/assets/upload/66games/jpg/{slug}.jpg"
    play  = f"{PLAY}/{slug}.html"
    gsite = f"{SITE_BASE}/{slug}"
    rows.append((slug, title, cat, thumb, play, gsite))

out = BASE / "scripts" / "gsite_games.csv"
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["slug", "title", "category", "thumbnail", "play_url", "gsite_url"])
    w.writerows(rows)

print(f"✓ {len(rows)} games → {out}")
for r in rows[:20]:
    print(f"  {r[1][:32]:<32} | {r[2][:18]:<18} | {r[4]}")
