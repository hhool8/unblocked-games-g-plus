#!/usr/bin/env python3
"""
gen_gsite_full.py
生成 Google Sites 建站用完整数据 CSV：
  slug, page_name, embed_url, thumbnail, description, game_url
"""
import re, csv
from pathlib import Path

BASE     = Path(__file__).parent.parent
GAME_DIR = BASE / "game"
PLAY     = "https://ug66.poki2.online/play"
GITLAB   = "https://unblockedgames66.gitlab.io"

RE_TITLE = re.compile(r'<title>([^<|]+)', re.I)
RE_CAT   = re.compile(r'"genre"\s*:\s*\[\s*"([^"]+)"', re.I)
RE_DESC  = re.compile(r'<meta\s+name="description"\s+content="([^"]+)"', re.I)

# 简介末尾统一附加语
SUFFIX = "— play free unblocked online, no download needed."

rows = []
for f in sorted(GAME_DIR.glob("*.html")):
    slug = f.stem
    raw  = f.read_text(errors="ignore")

    m_t = RE_TITLE.search(raw)
    m_c = RE_CAT.search(raw)
    m_d = RE_DESC.search(raw)

    raw_title = m_t.group(1).strip() if m_t else slug
    # 页面名：取第一段（" - " 或 " — " 之前），去掉末尾 " Unblocked"
    page_name = re.split(r'\s[—-]\s', raw_title)[0].strip()
    page_name = re.sub(r'\s+Unblocked$', '', page_name, flags=re.I).strip()
    category  = m_c.group(1).title() if m_c else "Games"
    # 简介：优先用 meta description，否则自动生成
    if m_d:
        raw_desc = m_d.group(1).strip()
        # 去掉已有的 "play free..." 后缀避免重复
        desc = re.sub(r'[—-]?\s*play\s+free.*$', '', raw_desc, flags=re.I).strip()
        description = f"Play {page_name} unblocked {SUFFIX}"
    else:
        description = f"Play {page_name} unblocked {SUFFIX}"

    embed_url = f"{PLAY}/{slug}.html"
    thumbnail = f"{GITLAB}/assets/upload/66games/jpg/{slug}.jpg"
    game_url  = f"{GITLAB}/{slug}/"

    rows.append({
        "slug":        slug,
        "page_name":   page_name,
        "embed_url":   embed_url,
        "thumbnail":   thumbnail,
        "description": description,
        "category":    category,
        "game_url":    game_url,
    })

out = BASE / "scripts" / "gsite_full.csv"
fields = ["slug", "page_name", "embed_url", "thumbnail", "description", "category", "game_url"]
with open(out, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)

print(f"✓ {len(rows)} 个游戏 → {out}")
print()
print(f"{'slug':<40} {'page_name':<30} {'category':<18}")
print("-" * 92)
for r in rows[:30]:
    print(f"{r['slug']:<40} {r['page_name']:<30} {r['category']:<18}")
if len(rows) > 30:
    print(f"  ... 还有 {len(rows)-30} 行")
