#!/usr/bin/env python3
"""
gen_directory.py
Generate docs/index.html — a static game directory page hosted on GitHub Pages.
474 game cards linking to unblockedgames66.gitlab.io (cross-domain external links).
"""

import csv
import html as htmllib
from pathlib import Path

BASE = Path(__file__).parent.parent
CSV = BASE / "scripts" / "games_for_gsite.csv"
OUT = BASE / "docs" / "index.html"
OUT.parent.mkdir(exist_ok=True)

GSITE_URL = "https://unblockedgames66.gitlab.io"

CATEGORY_COLORS = {
    "66-Ez Games":     "#e74c3c",
    "Io Games":        "#3498db",
    "Shooting Games":  "#e67e22",
    "Clicker Games":   "#9b59b6",
    "Parkour Games":   "#27ae60",
    "Platform Games":  "#16a085",
    "Two-Player Games":"#c0392b",
    "Online Games":    "#2980b9",
    "Free Games":      "#7f8c8d",
}

def cat_color(cat):
    return CATEGORY_COLORS.get(cat, "#555")

def build(rows):
    categories = sorted(set(r["Category"] for r in rows))

    # --- card HTML ---
    cards = []
    for r in rows:
        title   = htmllib.escape(r["Title"].title())
        cat     = htmllib.escape(r["Category"])
        thumb   = htmllib.escape(r["Thumbnail URL"])
        url     = htmllib.escape(r["Page URL"])
        desc    = htmllib.escape(r["Description"][:120]) + "…"
        color   = cat_color(r["Category"])
        slug    = r["Slug"]
        cards.append(f'''\
  <a class="card" href="{url}" target="_blank" rel="noopener" data-cat="{cat}">
    <img src="{thumb}" alt="{title} unblocked" loading="lazy" width="200" height="130"
         onerror="this.src='https://placehold.co/200x130/1a1a2e/fff?text=Game'">
    <div class="info">
      <span class="badge" style="background:{color}">{cat}</span>
      <h2>{title}</h2>
      <p>{desc}</p>
    </div>
  </a>''')

    # --- filter buttons ---
    btns = ['<button class="filter active" data-filter="all">All (474)</button>']
    for cat in categories:
        count = sum(1 for r in rows if r["Category"] == cat)
        safe = htmllib.escape(cat)
        btns.append(f'<button class="filter" data-filter="{safe}">{safe} ({count})</button>')

    return "\n".join(cards), "\n".join(btns)

