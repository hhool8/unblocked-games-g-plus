# Car Category — Scripts & Generated Files

> Located in: `ug66/unblockedgames66.gitlab.io/scripts/`

---

## Overview

This folder contains a one-script pipeline that extracts all games from the **Car** category page, then produces a CSV data file and a plug-and-play Google Sites embed widget.

---

## Files

| File | Type | Description |
|------|------|-------------|
| `extract_car_games.py` | Python script | Main pipeline — reads source HTML, writes CSV + embed HTML |
| `gen_car_gsite_html.py` | Python script | Earlier HTML-only version, superseded by above |
| `car_games.csv` | CSV (34 rows) | Structured game data — 6 columns |
| `car_games_googlesite.html` | HTML (~35 KB) | Self-contained embed widget for Google Sites |

---

## How to Run

```bash
cd ug66/unblockedgames66.gitlab.io
python3 scripts/extract_car_games.py
```

Both output files are regenerated on every run. No third-party dependencies required.

---

## Script: `extract_car_games.py`

### Constants

| Constant | Value |
|----------|-------|
| `BASE` | `Path(__file__).parent.parent` (repo root) |
| `CAT_FILE` | `category/car.html` |
| `GAME_DIR` | `game/` |
| `IMG_PREFIX` | `https://unblocked-games-g-plus.poki2.online` |
| `PLAY_PREFIX` | `https://unblocked-games-g-plus.poki2.online/play` |
| `LINK_PREFIX` | `https://sites.google.com/view/unblocked-games-g-site` |
| `OUT_CSV` | `scripts/car_games.csv` |
| `OUT_HTML` | `scripts/car_games_googlesite.html` |

### Logic Flow

1. **Parse** `category/car.html` — extract all `<a class="card" href="/game/{slug}.html">` blocks (34 games).
2. **Per game** — read `game/{slug}.html`:
   - Primary description: `<div class="description pb-2"><p>…</p></div>`
   - Fallback: `<meta name="description" content="…">`
3. **Build name** — strip HTML `<h3>` text, apply `.upper()`.
4. **Write CSV** — 6 columns (see below).
5. **Write HTML** — responsive CSS grid, all 34 game cards.

---

## Output: `car_games.csv`

**6 columns, 34 data rows.**

| Column | Example |
|--------|---------|
| `slug` | `drift-boss` |
| `name` | `DRIFT BOSS` (always uppercase) |
| `image` | `https://unblocked-games-g-plus.poki2.online/assets/upload/66games/jpg/drift-boss.jpg` |
| `description` | Full English description from the game page |
| `play_url` | `https://unblocked-games-g-plus.poki2.online/play/drift-boss.html` |
| `link` | `https://sites.google.com/view/unblocked-games-g-site/drift-boss` |

> **Note:** Image paths for games 31–34 use `/assets/upload/busqueda/jpg/` instead of `/assets/upload/66games/jpg/`.

---

## Output: `car_games_googlesite.html`

- Self-contained HTML file (~35 KB, well within Google Sites' ~100 KB embed limit).
- **Layout:** CSS Grid — `repeat(auto-fill, minmax(168px, 1fr))`, 14 px gap.
- **Cards:** thumbnail + uppercase title + 4-line clamped description.
- **Links:** open in the **same window** (no `target` attribute), no `.html` suffix in URL.
- **Images:** lazy-loaded, 180 × 180 px.

### How to Embed in Google Sites

1. Open your Google Site → navigate to the **Car** page.
2. Click **Insert → Embed**.
3. Select the **"Embed code"** tab.
4. Paste the entire contents of `car_games_googlesite.html`.
5. Click **Next → Insert**.
6. Resize/move the embed block as needed, then **Publish**.

---

## Game List (34 games)

| # | Slug | Name |
|---|------|------|
| 1 | adventure-drivers | ADVENTURE DRIVERS |
| 2 | blumgi-rocket | BLUMGI ROCKET |
| 3 | car-rush | CAR RUSH |
| 4 | cars-simulator | CARS SIMULATOR |
| 5 | crazy-cars | CRAZY CARS |
| 6 | crossy-road | CROSSY ROAD |
| 7 | deathcar-io | DEATHCAR IO |
| 8 | drift-boss | DRIFT BOSS |
| 9 | drift-hunters | DRIFT HUNTERS |
| 10 | drive-mad | DRIVE MAD |
| 11 | eggy-car | EGGY CAR |
| 12 | hill-climb-racing-2 | HILL CLIMB RACING 2 |
| 13 | impossible-monster-truck | IMPOSSIBLE MONSTER TRUCK |
| 14 | indian-truck | INDIAN TRUCK |
| 15 | jelly-truck | JELLY TRUCK |
| 16 | kart-fight-io | KART FIGHT IO |
| 17 | mad-truck-challenge | MAD TRUCK CHALLENGE |
| 18 | madalin-cars-multiplayer | MADALIN CARS MULTIPLAYER |
| 19 | madalin-stunt-cars-2 | MADALIN STUNT CARS 2 |
| 20 | madalin-stunt-cars-3 | MADALIN STUNT CARS 3 |
| 21 | monster-truck-vs-zombie | MONSTER TRUCK VS ZOMBIE |
| 22 | real-flying-truck | REAL FLYING TRUCK |
| 23 | real-garbage-truck | REAL GARBAGE TRUCK |
| 24 | rocket-league | ROCKET LEAGUE |
| 25 | scrap-metal-3-infernal-trap | SCRAP METAL 3 INFERNAL TRAP |
| 26 | smash-karts-io | SMASH KARTS IO |
| 27 | traffic-control | TRAFFIC CONTROL |
| 28 | traffic-run | TRAFFIC RUN |
| 29 | trafficmania | TRAFFICMANIA |
| 30 | x-trial-racing | X TRIAL RACING |
| 31 | 18-wheeler-truck-parking-ez | 18 WHEELER TRUCK PARKING |
| 32 | scrap-metal-infernal | SCRAP METAL INFERNAL |
| 33 | smash-karts | SMASH KARTS |
| 34 | ultimate-offroad-simulator | ULTIMATE OFFROAD SIMULATOR |
