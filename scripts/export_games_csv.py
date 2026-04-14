#!/usr/bin/env python3
"""
export_games_csv.py
Extract game data from 474 HTML files → games_for_gsite.csv
Columns: Title, Category, Slug, Page URL, Thumbnail URL, Description, Play Now URL
Used to populate Google Sheets → Awesome Table embed in Google Sites.
"""

import csv
import re
from pathlib import Path

BASE = Path(__file__).parent.parent
GAME_DIR = BASE / "game"
OUT = BASE / "scripts" / "games_for_gsite.csv"
BASE_URL = "https://unblocked-games-g-plus.poki2.online"

def extract(html: str, slug: str) -> dict:
    # Title: from og:title (already injected) or h1
    m = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    title = m.group(1).replace(" Unblocked — Play Free Online | Unblocked Games G+", "").strip() if m else slug.replace("-", " ").title()

    # Category
    m = re.search(r'<div class="card-category"><a [^>]+>([^<]+)</a>', html)
    category = m.group(1).strip().title() if m else ""

    # Thumbnail
    m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    thumbnail = m.group(1) if m else ""

    # Description
    m = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    desc = m.group(1) if m else ""

    page_url = f"{BASE_URL}/game/{slug}.html"

    return {
        "Title": title,
        "Category": category,
        "Slug": slug,
        "Page URL": page_url,
        "Thumbnail URL": thumbnail,
        "Description": desc,
        "Play Now": page_url,
    }

def main():
    files = sorted(GAME_DIR.glob("*.html"))
    rows = []
    for f in files:
        slug = f.stem
        try:
            html = f.read_text(encoding="utf-8", errors="ignore")
            rows.append(extract(html, slug))
        except Exception as e:
            print(f"  SKIP {slug}: {e}")

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["Title", "Category", "Slug", "Page URL", "Thumbnail URL", "Description", "Play Now"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Exported {len(rows)} games → {OUT}")

if __name__ == "__main__":
    main()