def main():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    cards_html, btns_html = build(rows)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>474 Unblocked Games — Free Online Game Directory | Unblocked Games G+</title>
<meta name="description" content="Browse 474 free unblocked games playable at school or work. No download needed — instant play on Chromebook and restricted networks.">
<meta name="keywords" content="unblocked games, free online games, games at school, Unblocked Games G+, play free games">
<link rel="canonical" href="https://unblocked-games-g-plus.poki2.online/docs/">
<meta property="og:type" content="website">
<meta property="og:title" content="474 Unblocked Games — Free Online Game Directory">
<meta property="og:description" content="Browse 474 free unblocked games. Instant play, no login required.">
<meta property="og:url" content="https://unblocked-games-g-plus.poki2.online/docs/">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Unblocked Games G+ — Free Online Game Directory",
  "description": "474 free unblocked games playable at school or work on any device.",
  "url": "https://unblocked-games-g-plus.poki2.online/docs/",
  "publisher": {{
    "@type": "Organization",
    "name": "Unblocked Games G+",
    "url": "{GSITE_URL}"
  }}
}}
</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0f0f1a;color:#e0e0e0;min-height:100vh}}
header{{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);padding:2rem 1rem;text-align:center;border-bottom:2px solid #e74c3c}}
header h1{{font-size:clamp(1.5rem,4vw,2.5rem);color:#fff;margin-bottom:.5rem}}
header p{{color:#aaa;max-width:600px;margin:0 auto}}
.filters{{display:flex;flex-wrap:wrap;gap:.5rem;padding:1rem;max-width:1400px;margin:0 auto}}
.filter{{padding:.4rem .9rem;border:1px solid #444;border-radius:20px;background:transparent;color:#ccc;cursor:pointer;font-size:.85rem;transition:all .2s}}
.filter:hover,.filter.active{{background:#e74c3c;border-color:#e74c3c;color:#fff}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem;padding:1rem;max-width:1400px;margin:0 auto}}
.card{{background:#1a1a2e;border-radius:10px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .2s,box-shadow .2s;display:flex;flex-direction:column}}
.card:hover{{transform:translateY(-4px);box-shadow:0 8px 24px rgba(231,76,60,.3)}}
.card img{{width:100%;height:130px;object-fit:cover;background:#111}}
.info{{padding:.75rem;flex:1;display:flex;flex-direction:column;gap:.35rem}}
.badge{{font-size:.7rem;padding:.2rem .55rem;border-radius:12px;color:#fff;width:fit-content}}
.info h2{{font-size:.9rem;font-weight:600;color:#fff;line-height:1.3}}
.info p{{font-size:.75rem;color:#999;line-height:1.4;flex:1}}
.hidden{{display:none!important}}
footer{{text-align:center;padding:2rem;color:#666;font-size:.8rem;border-top:1px solid #222;margin-top:2rem}}
footer a{{color:#e74c3c;text-decoration:none}}
/* ── In-page game player ── */
#player{{display:none;position:fixed;inset:0;z-index:9999;background:#000;flex-direction:column}}
#player.open{{display:flex}}
#player-bar{{display:flex;align-items:center;gap:.75rem;padding:.5rem .75rem;background:#1a1a2e;border-bottom:2px solid #e74c3c;min-height:44px;flex-shrink:0}}
#player-back{{background:#e74c3c;border:none;color:#fff;padding:.35rem .9rem;border-radius:6px;cursor:pointer;font-size:.85rem;font-weight:600;white-space:nowrap}}
#player-back:hover{{background:#c0392b}}
#player-title{{color:#fff;font-weight:600;font-size:.95rem;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
#player-ext{{color:#aaa;font-size:.8rem;text-decoration:none;border:1px solid #444;padding:.3rem .7rem;border-radius:6px;white-space:nowrap}}
#player-ext:hover{{border-color:#e74c3c;color:#e74c3c}}
#player-frame{{flex:1;width:100%;border:none;background:#000}}
#player-blocked{{display:none;flex:1;align-items:center;justify-content:center;flex-direction:column;gap:1rem;background:#0f0f1a}}
#player-blocked p{{color:#aaa;font-size:.95rem}}
#player-blocked a{{background:#e74c3c;color:#fff;padding:.6rem 1.4rem;border-radius:8px;text-decoration:none;font-weight:600}}
</style>
</head>
<body>
<!-- In-page game player overlay -->
<div id="player">
  <div id="player-bar">
    <button id="player-back">&#8592; Back</button>
    <span id="player-title"></span>
    <a id="player-ext" href="#" target="_blank" rel="noopener">Open tab ↗</a>
  </div>
  <iframe id="player-frame" allowfullscreen allow="fullscreen *; autoplay *"></iframe>
  <div id="player-blocked">
    <p>This game can't be embedded — open it directly:</p>
    <a id="player-blocked-link" href="#" target="_blank" rel="noopener">Play Now ↗</a>
  </div>
</div>
<header>
  <h1>🎮 Unblocked Games G+</h1>
  <p>474 free games — play instantly at school, work, or anywhere. No download, no login.</p>
</header>
<div class="filters">
{btns_html}
</div>
<div class="grid" id="grid">
{cards_html}
</div>
<footer>
  <p>Game directory linking to <a href="{GSITE_URL}" target="_blank" rel="noopener">unblockedgames66.gitlab.io</a> — © 2026 Unblocked Games G+</p>
</footer>
<script>
// ── Category filter ──
const btns = document.querySelectorAll('.filter');
const cards = document.querySelectorAll('.card');
btns.forEach(btn => btn.addEventListener('click', () => {{
  btns.forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const f = btn.dataset.filter;
  cards.forEach(c => c.classList.toggle('hidden', f !== 'all' && c.dataset.cat !== f));
}}));

// ── In-page player ──
const player      = document.getElementById('player');
const pFrame      = document.getElementById('player-frame');
const pTitle      = document.getElementById('player-title');
const pExt        = document.getElementById('player-ext');
const pBlocked    = document.getElementById('player-blocked');
const pBlockedLnk = document.getElementById('player-blocked-link');

function openGame(url, title) {{
  pTitle.textContent = title;
  pExt.href = url;
  pBlockedLnk.href = url;
  pFrame.style.display = 'block';
  pBlocked.style.display = 'none';
  pFrame.src = '';
  player.classList.add('open');
  document.body.style.overflow = 'hidden';
  // Detect X-Frame-Options block: if frame doesn't load within 5s → show fallback
  const timer = setTimeout(() => {{
    try {{
      // If contentDocument is null cross-origin load failed visibly
      if (!pFrame.contentWindow || !pFrame.contentWindow.location.href) throw new Error();
    }} catch(e) {{}}
  }}, 500);
  pFrame.onload = () => {{ clearTimeout(timer); }};
  pFrame.onerror = () => {{
    pFrame.style.display = 'none';
    pBlocked.style.display = 'flex';
  }};
  // Small delay so overlay renders first
  setTimeout(() => {{ pFrame.src = url; }}, 50);
}}

function closeGame() {{
  pFrame.src = '';
  player.classList.remove('open');
  document.body.style.overflow = '';
}}

document.getElementById('player-back').addEventListener('click', closeGame);
document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closeGame(); }});

// Intercept all card clicks
cards.forEach(card => {{
  card.addEventListener('click', e => {{
    e.preventDefault();
    openGame(card.href, card.querySelector('h2').textContent);
  }});
}});
</script>
</body>
</html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"✓ Generated {OUT} ({len(rows)} games, {OUT.stat().st_size//1024}KB)")

if __name__ == "__main__":
    main()
