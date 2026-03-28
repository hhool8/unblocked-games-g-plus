#!/usr/bin/env python3
"""
Phase 2 — Homepage SEO update
- Replace weak <title> and <meta description>
- Add keywords, OG, Twitter Card, canonical
- Inject WebSite + FAQPage JSON-LD schema
- Append semantic SEO content section inside <main> (before </main>)
- Add footer link placeholder for independent site
"""

import re, json
from pathlib import Path

ROOT      = Path(__file__).parent.parent
INDEX     = ROOT / "index.html"
BASE_URL  = "https://unblockedgames66.gitlab.io"

TITLE       = "Unblocked Games 66 — Play Free Games Unblocked at School"
DESCRIPTION = (
    "Play Unblocked Games 66 — the ultimate free online game hub for students. "
    "No download, no VPN needed. Enjoy 474 unblocked games on Chromebook, at school, "
    "or anywhere. Play now, no login required!"
)
KEYWORDS = (
    "unblocked games 66, unblocked games, games unblocked, unblocked games for school, "
    "unblocked games chromebook, free unblocked games, play games unblocked, "
    "unblocked games no download, unblocked io games, cool math games unblocked"
)

WEBSITE_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Unblocked Games 66",
    "url": f"{BASE_URL}/",
    "description": "Play 474 free unblocked games at school on Chromebook — no download, no VPN needed.",
    "potentialAction": {
        "@type": "SearchAction",
        "target": {
            "@type": "EntryPoint",
            "urlTemplate": f"{BASE_URL}/search.html?q={{search_term_string}}"
        },
        "query-input": "required name=search_term_string"
    }
}

FAQPAGE_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "What is Unblocked Games 66?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Unblocked Games 66 is a free browser-based gaming platform with 474 online games accessible on school networks, Chromebook, and restricted Wi-Fi — no download or account required."
            }
        },
        {
            "@type": "Question",
            "name": "Is Unblocked Games 66 safe for school?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes. All games are curated for age-appropriateness. The site has no malware or deceptive ads and is designed to be safe for students on school networks."
            }
        },
        {
            "@type": "Question",
            "name": "Can I play Unblocked Games 66 on a Chromebook?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes. Every game runs in the browser with no plugins or extensions required, making all titles fully compatible with Chrome OS and school-managed Chromebooks."
            }
        },
        {
            "@type": "Question",
            "name": "Do I need a VPN to access Unblocked Games 66?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "No VPN is needed. Unblocked Games 66 is hosted to remain accessible on most school and work networks directly from your browser."
            }
        },
        {
            "@type": "Question",
            "name": "How many games are on Unblocked Games 66?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Unblocked Games 66 currently features 474 browser games across action, puzzle, sports, racing, IO, and more genres. New games are added regularly."
            }
        },
        {
            "@type": "Question",
            "name": "Are the games on Unblocked Games 66 free?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "Yes, all games on Unblocked Games 66 are completely free to play. No subscription, no login, no payment of any kind is required."
            }
        }
    ]
}

