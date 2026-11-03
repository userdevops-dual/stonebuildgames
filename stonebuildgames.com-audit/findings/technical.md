# Technical SEO findings: stonebuildgames.com (pre-launch)

Audited snapshot: site/ as on disk at 2026-11-04 04:22 PKT (8 HTML pages incl. /services/, /about/, /contact/, self-hosted fonts, lazy three.js). Source-read, local Chrome checks; helper scripts not usable on localhost. Lighthouse not run (npx install denied). Earlier findings about Google Fonts, stray CSS brace, 404 canonical, JSON-LD "&amp;", eager three.js and JS-only games card were true for the pre-rebuild files and are fixed or obsolete in this snapshot.

Score: 80/100.

| Category | Status |
|---|---|
| Crawlability | PASS (robots.txt allow-all + absolute Sitemap; sitemap 7 URLs = 7 indexable pages) |
| Indexability | PASS (self-canonicals, unique titles/descriptions <=60/<=160, 404 noindex w/o canonical, no broken links/anchors) |
| Security | WARN (no CSP, no HSTS in _headers) |
| URL structure | PASS (clean trailing-slash URLs; www->apex and http->https must be set at host, not verifiable) |
| Mobile | PASS (viewport OK, 44px nav toggle; not re-measured on new pages) |
| Core Web Vitals | WARN (hero LCP gated behind JS reveal; not re-measured after rebuild) |
| Structured data | PASS (all JSON-LD parses) |
| JS rendering | PASS (games card prerendered in HTML) |
| IndexNow | FAIL (no key file) |

## High
1. Placeholder footer links on all 8 pages (index, services, about, games, contact, privacy-policy, terms, 404): four `<a href="#" rel="nofollow">` (YouTube, Instagram, X, LinkedIn) under comment "Replace the # links". Fix: delete them or insert real profile URLs; then add `sameAs` to Organization JSON-LD in index.html.
2. LCP hidden until JS: css/styles.css:401 `.js .reveal{opacity:0}`; js/main.js revealWithGsap sets hero words/lead to opacity 0 with 0.25s/0.55s delays; fallback only at 1200 ms (inline script line 32). Fix: leave h1 and hero .lead visible at first paint (remove `reveal`/opacity:0 from them; animate transform only).
3. Cache-Control on unversioned URLs (_headers): /css/* and /js/* 7 days; /assets/*, /vendor/*, /fonts/* immutable 1 year. A deploy can leave stale CSS/JS against new HTML; og-image.png edits stick for a year. Fix: fingerprint (styles.css?v=<hash>) or use `public, max-age=0, must-revalidate` for /css/* and /js/*, and `max-age=86400` for /assets/*.

## Medium
- _headers: add `Strict-Transport-Security: max-age=31536000` (after HTTPS confirmed) and a CSP (inline head script + importmap need hashes; style attributes need style-src-attr 'unsafe-inline'). Not re-validated against rebuilt pages.
- js/games.js removes the prerendered card and re-renders it from games-data.js with different copy ("GET IT ON" vs "COMING TO") and a second source of truth; skip re-render when data-prerendered exists.
- No `scroll-margin-top` in css/styles.css: /privacy-policy/#data-deletion heading lands under the fixed header (confirmed on old build; not re-measured).
- Duplicate ids sbg-top/sbg-mid/sbg-base on every page (header + footer SVG gradients).
- index.html: `<footer>` nested inside `<main>`/section#contact; move after `</main>`.
- IndexNow: add `<key>.txt` in site root and submit URLs (or enable Cloudflare Crawler Hints).
- Block `https://:project.pages.dev/*` with `X-Robots-Tag: noindex` in _headers.

## Low
- sitemap changefreq/priority ignored by Google; lastmod hand-maintained.
- 200 ms JS navigation delay for non-view-transition browsers (js/main.js).
- --text-3 (#6f7a8b) is 4.21:1 on card backgrounds.
- Verify live /robots.txt after deploy (Cloudflare managed robots can prepend rules).
