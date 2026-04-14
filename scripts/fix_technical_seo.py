#!/usr/bin/env python3
"""
Phase 4 — Technical SEO fix
1. Fix robots.txt: add Sitemap directive
2. Fix sitemaps.xml: relative → absolute URLs, add homepage + category pages
3. Output sitemap.xml (canonical name) alongside sitemaps.xml
"""

import os, re
from pathlib import Path

ROOT = Path(__file__).parent.parent
BASE_URL = "https://unblocked-games-g-plus.poki2.online"

# ─── 1. robots.txt ────────────────────────────────────────────────────────────
robots_path = ROOT / "robots.txt"
robots_txt = robots_path.read_text(encoding="utf-8")

sitemap_line = f"Sitemap: {BASE_URL}/sitemap.xml"
if "Sitemap:" not in robots_txt:
    robots_txt = robots_txt.rstrip() + f"\n{sitemap_line}\n"
    robots_path.write_text(robots_txt, encoding="utf-8")
    print("✓ robots.txt — Sitemap directive added")
else:
    print("· robots.txt — Sitemap already present, skipping")

# ─── 2. Collect all URLs ──────────────────────────────────────────────────────
urls = []

# Homepage
urls.append({"loc": f"{BASE_URL}/", "priority": "1.0", "changefreq": "daily"})

# Category pages
cat_dir = ROOT / "category"
if cat_dir.exists():
    for f in sorted(cat_dir.glob("*.html")):
        urls.append({
            "loc": f"{BASE_URL}/category/{f.name}",
            "priority": "0.7",
            "changefreq": "weekly",
        })

# Game pages
game_dir = ROOT / "game"
if game_dir.exists():
    for f in sorted(game_dir.glob("*.html")):
        urls.append({
            "loc": f"{BASE_URL}/game/{f.name}",
            "priority": "0.8",
            "changefreq": "monthly",
        })

# Static pages
for page in ["privacy/index.html", "terms/index.html", "contact/index.html"]:
    p = ROOT / page
    if p.exists():
        urls.append({
            "loc": f"{BASE_URL}/{page}",
            "priority": "0.5",
            "changefreq": "yearly",
        })

# ─── 3. Build sitemap XML ─────────────────────────────────────────────────────
lastmod = "2026-03-28"
lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
for u in urls:
    lines.append("  <url>")
    lines.append(f"    <loc>{u['loc']}</loc>")
    lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines.append(f"    <changefreq>{u['changefreq']}</changefreq>")
    lines.append(f"    <priority>{u['priority']}</priority>")
    lines.append("  </url>")
lines.append("</urlset>")
sitemap_xml = "\n".join(lines) + "\n"

# Write both names
(ROOT / "sitemap.xml").write_text(sitemap_xml, encoding="utf-8")
(ROOT / "sitemaps.xml").write_text(sitemap_xml, encoding="utf-8")
print(f"✓ sitemap.xml + sitemaps.xml — {len(urls)} URLs written (absolute paths)")