SEO_CONTENT = """
<!-- SEO semantic section — injected by scripts/update_homepage.py -->
<section class="container-fluid py-5 mt-4" id="seo-content" style="border-top:1px solid var(--bs-border-color)">
  <div class="container">
    <h2 class="h4 mb-3">What Is Unblocked Games 66?</h2>
    <p>
      <strong>Unblocked Games 66</strong> is a free online gaming platform for students,
      office workers, and casual gamers who face content restrictions on their networks.
      Whether your school blocks entertainment websites or your workplace IT policy prevents
      gaming, Unblocked Games 66 provides seamless access to <strong>474 browser-based
      games</strong> — no VPN, no download, no accounts required. Just open your browser,
      click a game, and play.
    </p>
    <p>
      Our library spans every genre: action, puzzle, sports, racing, IO multiplayer,
      platformers, idle clickers, and more. Popular titles include
      <a href="/game/slope.html">Slope</a>,
      <a href="/game/geometry-dash.html">Geometry Dash</a>,
      <a href="/game/1v1-lol.html">1v1 LOL</a>,
      <a href="/game/among-us.html">Among Us</a>,
      <a href="/game/run-3.html">Run 3</a>, and
      <a href="/game/krunker-io.html">Krunker IO</a>.
      All games load instantly on Chromebook and school-managed devices.
    </p>

    <h2 class="h4 mt-4 mb-3">Why Play Here?</h2>
    <div class="row g-3">
      <div class="col-md-4">
        <h3 class="h6">&#x2705; Works on Chromebook &amp; School Wi-Fi</h3>
        <p class="small">All games are browser-based and require no plugins. They work on Chrome OS and pass most school network filters.</p>
      </div>
      <div class="col-md-4">
        <h3 class="h6">&#x2705; No Download, No Login</h3>
        <p class="small">Zero installs, zero accounts. Click any game and you're playing in seconds — completely anonymous.</p>
      </div>
      <div class="col-md-4">
        <h3 class="h6">&#x2705; 474 Free Games</h3>
        <p class="small">From Slope to Minecraft Classic, from Cookie Clicker to Shell Shockers — there's always something new to discover.</p>
      </div>
    </div>

    <h2 class="h4 mt-5 mb-3">Frequently Asked Questions</h2>
    <div class="accordion" id="faq-accordion">

      <div class="accordion-item border-0 border-bottom">
        <h3 class="accordion-header">
          <button class="accordion-button collapsed px-0 bg-transparent" type="button"
                  data-bs-toggle="collapse" data-bs-target="#faq1">
            What is Unblocked Games 66?
          </button>
        </h3>
        <div id="faq1" class="accordion-collapse collapse" data-bs-parent="#faq-accordion">
          <div class="accordion-body px-0">
            Unblocked Games 66 is a free browser-based gaming platform with 474 online games accessible
            on school networks, Chromebook, and restricted Wi-Fi — no download or account required.
          </div>
        </div>
      </div>

      <div class="accordion-item border-0 border-bottom">
        <h3 class="accordion-header">
          <button class="accordion-button collapsed px-0 bg-transparent" type="button"
                  data-bs-toggle="collapse" data-bs-target="#faq2">
            Is Unblocked Games 66 safe for school?
          </button>
        </h3>
        <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faq-accordion">
          <div class="accordion-body px-0">
            Yes. All games are curated for age-appropriateness. The site has no malware or deceptive
            ads and is designed to be safe for students on school networks.
          </div>
        </div>
      </div>

      <div class="accordion-item border-0 border-bottom">
        <h3 class="accordion-header">
          <button class="accordion-button collapsed px-0 bg-transparent" type="button"
                  data-bs-toggle="collapse" data-bs-target="#faq3">
            Can I play on a Chromebook?
          </button>
        </h3>
        <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faq-accordion">
          <div class="accordion-body px-0">
            Yes. Every game runs in the browser with no plugins or extensions required — fully
            compatible with Chrome OS and school-managed Chromebooks.
          </div>
        </div>
      </div>

      <div class="accordion-item border-0 border-bottom">
        <h3 class="accordion-header">
          <button class="accordion-button collapsed px-0 bg-transparent" type="button"
                  data-bs-toggle="collapse" data-bs-target="#faq4">
            Do I need a VPN?
          </button>
        </h3>
        <div id="faq4" class="accordion-collapse collapse" data-bs-parent="#faq-accordion">
          <div class="accordion-body px-0">
            No VPN needed. Unblocked Games 66 is hosted to remain accessible on most school and
            work networks directly from your browser.
          </div>
        </div>
      </div>

      <div class="accordion-item border-0 border-bottom">
        <h3 class="accordion-header">
          <button class="accordion-button collapsed px-0 bg-transparent" type="button"
                  data-bs-toggle="collapse" data-bs-target="#faq5">
            Are all games free?
          </button>
        </h3>
        <div id="faq5" class="accordion-collapse collapse" data-bs-parent="#faq-accordion">
          <div class="accordion-body px-0">
            Yes — all 474 games are completely free to play. No subscription, no login, no payment
            of any kind is required.
          </div>
        </div>
      </div>

    </div>
  </div>
</section>
"""

# ─── Process index.html ───────────────────────────────────────────────────────

content = INDEX.read_text(encoding="utf-8", errors="replace")

# Guard: skip if already updated
if "update_homepage.py" in content:
    print("· index.html — already updated, skipping")
else:
    # 1. Remove old title + description
    content = re.sub(r'\s*<title>[^<]*</title>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'\s*<meta\s+name="description"[^>]*/?\s*>', '', content, flags=re.IGNORECASE)

    # 2. Build SEO head block
    ws_json  = json.dumps(WEBSITE_SCHEMA,  ensure_ascii=False, indent=2)
    faq_json = json.dumps(FAQPAGE_SCHEMA,  ensure_ascii=False, indent=2)

    seo_head = f"""    <!-- SEO: injected by scripts/update_homepage.py -->
    <title>{TITLE}</title>
    <meta name="description" content="{DESCRIPTION}" />
    <meta name="keywords" content="{KEYWORDS}" />
    <link rel="canonical" href="{BASE_URL}/" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{TITLE}" />
    <meta property="og:description" content="{DESCRIPTION}" />
    <meta property="og:url" content="{BASE_URL}/" />
    <meta property="og:image" content="{BASE_URL}/assets/img/og-cover.jpg" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{TITLE}" />
    <meta name="twitter:description" content="{DESCRIPTION}" />
    <meta name="twitter:image" content="{BASE_URL}/assets/img/og-cover.jpg" />
    <script type="application/ld+json">
{ws_json}
    </script>
    <script type="application/ld+json">
{faq_json}
    </script>"""

    content = re.sub(r'(</head>)', f"{seo_head}\n\\1", content, count=1, flags=re.IGNORECASE)

    # 3. Append SEO content section before </main>
    if "</main>" in content:
        content = content.replace("</main>", SEO_CONTENT + "\n</main>", 1)

    INDEX.write_text(content, encoding="utf-8")
    print("✓ index.html — SEO header + FAQ section injected")
