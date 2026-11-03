# StoneBuild Games — SEO Action Plan (pre-launch, 2026-11-04)

Audited locally from the files in `site/` (domain not live yet). Specialist findings are in `findings/`.

## Applied in this build

| Area | Fix |
|---|---|
| Structured data | Organization + WebSite + WebPage graph on home; WebPage/CollectionPage/AboutPage/ContactPage + BreadcrumbList on inner pages; `&amp;` bug in Terms breadcrumb fixed; 404 schema removed; VideoGame JSON in `games.js` uses `GameApplication`, OS mapping, absolute image URLs, publisher `@id`, `installUrl`, `availability` |
| On-page | Home title 58 chars, description 145; every page has a unique title/description; H1 carries the topic keyword ("3D & mobile game development studio") as a kicker; headings in sequential order on every page |
| Content | Consistent studio sentence everywhere (Android, iOS and PC; no "console"); honest games copy ("first title in production for Android"); services copy targets "mobile game development", "game development company", Unity/Unreal/Godot; FAQ with six quotable answers on /services/ |
| Thin /games/ | Static first-title card in the HTML (no JS needed), honest title/description, disabled store badge rendered as a `<span>` |
| Performance | Fonts self-hosted (no Google Fonts request); three.js (670 KB) loads lazily and only on capable desktops; phones get a CSS hero; body fade-in removed (it caused NO_FCP in Lighthouse) |
| Privacy | Policy no longer mentions a cookie notice; states fonts/scripts are self-hosted and that the mini-game stores the best score only in the browser |
| Agents / AI | `robots.txt` lists search and answer-engine crawlers explicitly (a Content-Signal line was tried and removed because Lighthouse flags it as an invalid directive); `llms.txt` added; `.well-known/security.txt` added; section dots have `aria-label`s and larger hit areas; marquee duplicate is `aria-hidden`; breadcrumbs wrapped in `<nav>`; form status has `role="status"`; mobile menu closes on Escape |
| Caching / security | `_headers`: CSS and JS revalidate on every deploy, assets 1 day, fonts/vendor 1 year, HSTS and a Content-Security-Policy, `noindex` on the `*.pages.dev` preview host; IndexNow key file in `site/` |
| LCP | Hero headline and lead are never fully transparent (opacity .35 at first paint, then animated), so Chrome counts them as the LCP element immediately |
| Markup | No duplicate SVG gradient ids (header and footer marks use different ids); `scroll-margin-top` on inner-page anchors |

## Needs the owner (cannot be invented)

1. **Social / store profile URLs** — footer icons point to `#`. Replace or remove them, then add the URLs as `sameAs` in the Organization schema in `site/index.html`.
2. **Legal entity and country** — name the jurisdiction in Terms section 16 and, when ready, add `founder`, `foundingDate` and `address.addressCountry` to the Organization schema. Google Play's developer name must match "StoneBuild Games".
3. **After deploy on Cloudflare** — turn off AI-crawler blocking / Bot Fight Mode for search crawlers, and confirm the served `/robots.txt` equals the repo file.
4. **Search Console + Bing Webmaster Tools** — submit `sitemap.xml` on launch day; IndexNow when the first game ships.
5. **First real content** — a devlog or case-study post with a byline and date, real screenshots and a trailer for the first title. This is what earns citations and rankings; nothing on-page can substitute for it.
6. **Training-crawler policy** — `robots.txt` currently allows GPTBot / ClaudeBot / Google-Extended (no training preference stated). Add a `User-agent: GPTBot` / `ClaudeBot` / `Google-Extended` group with `Disallow: /` if you do not want training use; search and answer-engine crawlers stay allowed either way.

## Later (month 2+)

- Dedicated service pages (e.g. /services/unity-game-development/) only when each can carry 800+ words of genuine content.
- Replace the procedural cover art with real game screenshots (with alt text) and add a team photo on /about/.
- Clutch / GoodFirms / LinkedIn company profiles; genuine posts in r/gamedev; YouTube devlog.
