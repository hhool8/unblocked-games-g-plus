#!/usr/bin/env python3
"""
Phase 1 — Batch SEO injection for all 474 game pages
Injects into each game/XXX.html:
  - <title>  {Title} Unblocked — Play Free Online | Unblocked Games G+
  - <meta description>
  - <meta keywords>
  - Open Graph tags
  - <link rel="canonical">
  - JSON-LD VideoGame schema
  - img alt attributes on thumbnail images
  - loading="lazy" on game iframes
  - <!-- FUTURE_CANONICAL --> comment for independent-site migration
"""

import os, re, json, html
from pathlib import Path

ROOT     = Path(__file__).parent.parent
GAME_DIR = ROOT / "game"
BASE_URL = "https://unblockedgames66.gitlab.io"
IND_DOMAIN_PLACEHOLDER = "INDEPENDENT_DOMAIN"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def title_case(slug: str) -> str:
    """Convert 'krunker-io' → 'Krunker Io', then clean common suffixes."""
    words = slug.replace("-", " ").title()
    # Minor display fixes
    words = re.sub(r'\bIo\b', 'IO', words)
    words = re.sub(r'\b3d\b', '3D', words, flags=re.IGNORECASE)
    words = re.sub(r'\b2d\b', '2D', words, flags=re.IGNORECASE)
    return words


def extract_title(content: str, slug: str) -> str:
    """Extract game title from <h1 class="h4"><strong>TITLE</strong></h1>."""
    m = re.search(r'<h1[^>]*class="h4"[^>]*>\s*<strong>(.*?)</strong>', content, re.IGNORECASE | re.DOTALL)
    if m:
        return html.unescape(m.group(1).strip())
    return title_case(slug)


def extract_genres(content: str) -> list:
    """Extract categories from <div class="card-category"><a ...>GENRE</a></div>."""
    genres = re.findall(
        r'<div[^>]*class="card-category"[^>]*>\s*<a[^>]*>(.*?)</a>',
        content, re.IGNORECASE | re.DOTALL
    )
    cleaned = []
    for g in genres:
        g = html.unescape(re.sub(r'<[^>]+>', '', g)).strip()
        if g:
            cleaned.append(g)
    return cleaned or ["Browser Game"]


def already_injected(content: str) -> bool:
    return "FUTURE_CANONICAL" in content or '"@type": "VideoGame"' in content


def build_seo_block(slug: str, title: str, genres: list) -> str:
    """Build the full SEO <head> block to insert before </head>."""
    page_url   = f"{BASE_URL}/game/{slug}.html"
    thumb_url  = f"{BASE_URL}/assets/upload/66games/jpg/{slug}.jpg"
    future_url = f"https://{IND_DOMAIN_PLACEHOLDER}/game/{slug}/"

    title_tag  = f"{title} Unblocked — Play Free Online | Unblocked Games G+"
    desc_tag   = (
        f"Play {title} unblocked for free on Unblocked Games G+. "
        "No download, no login required. Works on school Chromebook and restricted networks."
    )
    genre_csv  = ", ".join(genres)

    schema = {
        "@context": "https://schema.org",
        "@type": "VideoGame",
        "name": f"{title} Unblocked",
        "description": desc_tag,
        "url": page_url,
        "image": thumb_url,
        "genre": genres,
        "gamePlatform": ["Web Browser", "Chrome OS"],
        "applicationCategory": "Game",
        "operatingSystem": "Any",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "author": {
            "@type": "Organization",
            "name": "Unblocked Games G+"
        }
    }
    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)

    block = f"""    <!-- SEO: injected by scripts/seo_inject_games.py -->
    <!-- FUTURE_CANONICAL: {future_url} -->
    <title>{html.escape(title_tag)}</title>
    <meta name="description" content="{html.escape(desc_tag)}" />
    <meta name="keywords" content="{html.escape(title)} unblocked, {html.escape(title.lower())} unblocked, Unblocked Games G+, free unblocked games, {html.escape(genre_csv.lower())}" />
    <link rel="canonical" href="{page_url}" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{html.escape(title_tag)}" />
    <meta property="og:description" content="{html.escape(desc_tag)}" />
    <meta property="og:url" content="{page_url}" />
    <meta property="og:image" content="{thumb_url}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{html.escape(title_tag)}" />
    <meta name="twitter:description" content="{html.escape(desc_tag)}" />
    <meta name="twitter:image" content="{thumb_url}" />
    <script type="application/ld+json">
{schema_json}
    </script>"""
    return block


def inject_img_alt(content: str, title: str, slug: str) -> str:
    """Add alt attribute only to the main game thumbnail img (by slug in src), not sidebar cards."""
    alt_text = f"{title} unblocked game"

    # Only target the img whose src contains this game's slug (the hero thumbnail)
    pattern = re.compile(
        r'(<img\s[^>]*src="[^"]*' + re.escape(slug) + r'[^"]*"[^>]*>)',
        re.IGNORECASE
    )

    def add_alt(m):
        tag = m.group(1)
        if 'alt=' in tag:
            return tag
        return re.sub(r'(\s*/?>)', f' alt="{html.escape(alt_text)}"\\1', tag, count=1)

    return pattern.sub(add_alt, content, count=1)


def inject_iframe_lazy(content: str) -> str:
    """Add loading="lazy" to the main game iframe (class="game-iframe")."""
    def add_lazy(m):
        tag = m.group(0)
        if 'loading=' in tag:
            return tag
        return re.sub(r'(<iframe)', r'\1 loading="lazy"', tag, count=1)

    return re.sub(
        r'<iframe[^>]*class="game-iframe"[^>]*>',
        add_lazy,
        content,
        flags=re.IGNORECASE
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_file(path: Path) -> bool:
    slug    = path.stem
    content = path.read_text(encoding="utf-8", errors="replace")

    if already_injected(content):
        return False  # skip already-processed

    title  = extract_title(content, slug)
    genres = extract_genres(content)

    # 1. Remove old weak <title> and <meta description>
    content = re.sub(r'\s*<title>[^<]*</title>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*<meta\s+name="description"[^>]*/?\s*>', '', content, flags=re.IGNORECASE)

    # 2. Build and inject SEO block before </head>
    seo_block = build_seo_block(slug, title, genres)
    content = re.sub(r'(</head>)', f"{seo_block}\n\\1", content, count=1, flags=re.IGNORECASE)

    # 3. img alt (only on this game's hero thumbnail)
    content = inject_img_alt(content, title, slug)

    # 4. iframe loading=lazy
    content = inject_iframe_lazy(content)

    path.write_text(content, encoding="utf-8")
    return True


def main():
    files   = sorted(GAME_DIR.glob("*.html"))
    updated = 0
    skipped = 0
    for f in files:
        if process_file(f):
            updated += 1
        else:
            skipped += 1

    print(f"✓ seo_inject_games — {updated} files updated, {skipped} skipped (already injected)")


if __name__ == "__main__":
    main()
