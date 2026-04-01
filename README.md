# Unblocked Games G+

> **Live site:** [https://unblocked-games-g-plus.poki2.online](https://unblocked-games-g-plus.poki2.online)  
> **Repository:** [github.com/hhool8/unblocked-games-g-plus](https://github.com/hhool8/unblocked-games-g-plus)  
> **Deployment:** GitLab CI → GitLab Pages (served via custom domain CNAME)

A static HTML5 game portal hosting **474+ free browser games**. No server-side runtime required. All pages are pre-generated and served as static files.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Getting Started (Developer)](#getting-started-developer)
- [Content Pipeline (Operations)](#content-pipeline-operations)
- [Deployment (DevOps)](#deployment-devops)
- [SEO & Domain (Marketing / Growth)](#seo--domain-marketing--growth)
- [Maintenance](#maintenance)
- [Contributing](#contributing)

---

## Project Overview

| Property | Value |
|---|---|
| Site type | Static HTML — no framework, no build step for HTML |
| Game count | 474 games across 20 categories |
| Tech stack | Bootstrap 5, vanilla JS, Python scripts for content generation |
| Hosting | GitLab Pages + GitHub mirror |
| Custom domain | `unblocked-games-g-plus.poki2.online` (CNAME) |
| Main SEO site | `https://unblocked-games-g.poki2.online` (separate repo) |
| Target audience | Students on school Chromebooks, office users, casual gamers |

---

## Repository Structure

```
unblockedgamesgplus/
├── index.html              # Homepage — hero, featured games, category nav
├── search.html             # Client-side game search
├── 404.html                # Custom error page
├── CNAME                   # Custom domain: unblocked-games-g-plus.poki2.online
├── robots.txt              # Crawler rules + sitemap pointer
├── sitemap.xml             # Main sitemap (498 URLs, all pages + games)
├── sitemaps.xml            # Alternate sitemap (identical structure)
├── feed.xml                # RSS feed
├── favicon.ico
│
├── game/                   # 474 individual game pages (game/slug.html)
├── play/                   # Embedded game iframe pages
├── category/               # 20 category listing pages
│   ├── all.html, car.html, io.html, ...
├── contact/                # Contact page
├── privacy/                # Privacy policy
├── terms/                  # Terms of use
│
├── assets/                 # Static assets
│   ├── bootstrap/          # Bootstrap 5 CSS/JS
│   ├── css/                # Custom styles
│   ├── js/                 # Custom scripts
│   ├── fonts/
│   ├── icons/
│   └── upload/             # Game thumbnail images (PNG)
│       └── 66games/png/
│
├── scripts/                # Python content-generation & maintenance scripts
│   ├── export_games_csv.py          # Export full game list to CSV
│   ├── extract_category_games.py    # Generate per-category CSV files
│   ├── gen_directory.py             # Build category landing pages
│   ├── gen_play_pages.py            # Build /play/* iframe wrapper pages
│   ├── seo_inject_games.py          # Inject SEO metadata into game pages
│   ├── fix_technical_seo.py         # Audit and patch technical SEO issues
│   ├── update_homepage.py           # Regenerate homepage game lists
│   ├── update_static_pages.py       # Sync static pages (privacy, terms, contact)
│   ├── gen_gsite_*.py               # Google Sites data export helpers
│   └── *.csv                        # Category game data files
│
├── docs/                   # Internal documentation
├── SEO-PLAN-unblockedgamesGplus.md  # SEO strategy document
└── README.googlesite.md    # Legacy Google Sites migration notes
```

---

## Getting Started (Developer)

### Prerequisites

- Python 3.8+ (for content scripts)
- Git
- Any static file server for local preview

### Local Preview

```bash
# Serve the site locally on port 8080
python3 -m http.server --directory . 8080
# Open http://localhost:8080
```

### Run Content Scripts

```bash
cd scripts/

# Export full game list
python3 export_games_csv.py

# Regenerate all category pages
python3 extract_category_games.py
python3 gen_directory.py

# Rebuild play (iframe) pages
python3 gen_play_pages.py

# Inject/update SEO tags across game pages
python3 seo_inject_games.py

# Audit technical SEO issues
python3 fix_technical_seo.py
```

> **Note:** Scripts read/write HTML files in-place. Always commit current state before running batch scripts.

### Adding a New Game

1. Create `game/<slug>.html` — copy an existing game page as template.
2. Add thumbnail to `assets/upload/66games/png/<slug>.png`.
3. Create `play/<slug>.html` with the game iframe URL.
4. Add the game entry to the relevant category CSV in `scripts/`.
5. Run `python3 scripts/gen_directory.py` to update category pages.
6. Run `python3 scripts/update_homepage.py` to refresh featured games.
7. Update `sitemap.xml` with the new URL (see [Maintenance](#maintenance)).

### Play Page UI Parameters

All pages in `play/*.html` support query parameters to control top bar visibility.

- Default behavior: all UI elements are visible.
- Supported keys: `bar`, `title`, `fullscreen`, `open`.
- Hide values: `0`, `false`, `no`, `hide`.

Examples:

```text
/play/1v1-lol.html
/play/1v1-lol.html?title=0
/play/1v1-lol.html?fullscreen=false&open=no
/play/1v1-lol.html?bar=hide
```

Notes:

- `bar` controls the entire top `<div class="bar">`.
- `title` controls the game title text.
- `fullscreen` controls the Fullscreen button.
- `open` controls the Open link.

---

## Content Pipeline (Operations)

### Game Catalog Flow

```
scripts/*.csv  →  gen_directory.py  →  category/*.html
                                    →  index.html (featured)
             →  gen_play_pages.py   →  play/*.html
             →  seo_inject_games.py →  game/*.html (meta tags)
```

### Category Pages (20 total)

| Category | File |
|---|---|
| All Games | `category/all.html` |
| IO Games | `category/io.html` |
| Car | `category/car.html` |
| Shooting | `category/shooting.html` |
| Parkour | `category/parkour.html` |
| Running | `category/running.html` |
| Platform | `category/platform.html` |
| Stickman | `category/stickman.html` |
| Soccer | `category/soccer.html` |
| Clicker | `category/clicker.html` |
| Fighting | `category/fighting.html` |
| Multiplayer | `category/multiplayer.html` |
| Two-Player | `category/two-player.html` |
| Trending | `category/trending.html` |
| New | `category/new.html` |
| Racing | `category/racing.html` |
| Puzzle | `category/puzzle.html` |
| Skill | `category/skill.html` |
| School | `category/school.html` |
| Kids | `category/kids.html` |

### Updating the Sitemap

After adding or removing pages, regenerate the sitemap manually or via script. Ensure all `<loc>` values use `https://unblocked-games-g-plus.poki2.online/` and set `<lastmod>` to today's date (`YYYY-MM-DD`).

```bash
# Quick domain check
grep -c 'unblocked-games-g-plus.poki2.online' sitemap.xml
# Expected: ~498 (homepage + categories + game pages)
```

---

## Deployment (DevOps)

### Pipeline

Push to `main` → GitLab CI triggers → site published to GitLab Pages → served at custom domain via CNAME.

```yaml
# .gitlab-ci.yml (summary)
pages:
  stage: deploy
  script:
    - cp -r ./* .public && mv .public public
  artifacts:
    paths: [public]
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

### Custom Domain Setup

| Setting | Value |
|---|---|
| `CNAME` file | `unblocked-games-g-plus.poki2.online` |
| DNS | CNAME record pointing to GitLab Pages |
| `robots.txt` sitemap | `https://unblocked-games-g-plus.poki2.online/sitemap.xml` |

### GitHub Mirror

The repo is also mirrored to GitHub at `git@github.com:hhool8/unblocked-games-g-plus.git`.  
Push to either remote; GitLab CI only watches the GitLab remote.

```bash
# Push to both remotes
git push origin main          # GitHub (primary dev remote)
# Set up GitLab remote separately if needed:
# git remote add gitlab git@gitlab.com:hhool8/unblockedgames66.git
```

### Rollback

```bash
# Hard reset to a known-good commit
git reset --hard <commit-sha>
git push --force origin main
```

---

## SEO & Domain (Marketing / Growth)

### Domain Hierarchy

```
poki2.online  (root brand)
├── unblocked-games-g.poki2.online      ← Main SEO landing site (separate repo: h5games_poki2_site)
└── unblocked-games-g-plus.poki2.online ← Game library portal (THIS repo)
```

### SEO Configuration

| Element | Location |
|---|---|
| Per-page `<title>`, `<meta description>` | Each `game/*.html`, `category/*.html` |
| Canonical URLs | `https://unblocked-games-g-plus.poki2.online/<path>` |
| Sitemap | `sitemap.xml` (498 URLs), referenced in `robots.txt` |
| SEO strategy | `SEO-PLAN-unblockedgamesGplus.md` |
| Technical SEO audit | `scripts/fix_technical_seo.py` |

### Key SEO Keywords

`unblocked games g+`, `g plus unblocked games`, `unblocked games 6x`, `unblocked game websites`, `school chromebook games`

### Ahrefs Domain Verification

The file `ahrefs_585f4691b0e399a160cb6e0c016b4fcd7b0c55de8ae4d7dc4c83d5d0761520b3` is the Ahrefs site ownership token — do not delete or rename it.

---

## Maintenance

### Routine Tasks

| Frequency | Task | How |
|---|---|---|
| On game add/remove | Update sitemap + category CSV | `scripts/gen_directory.py` |
| Weekly | Check broken game iframes | `scripts/fix_technical_seo.py` |
| Monthly | Update `<lastmod>` in sitemap | `sed -i 's/OLD_DATE/NEW_DATE/g' sitemap.xml sitemaps.xml` |
| As needed | Refresh homepage featured games | `scripts/update_homepage.py` |

### Quick Domain Sync (after domain change)

```bash
OLD="https://old-domain.example.com"
NEW="https://unblocked-games-g-plus.poki2.online"
sed -i "s|$OLD|$NEW|g" sitemap.xml sitemaps.xml robots.txt
```

### File Count Sanity Check

```bash
ls game/ | wc -l      # Should be 474
ls category/ | wc -l  # Should be 20
grep -c '<loc>' sitemap.xml  # Should be ~498
```

---

## Contributing

1. Fork or clone the repo.
2. Create a feature branch: `git checkout -b feat/add-game-slug`.
3. Follow the [Adding a New Game](#adding-a-new-game) steps.
4. Commit with a descriptive message: `git commit -m "add: game SlugName + category update"`.
5. Push and open a Pull Request to `main`.

---

*© 2026 Unblocked Games G+. All rights reserved.*
