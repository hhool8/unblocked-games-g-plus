#!/usr/bin/env python3
"""
gen_play_pages.py
-----------------
Reads every game/*.html, extracts the REAL game iframe src, then generates
docs/play/{slug}.html — a self-contained page with:
  - AdSense placeholder (top + bottom)
  - Game iframe pointing directly to the working game URL
  - Title / meta / canonical / OG tags
  - Fullscreen button

These pages are the target embed for Google Sites:
  <iframe src="https://unblocked-games-g-plus.poki2.online/play/{slug}.html" ...></iframe>
"""

import re
import html as htmllib
from pathlib import Path

BASE     = Path(__file__).parent.parent
GAME_DIR = BASE / "game"
OUT_DIR  = BASE / "play"
SITE     = "https://unblocked-games-g-plus.poki2.online"
GITLAB   = "https://unblockedgames66.gitlab.io"

OUT_DIR.mkdir(parents=True, exist_ok=True)

RE_IFRAME = re.compile(r'<iframe[^>]+class="game-iframe"[^>]+src="([^"]+)"', re.I | re.S)
RE_TITLE  = re.compile(r'<title>([^<]+)</title>', re.I)
RE_DESC   = re.compile(r'<meta\s+name="description"\s+content="([^"]+)"', re.I)


def extract(raw):
    src   = RE_IFRAME.search(raw)
    title = RE_TITLE.search(raw)
    desc  = RE_DESC.search(raw)
    return (
        src.group(1).strip()    if src   else None,
        title.group(1).strip()  if title else "Unblocked Game",
        desc.group(1).strip()   if desc  else "",
    )


def make_page(slug, game_url, title, desc):
    safe_title = htmllib.escape(title)
    safe_desc  = htmllib.escape(desc)
    thumb      = f"{GITLAB}/assets/upload/66games/jpg/{slug}.jpg"
    orig       = f"{GITLAB}/game/{slug}.html"
    play_url   = htmllib.escape(game_url)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
<title>{safe_title}</title>
<meta name="description" content="{safe_desc}">
<link rel="canonical" href="{SITE}/game/{slug}.html">
<meta property="og:type" content="website">
<meta property="og:title" content="{safe_title}">
<meta property="og:description" content="{safe_desc}">
<meta property="og:image" content="{thumb}">
<meta property="og:url" content="{SITE}/game/{slug}.html">
<meta name="twitter:card" content="summary_large_image">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f0f1a;color:#e0e0e0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;display:flex;flex-direction:column;min-height:100vh}}
.ad-wrap{{width:100%;background:#111;display:flex;align-items:center;justify-content:center;padding:4px 0;min-height:90px}}
.ad-placeholder{{max-width:728px;width:100%;min-height:90px;background:#1a1a2e;border:1px dashed #333;display:flex;align-items:center;justify-content:center;color:#444;font-size:.72rem;letter-spacing:.05em}}
.bar{{display:flex;align-items:center;gap:.5rem;padding:.4rem .7rem;background:#1a1a2e;border-bottom:2px solid #e74c3c;flex-wrap:wrap;flex-shrink:0}}
.bar h1{{flex:1;color:#fff;font-size:.92rem;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}}
.btn-fs{{background:#e74c3c;border:none;color:#fff;padding:.28rem .8rem;border-radius:5px;cursor:pointer;font-size:.8rem;font-weight:700;white-space:nowrap}}
.btn-fs:hover{{background:#c0392b}}
.ext{{color:#aaa;font-size:.76rem;text-decoration:none;border:1px solid #444;padding:.26rem .6rem;border-radius:5px;white-space:nowrap}}
.ext:hover{{border-color:#e74c3c;color:#e74c3c}}
.game-wrap{{flex:1;position:relative;background:#000}}
.game-wrap iframe{{position:absolute;top:0;left:0;width:100%;height:100%;border:none;background:#000}}
</style>
</head>
<body>

<!-- ▼ AdSense Top — replace .ad-placeholder with your <ins> tag -->
<div class="ad-wrap">
  <div class="ad-placeholder" id="ad-top">ADVERTISEMENT</div>
</div>

<div class="bar">
  <h1>{safe_title}</h1>
  <button class="btn-fs" onclick="goFS()">&#9974; Fullscreen</button>
  <a class="ext" href="{orig}" target="_blank" rel="noopener">Open ↗</a>
</div>

<div class="game-wrap" id="gwrap">
  <iframe id="gf"
          src="{play_url}"
          allowfullscreen
          allow="fullscreen *; autoplay *; gamepad *"
          scrolling="no">
  </iframe>
</div>

<!-- ▼ AdSense Bottom — replace .ad-placeholder with your <ins> tag -->
<div class="ad-wrap">
  <div class="ad-placeholder" id="ad-bottom">ADVERTISEMENT</div>
</div>

<script>
(function(){{
  // Make game-wrap fill remaining viewport height
  function resize(){{
    var used = document.querySelector('.ad-wrap').offsetHeight * 2
              + document.querySelector('.bar').offsetHeight;
    document.getElementById('gwrap').style.height =
      Math.max(380, window.innerHeight - used) + 'px';
  }}
  resize();
  window.addEventListener('resize', resize);

  // Fullscreen
  window.goFS = function(){{
    var f = document.getElementById('gf');
    var fn = f.requestFullscreen || f.webkitRequestFullscreen || f.msRequestFullscreen;
    if (fn) fn.call(f);
  }};
}})();
</script>
</body>
</html>"""


def main():
    files = sorted(GAME_DIR.glob("*.html"))
    ok = skip = 0
    skipped = []

    for f in files:
        slug = f.stem
        raw  = f.read_text(encoding="utf-8", errors="ignore")
        game_url, title, desc = extract(raw)

        if not game_url:
            skipped.append(slug)
            skip += 1
            continue

        out = OUT_DIR / f"{slug}.html"
        out.write_text(make_page(slug, game_url, title, desc), encoding="utf-8")
        ok += 1

    print(f"✓ Generated {ok} play pages  →  docs/play/")
    if skipped:
        print(f"  Skipped {skip} (no game-iframe found):")
        for s in skipped:
            print(f"    - {s}")


if __name__ == "__main__":
    main()
