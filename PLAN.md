# StoneBuild Games — Website Plan

Domain: https://stonebuildgames.com  ·  Email: support@stonebuildgames.com

## Goals
1. Present StoneBuild Games as a professional game development studio (services + own titles).
2. Give every game a public home: a Games page that grows as titles ship, plus Privacy Policy and
   Terms pages that satisfy Google Play / App Store listing requirements.
3. Feel premium: full-viewport sections (one section = one screen, snap scrolling), real motion
   graphics (3D hero, scroll reveals), generous side spacing, strong typography.
4. Ship SEO-ready: semantic HTML, metadata, Open Graph, JSON-LD, sitemap, robots, fast static files.

## Stack (deliberately simple, zero build step)
- Static HTML + CSS + vanilla JS. Hostable anywhere (Cloudflare Pages, Netlify, Vercel, GitHub Pages).
- Three.js (CDN, pinned) for the 3D hero scene. GSAP + ScrollTrigger (CDN, pinned) for section motion.
- Games list driven by one data file: `site/js/games-data.js`. Adding a game = adding one object.
- No frameworks, no bundler, no tracking scripts by default.

## Design system
- Theme: dark "forge & stone". Background #0A0C10, surface #11151C, text #E8ECF2.
- Accent: logo orange #FF6A2B (primary), cool steel #7DD3FC (secondary). Gradient only on key moments.
- Type: Sora (display) + Inter (body), fluid sizes via clamp().
- Layout: 1240px container, side gutters clamp(24px, 6vw, 96px). 8pt spacing scale.
- Motion: GSAP word-by-word hero reveal, blur/slide section reveals, hero parallax on scroll, 3D low-poly
  "stones" with mouse parallax (desktop only, lazy-loaded), tilt cards, magnetic buttons, pill navbar on scroll,
  cross-document view transitions between pages. All motion respects prefers-reduced-motion.
- Logo: "Mined Block" mark (isometric block with a mined-out corner and a small cube popping free), orange #FF6A2B.
  Lockup: STONE BUILD in Chakra Petch 700 + spaced GAMES in orange. Footer carries a giant STONEBUILD wordmark.

## Pages
| URL | Purpose |
|---|---|
| `/` | Home. 6 full-viewport sections: Hero (3D), Services teaser, Stone Stack mini-game, Games, Why us / Tech, Contact + footer |
| `/services/` | Six services in depth, engagement models, process, FAQ |
| `/about/` | Studio story, values, process, toolbox |
| `/games/` | All games (data-driven cards with store badges, status, genre, platform) |
| `/contact/` | Contact details and inquiry form |
| `/privacy-policy/` | Studio-wide privacy policy covering website + all games (Play Store compliant) |
| `/terms/` | Terms & Conditions / EULA for games and site |
| `/404.html` | Branded not-found page |

## SEO checklist (applied in build, verified with the SEO skill afterwards)
- Unique title/description per page, canonical URLs, lang, viewport, theme-color.
- Open Graph + Twitter cards with a 1200×630 OG image.
- JSON-LD: Organization, WebSite, plus VideoGame on game cards, BreadcrumbList on inner pages.
- `sitemap.xml`, `robots.txt`, `site.webmanifest`, favicons.
- Semantic landmarks (header/nav/main/section/footer), one H1 per page, descriptive alt text.
- Performance: no heavy images, fonts with `display=swap`, deferred scripts, CDN libs pinned.

## Adding a new game later
1. Open `site/js/games-data.js`, copy an existing object, fill title, slug, genre, platforms, status,
   description, cover (SVG/WebP in `site/assets/games/`), `playStore` / `appStore` URLs.
2. Add the game's URL to `site/sitemap.xml` if it gets its own page.
3. Done. Home "Games" section and `/games/` update automatically.

## Deploy
- Upload the `site/` folder (publish directory = `site`) to Cloudflare Pages / Netlify.
- Point `stonebuildgames.com` DNS to the host. Set up `support@stonebuildgames.com` mailbox
  (Zoho Mail free / Google Workspace / Cloudflare Email Routing forwarding).
