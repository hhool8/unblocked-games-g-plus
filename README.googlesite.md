# Google Sites Build Guide — Unblocked Games G+

> Reference site: [classroom.center](https://sites.google.com/classroom.center/view-1/)  
> Goal: Google Sites acts as a traffic entry point and SEO satellite. The actual game content lives on GitHub Pages (your own infrastructure), giving you full control over ad placement.

---

## Architecture

```
Google Sites sub-page (e.g. "Slope")
    └─ Google Sites Embed
          └─ https://ug66.poki2.online/play/slope.html   ← your GitHub Pages (full control)
                ├─ AdSense ad slots (top + bottom)
                └─ <iframe src="https://unblockedgames66.gitlab.io/slope/"> ← real game
```

**Three-tier breakdown:**

| Layer | URL | Owner | Purpose |
|-------|-----|-------|---------|
| Google Sites | `sites.google.com/your-site/slope` | Google (free) | Traffic entry, search exposure, backlinks |
| Middle page | `ug66.poki2.online/play/{slug}.html` | **You** | AdSense ads, SEO metadata |
| Game files | `unblockedgames66.gitlab.io/{slug}/` | GitLab Pages | Real game assets, correct root paths |

---

## Generated Files

- **474 middle pages** in `docs/play/` — deployed via GitHub Pages
- Each page includes:
  - Top + bottom AdSense placeholder slots (`id="ad-top"` / `id="ad-bottom"`)
  - Game iframe pointing directly to the GitLab working URL (no double-nesting)
  - Fullscreen button + "Open ↗" direct link
  - `canonical` / Open Graph / `twitter:card` meta tags
  - Viewport-filling responsive height (subtracts ad bar heights)

**Generator script:** `scripts/gen_play_pages.py`  
**To regenerate all pages:**
```bash
cd /path/to/unblockedgames66.gitlab.io
python3 scripts/gen_play_pages.py
```

---

## Google Sites Build Steps

### Step 1 — Create the site

1. Go to [sites.google.com](https://sites.google.com) → click **+** New site
2. Name: `Unblocked Games G+` (or your choice)
3. Theme: choose a dark theme

### Step 2 — Set up the homepage

1. Select a **Blank** layout
2. Insert → **Embed** → enter:
   ```
   https://ug66.poki2.online/
   ```
3. Set embed height to `700px` (shows all 474 game cards)

### Step 3 — Create individual game sub-pages (start with the top 20)

For each game:
1. Bottom-right **⊕ New page** → name the page with the game title (e.g. `Slope`)
2. URL path auto-generates as `/slope`
3. Insert → **Embed** → paste the embed code from the table below
4. Set height to `700px` → Save

### Step 4 — Set up navigation

```
Home | IO Games | Shooting | Free Games | Two Player
```
Category pages can each embed the directory page with a hash filter (hash-filter feature to be added later).

### Step 5 — Publish

1. Top-right **Publish** → set visibility to **Public**
2. Optionally set a custom URL (requires a paid Google Workspace account)
3. After publishing, submit the sitemap in Google Search Console

---

## Top 20 Game Embed Codes

> Generic format — replace `{slug}` with the game's slug:
> ```html
> <iframe src="https://ug66.poki2.online/play/{slug}.html"
>         width="100%" height="700"
>         frameborder="0"
>         allow="fullscreen; autoplay; gamepad">
> </iframe>
> ```

| Game | Slug | Embed URL (paste into Google Sites) | Real Game URL |
|------|------|--------------------------------------|--------------|
| Slope | `slope` | `https://ug66.poki2.online/play/slope.html` | `https://unblockedgames66.gitlab.io/slope/` |
| 1v1 LOL | `1v1-lol` | `https://ug66.poki2.online/play/1v1-lol.html` | `https://unblockedgames66.gitlab.io/1v1-lol/` |
| Geometry Dash | `geometry-dash` | `https://ug66.poki2.online/play/geometry-dash.html` | `https://unblockedgames66.gitlab.io/geometry-dash/` |
| Run 3 | `run-3` | `https://ug66.poki2.online/play/run-3.html` | `https://unblockedgames66.gitlab.io/run-3/` |
| Cookie Clicker | `cookie-clicker` | `https://ug66.poki2.online/play/cookie-clicker.html` | `https://unblockedgames66.gitlab.io/cookie-clicker/` |
| Drift Hunters | `drift-hunters` | `https://ug66.poki2.online/play/drift-hunters.html` | `https://unblockedgames66.gitlab.io/drift-hunters/` |
| Smash Karts | `smash-karts` | `https://ug66.poki2.online/play/smash-karts.html` | `https://unblockedgames66.gitlab.io/smash-karts/` |
| Basketball Stars | `basketball-stars` | `https://ug66.poki2.online/play/basketball-stars.html` | `https://unblockedgames66.gitlab.io/basketball-stars/` |
| Krunker.io | `krunker-io` | `https://ug66.poki2.online/play/krunker-io.html` | `https://unblockedgames66.gitlab.io/krunker-io/` |
| Retro Bowl | `retro-bowl` | `https://ug66.poki2.online/play/retro-bowl.html` | `https://unblockedgames66.gitlab.io/retro-bowl/` |
| Bloxd.io | `bloxd-io` | `https://ug66.poki2.online/play/bloxd-io.html` | `https://unblockedgames66.gitlab.io/bloxd-io/` |
| OvO | `ovo` | `https://ug66.poki2.online/play/ovo.html` | `https://unblockedgames66.gitlab.io/ovo/` |
| Among Us | `among-us` | `https://ug66.poki2.online/play/among-us.html` | `https://unblockedgames66.gitlab.io/among-us/` |
| Minecraft Classic | `minecraft-classic` | `https://ug66.poki2.online/play/minecraft-classic.html` | `https://unblockedgames66.gitlab.io/minecraft-classic/` |
| Happy Wheels | `happy-wheels` | `https://ug66.poki2.online/play/happy-wheels.html` | `https://unblockedgames66.gitlab.io/happy-wheels/` |
| Flappy Bird | `flappy-bird` | `https://ug66.poki2.online/play/flappy-bird.html` | `https://unblockedgames66.gitlab.io/flappy-bird/` |
| Vex 5 | `vex-5` | `https://ug66.poki2.online/play/vex-5.html` | `https://unblockedgames66.gitlab.io/vex-5/` |
| Moto X3M | `moto-x3m` | `https://ug66.poki2.online/play/moto-x3m.html` | `https://unblockedgames66.gitlab.io/moto-x3m/` |
| Shell Shockers | `shell-shockers` | `https://ug66.poki2.online/play/shell-shockers.html` | `https://unblockedgames66.gitlab.io/shell-shockers/` |
| Subway Surfers | `subway-surfers` | `https://ug66.poki2.online/play/subway-surfers.html` | `https://unblockedgames66.gitlab.io/subway-surfers/` |

---

## Enabling Ads

All 474 pages contain two placeholder ad slots:

```html
<!-- Top ad slot -->
<div class="ad-placeholder" id="ad-top">ADVERTISEMENT</div>

<!-- Bottom ad slot -->
<div class="ad-placeholder" id="ad-bottom">ADVERTISEMENT</div>
```

**To activate AdSense (once your account is approved):**

1. Open `scripts/gen_play_pages.py`
2. In the `make_page()` function, replace the `<div class="ad-placeholder" ...>` lines with your AdSense `<ins class="adsbygoogle" ...>` code
3. Regenerate and deploy:
```bash
python3 scripts/gen_play_pages.py
git add docs/play && git commit -m "ads: inject AdSense units" && git push
```

---

## All 474 Game Slugs

Any game is accessible at `https://ug66.poki2.online/play/{slug}.html`.

<details>
<summary>Click to expand all 474 slugs</summary>

```
10-minutes-till-dawn, 1010-color-match, 18-wheeler-truck-parking-ez, 1v1-lol,
2048-fusion, 2048, 3-pandas-in-japan, 3d-bowling, 3d-free-kick, 99-balls,
a-dance-of-fire-and-ice, a-small-world-cup, achievement-unlocked,
adam-and-eve-5-part-2, adam-and-eve-5-part-one, adam-and-eve-6, adam-and-eve-7,
adventure-drivers, agarpaper-io, alien-hominid, amazing-rope-vice-spider-vegas,
amazing-strange-rope-police, amidst-the-sky, amogus-io, among-us, angry-gran-run,
apple-shooter, aquapark-io, arcane-archer, archery-world-tour, arras-io,
aspiring-artist, awesome-tanks-2, backflipper, backrooms-2d, backrooms,
bacon-may-die, bad-egg-io, bad-ice-cream-2, bad-ice-cream-3,
baldis-basics-field-trip, baldis-basics, ball-sort-soccer, ballistic,
basket-and-ball, basket-bros-io, basket-random, basketball-legends,
basketball-stars, battledudes-io, betrayal-io, big-tower-tiny-square,
biker-street, bitlife, block-tanks, block-the-pig, block-world, blockpost,
blocky-snakes, bloomgi-bloom, bloons-td-2, bloons-td4, bloxd-io, bloxorz,
blumgi-bloom, blumgi-rocket, blumgi-slime, bob-the-robber-2,
booblehead-soccer-royale, booblehead-soccer, bottle-flip-3d, bouncy-woods,
boxing-phsyics-2, boxing-physics-2, boxing-random, braains-io, breaking-the-bank,
browserfps-com, bullet-force, bullet-party-2, burger-clicker,
burrito-bison-launcha-libre, burrito-bison, candy-crush-saga, cannon-basketball-4,
car-rush, cars-simulator, case-clicker, checkers, chicken-merge, choppy-orc,
circlo0, city-coach-bus-sim, clicker-heroes, climb-over-it, color-switch-challenges,
connect-3, cookie-clicker, craftmine, crazy-cars, crazy-tunel-3d,
creative-kill-chamber, crossy-road, cubeshot-io, cut-the-rope, dark-ninja,
dashcraft-io, dead-again, deadshot-io, deal-or-no-deal, death-run-3d,
deathcar-io, diebrary, dino-chrome-io, dinosaurs-merge-master, dogeminer,
doodle-jump, down-the-hill, dreadhead-parkour, drift-boss, drift-hunters,
drive-mad, duke-dashington-remastered, dunkers-2, eggy-car, elastic-man,
electron-dash, endless-tunnel, endless-war-3, eparkour-io, ev-io,
fall-guys-ultimate-knockout, falling-fred, farm-match-seasons, ferge-io,
fightz-io, fire-truck-rescue, fireboy-and-watergirl-6,
fireboy-and-watergirl-forest-temple, fishing-and-lines, fishing-frenzy,
five-nights-at-freddies-2, five-nights-at-freddys-3, flappy-bird, flip-bottle,
fnaf-2, fnaf-4, fnaf-shooter, fnaf-web, fnf-online, football-run,
football-strike, fortnite-made-in-china, fred-running, free-kick-classic,
funny-shooter-3d, funny-shooter-destroy-all, gartic-io, gartic-phone-io,
geodash-2, geodash, geometry-dash-2, geometry-dash,
geometry-monster-shell-shockers, get-on-top, getaway-shootout, getting-over-it,
gigga-io, gobdun, gold-digger-frvr, grand-vegas-simulator, granny,
gravity-soccer, grindcraft-remastered, gswitch-2, gswitch-3, gswitch-4,
gswitch, gulper-io, gun-mayhem-2, gun-mayhem-redux, gun-spin,
hammer-2-reloaded, hammer-2, hanger-2, hanger, happy-fishing, happy-wheels,
head-soccer-2023, hexbee-merger, hide-and-smash, hill-climb-racing-2, hole-io,
hop-and-pop-it, house-of-hazards, icy-purple-head-2, icy-purple-head-3,
idle-breakout, idle-light-city, idle-mining-empire, idle-restaurants-tycoon,
idle-restaurants, idle-tree-city, impossible-monster-truck, indian-truck,
infinite-soccer, iron-snout, jelly-truck, jetpack-joyride-browser,
jetpack-joyride, jewels-blitz-5, johnny-revenge, johnny-trigger,
johnny-upgrade, johny-revenge, johny-trigger, jungle-td, jungle-tower-defense,
just-fall-lol, kart-fight-io, kirka-io, knight-hero-adventure-rpg,
knight-hero-adventure, krunker-io, leader-strike, learn-to-fly, lol-shot-io,
lolbeans-io, lurkers-io, mad-gunz, mad-shark, mad-truck-challenge,
madalin-cars-multiplayer, madalin-stunt-cars-2, madalin-stunt-cars-3,
marbles-sorting, masked-forces, merc-zone, merge-harvest, merge-round-racers,
minecraft-case-simulator, minecraft-classic, money-movers-2, money-movers-3,
money-movers-guard-duty, money-movers, money-roller, money-rush, monkey-mart,
monster-truck-vs-zombie, moomoo-io-sandbox, moto-maniac-3, moto-x3m-3-pool-party,
moto-x3m-6-spooky-land, moto-x3m-spooky-land, moto-x3m-two, moto-x3m,
moto-x3m4-winter, moto3xm-pool-party, mr-bullet, mutazone, narrow-one,
ninja-cat-exploit, ninja-vs-evil-corp, noob-steve-parkour, noob-steve,
offroad-ultimate, only-up-2, only-up-3d-parkour, only-up, ovo-2-144-version,
ovo-3-dimensions, ovo-3, ovo, pacman-remake, papas-burgeria, papas-freezeria,
papas-pizzaria, paper-2-io, park-out, parking-fury-2, parking-fury-3,
parking-fury, parkour-race, penalty-kick-online, penalty-kick,
penalty-shooters-2, penalty-shooters-3, petz-lol, pixel-gun-3d,
pixel-gun-apocalypse-2, pixel-smash-duel, pizza-tower, poop-clicker-3, pou,
president-simulator, pudding-monsters, push-the-box, rabbit-samurai-2,
raft-wars-2, raft-wars, raft-warz-2, rainbow-parkour-kogama, real-flying-truck,
real-garbage-truck, recoil, red-driver-5, repuls, retro-bowl, riddle-school-5,
riddle-transfer-2, rise-of-neon-square, roblox, rocket-league, rolling-ball-3d,
rolly-vortex-ball, rooftop-snipers-2, rooftop-snipers, roper, royale-dudes-io,
royale-dudes, run-3, running-fred, sandstrike-io, sausage-flip, sausage-flipping,
save-the-doge, scenexe-io, scrap-metal-3-infernal-trap, scrap-metal-infernal,
shell-shockers-io, shell-shockers, ships-3d, short-ride, skibidi-toilet-attack,
skibidi-toilet-rampage, skiing-fred, skillfite-io, skyblock, slime-rush-td,
slope-2-players, slope-ball, slope-two-players-multiplayer, slope, small-world-cup,
smash-karts-io, smash-karts, snail-bob-5, snail-bob-8, snail-bob-fantasy-story,
snail-bob-island-story, snail-bob-love-story, snail-bob-space-trip,
snail-bob-winter-story, snake-io, snay-io-agario, sniper-shot-bullet-time,
sniper-shot, snipey-io, snow-battle-io, snow-rider-3d, soccer-heads,
soccer-random, soccer-skills-euro-cup-2021, soccer-skills-euro,
sonic-the-hedgehog-remastered, spider-solitaire, sprinter, stabfish-2,
stabfish-io, stack-bump-3d, starblast-io, stealing-the-diamond,
stick-archers-battle, stick-defenders, stick-duel-battle, stick-merge,
stickbattle-lol, stickman-boost-2, stickman-boost, stickman-hook,
subway-princess-runner, subway-runner, subway-surfers-bali, subway-surfers-hawaii,
subway-surfers-new-york, subway-surfers-san-francisco, subway-surfers-zurich,
subway-surfers, sugar-shock-io, suika-game, suika, super-falling-fred,
super-fowlst, super-hexbee-merger, super-liquid-soccer, super-mario-64,
super-mario-bros, superhot, surviv-io, survivor-in-rainbow-monster,
table-tennis-ultimate-tournament, taming-io, tank-trouble-2, tank-trouble,
tanuki-sunset, tap-tap-shots, temple-run-2, tetris, the-backrooms-3d,
the-backrooms, the-bowling-club, the-final-earth-2, the-final-earth,
the-fish-master, the-heist, the-impossible-quiz-2, the-impossible-quiz,
there-is-no-game, timber-man, time-shooter-2, time-shooter-3-swat, time-shooter-3,
tiny-fishing, tomb-runner, tower-crash-3d, tower-defense-2d, traffic-control,
traffic-run, trafficmania, tribals-io, tricksplit-io, tricksplit, tube-clicker,
tube-jumpers, tunnel-rush-2, tunnel-rush, turn-turn, two-ball-3d, two-tunnel-3d,
ultimate-offroad-simulator, uno-4-colors-multiplayer, uno, venge-io, vex-3,
vex-4, vex-5, vex-6, vex-7, vex-8, volley-random, voxiom-io, war-brokers-io,
wheelie-bike, wheely-2, wheely-3, wheely-4-time-travel, wheely-5,
wheely-6-fairytale, wheely-7-detective, wheely-8-aliens, wizard-mike, word-slide,
wordle-infinite, wordle-plus, worlds-hardest-game-2, worlds-hardest-game,
wormate-io, wrestle-bros-io, x-trial-racing, yohoho-io, zombie-shooter-2d,
zombs-royale-io, zuck-vs-musk-techbro-beatdown
```

</details>

---

## Manual Checklist (human action required)

| # | Action | Notes |
|---|--------|-------|
| 1 | Sign in to [sites.google.com](https://sites.google.com) | Use a Google account |
| 2 | Create new site "Unblocked Games G+" | Choose a dark theme |
| 3 | Embed `https://ug66.poki2.online/` on the homepage | Set height to 700px |
| 4 | Create 20 individual game sub-pages | Copy embed codes from the table above |
| 5 | Set up navigation bar | Home / IO Games / Shooting / Free Games |
| 6 | Publish the site as Public | Top-right Publish button |
| 7 | Submit sitemap in Google Search Console | `https://ug66.poki2.online/sitemap.xml` |
| 8 | Apply for Google AdSense | Replace ad placeholders once account is approved |

---

## Branch Info

- **Branch:** `dev_googlesite`
- **Contents:**
  - `scripts/gen_play_pages.py` — generator script
  - `docs/play/*.html` — 474 game middle pages
  - `README.googlesite.md` — this file

Once merged into `main`, GitHub Pages auto-deploys and `ug66.poki2.online/play/{slug}.html` becomes live.
