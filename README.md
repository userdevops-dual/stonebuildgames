# StoneBuild Games — Website

Production domain: **https://stonebuildgames.com** · Support email: **support@stonebuildgames.com**

A static, zero-build website for the StoneBuild Games studio: services, games catalogue, privacy policy
and terms (required for Google Play / App Store listings), with a 3D animated hero and full-screen sections.

```
site/                      ← publish this folder
  index.html               Home: 6 full-screen sections (hero, services, Stone Stack game, games, why us, contact)
  services/index.html      Six services, engagement models, process, FAQ
  about/index.html         Studio story, values, process, toolbox
  games/index.html         Games catalogue (first card is static; more come from js/games-data.js)
  contact/index.html       Contact details + inquiry form (opens the visitor's email app)
  privacy-policy/index.html, terms/index.html, 404.html
  css/styles.css           Design system + layout (tokens at the top)
  css/fonts.css + fonts/   Self-hosted Inter and Sora (no Google Fonts request)
  js/main.js               Pill navbar, nav, section dots, reveals, page transitions, contact form
  js/hero3d.js             Three.js hero scene (lazy, desktop only; CSS fallback on phones)
  js/game.js               Stone Stack mini-game (canvas)
  js/games-data.js         ← EDIT THIS to add games
  js/games.js              Renders game cards + VideoGame structured data
  vendor/                  gsap, ScrollTrigger, three (self-hosted, pinned)
  assets/                  favicon, logo, OG image
  robots.txt  sitemap.xml  llms.txt  site.webmanifest  _headers  .well-known/security.txt
PLAN.md                    Design + architecture plan
stonebuildgames.com-audit/ SEO audit findings and Lighthouse reports (not deployed)
.claude/launch.json        Local preview (python http.server on :8787)
```

## Run locally

```bash
python3 -m http.server 8787 -d site
```
Open http://localhost:8787

## Add a game (when your game is ready)

1. Open `site/js/games-data.js`.
2. Copy the `TEMPLATE` object into the `STONEBUILD_GAMES` array and fill it in:
   `title`, `tagline`, `description`, `genre`, `platforms`, `status` (`live` / `coming-soon` / `in-production`),
   `playStore` URL, optional `cover` image (put it in `site/assets/games/`, 1600×1000 WebP or PNG).
3. Set `status: "live"` once it is on Google Play. The Games page and home section update automatically,
   and live games get `VideoGame` structured data for Google.
4. Replace the placeholder "Our first title" entry when the first game ships, and delete the static
   placeholder card in `site/games/index.html` (the one marked `data-prerendered`); the script replaces it anyway.

## Google Play listing

Use these public URLs in Play Console:

| Field | URL |
|---|---|
| Privacy policy | https://stonebuildgames.com/privacy-policy/ |
| Terms | https://stonebuildgames.com/terms/ |
| Data deletion (if your game has accounts) | https://stonebuildgames.com/privacy-policy/#data-deletion |
| Website | https://stonebuildgames.com |
| Support email | support@stonebuildgames.com |

Before you submit, check the privacy policy's Section 4 and remove any SDK your game does not use
(AdMob, Unity Ads, Firebase, Play Games Services). The Play "Data safety" form must match it.

## Deploy (pick one — all free)

**Cloudflare Pages (recommended):** Pages → Create project → Upload assets → upload the `site/` folder.
Add custom domain `stonebuildgames.com` (Cloudflare manages DNS automatically). `_headers` is picked up.

**Netlify:** drag the `site/` folder onto app.netlify.com/drop, then Domain settings → add `stonebuildgames.com`.

**GitHub Pages:** push `site/` contents to a repo, enable Pages, add a `CNAME` file containing `stonebuildgames.com`.

After deploy:
1. Submit `https://stonebuildgames.com/sitemap.xml` in Google Search Console.
2. Verify the OG image at https://stonebuildgames.com/assets/og-image.png renders in a share preview.

## Email: support@stonebuildgames.com

Free options: **Cloudflare Email Routing** (forward to your Gmail; sending needs a Gmail "send as" setup) or
**Zoho Mail Free** (real mailbox, 5 users). Paid: Google Workspace.
The contact form on the site opens the visitor's email client addressed to this mailbox, so it works with no backend.
If you later want a hosted form, point the form at Formspree or Netlify Forms and remove the mailto handler in `js/main.js`.

## Before launch: fill in the blanks

- Footer social icons point to `#`. Replace them with your YouTube / Instagram / X / LinkedIn URLs
  (search for `rel="nofollow"` in the pages) or delete the ones you do not use.
- Terms section 16 names no country. Add the country where the studio is registered.
- Consider adding founder name and country to the Organization schema in `site/index.html` once you want them public.
- If you deploy on Cloudflare, check that its AI-crawler blocking is off (it can override `robots.txt`).

## Customising

- Colors, fonts, spacing: `:root` tokens at the top of `site/css/styles.css`.
- Services, process steps, why-us copy: edit `site/index.html` directly (plain HTML).
- The hero 3D scene: `site/js/hero3d.js` (stone count, colors, speed).
- Full-screen snapping is on for desktops ≥ 1024px wide and ≥ 720px tall; mobile scrolls normally.
- The Stone Stack game lives in `site/js/game.js` (block height, speed curve, colors at the top of the file).
- Pages share the same header and footer markup; when you change it, change it in every page (or ask Claude to re-run the page builder).
- Everything respects `prefers-reduced-motion`.
