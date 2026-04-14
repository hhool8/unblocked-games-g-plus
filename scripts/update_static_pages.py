#!/usr/bin/env python3
"""
Phase 3 — Static pages SEO update
Operates on: privacy/index.html, terms/index.html, contact/index.html
- Replace weak <title> and <meta description>
- Inject canonical, OG tags
- Refresh existing injected tags so the main domain is used consistently
"""

import re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
BASE_URL = "https://unblocked-games-g-plus.poki2.online"

PAGES = [
    {
        "path": ROOT / "privacy" / "index.html",
        "title": "Privacy Policy — Unblocked Games G+",
        "description": (
            "Read the Privacy Policy for Unblocked Games G+. Learn how we collect, use, "
            "and protect your data when you visit our free unblocked games site."
        ),
        "canonical": f"{BASE_URL}/privacy/",
        "h1_fix": None,   # existing H1 is fine
    },
    {
        "path": ROOT / "terms" / "index.html",
        "title": "Terms and Conditions — Unblocked Games G+",
        "description": (
            "Review the Terms and Conditions for using Unblocked Games G+. "
            "By accessing our site you agree to these terms governing free browser-based gaming."
        ),
        "canonical": f"{BASE_URL}/terms/",
        "h1_fix": None,
    },
    {
        "path": ROOT / "contact" / "index.html",
        "title": "Contact Us — Unblocked Games G+",
        "description": (
            "Get in touch with Unblocked Games G+. Submit a game request, report an issue, "
            "or send us feedback — we'd love to hear from you."
        ),
        "canonical": f"{BASE_URL}/contact/",
        "h1_fix": None,
    },
]


def process_page(cfg: dict):
    path = cfg["path"]
    if not path.exists():
        print(f"  ⚠ {path} not found — skipping")
        return

    content = path.read_text(encoding="utf-8", errors="replace")

    content = re.sub(
        r'\s*<!-- SEO: injected by scripts/update_static_pages\.py -->.*?<meta property="og:url" content="[^"]+" />\n?',
        '',
        content,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # 1. Remove old title + description
    content = re.sub(r'\s*<title>[^<]*</title>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*<meta\s+name="description"[^>]*/?\s*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*<link\s+rel="canonical"[^>]*/?\s*>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*<meta\s+property="og:[^"]+"[^>]*/?\s*>', '', content, flags=re.IGNORECASE)

    # 2. Build SEO head block
    seo_head = (
        f'    <!-- SEO: injected by scripts/update_static_pages.py -->\n'
        f'    <title>{cfg["title"]}</title>\n'
        f'    <meta name="description" content="{cfg["description"]}" />\n'
        f'    <link rel="canonical" href="{cfg["canonical"]}" />\n'
        f'    <meta property="og:type" content="website" />\n'
        f'    <meta property="og:title" content="{cfg["title"]}" />\n'
        f'    <meta property="og:description" content="{cfg["description"]}" />\n'
        f'    <meta property="og:url" content="{cfg["canonical"]}" />\n'
    )

    content = re.sub(r'(</head>)', f"{seo_head}\\1", content, count=1, flags=re.IGNORECASE)

    # 3. Fix wrong domain references left over from template copy-paste
    content = content.replace("76GAMES.io", "Unblocked Games G+")
    content = content.replace("in 76GAMES.io", "on Unblocked Games G+")

    path.write_text(content, encoding="utf-8")
    print(f"  ✓ {path.parent.name}/index.html — SEO header injected")


def main():
    print("Phase 3 — Static pages SEO refresh")
    for cfg in PAGES:
        process_page(cfg)


if __name__ == "__main__":
    main()
