# Agent Readiness Audit: stonebuildgames.com (pre-launch, static review)

Reviewed 2026-11-04 from the files on disk (`site/`, exactly what will be served). No site files were modified.
Production domain is not live, and the claude-seo URL helpers cannot reach localhost, so this is a source review plus
one supplementary data source (an existing local Lighthouse 12.8.2 run, see section 3). Nothing here was measured
against a live host.

Files read: `index.html`, `games/index.html`, `privacy-policy/index.html`, `terms/index.html`, `404.html`,
`robots.txt`, `sitemap.xml`, `site.webmanifest`, `_headers`, `js/main.js`, `js/games.js`, `js/games-data.js`,
`css/styles.css` (selectors only), `js/hero3d.js` (grep only), `README.md`, `PLAN.md`.

## 1. Summary

| Measure | Result |
|---|---|
| Agent-readiness score (manual static rubric, section 2) | **67 / 100**. About 90 if every P0 and P1 item below is applied (estimate, not a promise) |
| Lighthouse Agentic Browsing | **Not run** (no live URL). Predicted counted audits: 2 (tree + CLS). Predicted desktop home result 1/2, caused by the section-dots links (A2). Prediction from the audit rules, not a measurement |
| Agent-UX 0-100 heuristic | **unavailable** (`render_page.py` cannot reach a pre-launch or localhost target). The 67 above is NOT this heuristic and NOT the Lighthouse fraction |
| P0 | 3 (A1 games list is JS-only, A2 unnamed section-dot links, A3 no deliberate AI-purpose robots groups; A3 is a policy decision and blocks nothing) |
| P1 | 4 |
| P2 | 6 |
| P3 | 7 |

What most limits agents today: the game list, the one page whose job is to tell an agent what the studio has shipped
and where to get it, is built in the browser by `js/games.js`. Today it holds a single placeholder card, so little is lost.
The day the first title ships, every store link will be invisible to any agent that does not run JavaScript.

## 2. Score rubric (manual, static)

| Area | Max | Score | Basis |
|---|---|---|---|
| A. Primary content available without JavaScript | 20 | 14 | Home, legal pages, 404 fully static. `/games/` list and its VideoGame JSON-LD are JS-only |
| B. Accessibility tree and semantics | 30 | 22 | Strong base. Deductions: unnamed dot links (-4), home footer inside `<main>` (-1), fake disabled store links (-1), silent form status (-1), JS-only `aria-current` (-0.5), heading order (-0.5) |
| C. Access policy (robots, signals, WAF) | 20 | 12 | robots.txt reachable, valid, sitemap declared, nothing blocked or noindexed. No AI-purpose groups or Content-Signal (-6). WAF untestable (-2) |
| D. Discovery and Markdown | 15 | 10 | Good JSON-LD, sitemap, canonicals, real 404 page. No llms.txt (-3), no Markdown (-2, optional) |
| E. Action reliability and stability | 15 | 9 | Visible mailto link works. Form is a mailto handoff an agent cannot confirm (-3), CLS headroom on `/games/` (-1), below-fold fade-in (-1), 7-day cache on the games data file (-1) |
| **Total** | **100** | **67** | |

## 3. Lighthouse Agentic Browsing

**Not run.** Reason: no live URL. Report as `n/a`, not as a fraction.

Lighthouse version to use: 13.5.0 (npm latest as of the matrix check 2026-09-23). The category needs Lighthouse 13.2 or later.

Predicted counted audits from the category rules (`references/lighthouse-agentic-category.md`):

| Audit | Predicted status | Why |
|---|---|---|
| `agent-accessibility-tree` | Home, desktop: likely FAIL. Home mobile and all other pages: likely pass | `link-name` on the six `.dots a` links (A2). `.dots` is `display:none` at 1100px and below, so a mobile run never evaluates them |
| `cumulative-layout-shift` | Counted. Likely pass, thin margin on `/games/` | See supplementary data below |
| `llms-txt` | N/A today (404 is N/A). Becomes counted once `/llms.txt` exists and is valid | 4xx is N/A, 5xx fails |
| `ard-schema` | N/A | No catalog signalled, `/.well-known/ai-catalog.json` will 404 |
| `webmcp-form-coverage` | Informative at most, never counted while the form is unannotated | One form, no `toolname` |
| `webmcp-registered-tools` | Informative or N/A | No tools registered |
| `webmcp-schema-validity` | N/A | No tools |

Predicted N = 2 today (tree + CLS), 3 with a valid `llms.txt`.

Paths that add a counted audit (options, not goals; a higher N is not a better site):
- Valid `/llms.txt`: +1 (recommended, cheap, section B1).
- Imperative WebMCP tools: adds `webmcp-schema-validity`. Not recommended here (section C5).
- Annotating every form: adds `webmcp-form-coverage`. Not recommended here; the form is a mailto handoff.
- Valid `ai-catalog.json`: +1. Not recommended; there are no agent resources to list, and an invalid or unreachable signalled catalog is a counted failure.

To get a real X/N before launch (this reviewer did not run it):
```
npx lighthouse@latest http://localhost:8787/ --only-categories=agentic-browsing --preset=desktop --output=json --output-path=./home-desktop.json
npx lighthouse@latest http://localhost:8787/ --only-categories=agentic-browsing --output=json --output-path=./home-mobile.json
"$HOME/.claude/skills/seo/scripts/claude-seo" run lighthouse_agentic.py --from-json ./home-desktop.json --json
```
(Needs Node 22.19+. Run desktop and mobile; they differ because of the `.dots` breakpoint.)

### Supplementary evidence: existing local Lighthouse run

`stonebuildgames.com-audit/lighthouse/home.report.json` and `games.report.json`: Lighthouse **12.8.2**, mobile, `http://localhost:8787`,
fetched 2026-11-03T23:02Z, standard categories only (no agentic category). Structured fields extracted only. Not a substitute for the fraction.

| Field | Home | Games |
|---|---|---|
| Accessibility category | 0.98 | 0.98 |
| `link-name`, `button-name`, `label`, `aria-hidden-focus`, `aria-allowed-attr`, `aria-prohibited-attr`, `definition-list` | all pass | pass or N/A |
| `heading-order` | FAIL (footer `h4` "Studio" follows an `h2`/`h3`) | FAIL (`h3` "Our first title" directly after `h1`) |
| Cumulative Layout Shift | 0 | **0.076** (score 0.95), single shift on `body > div.inner-footer-wrap` |
| LCP / TBT (mobile, throttled, localhost) | 8.8 s / 5,330 ms (perf 0.29) | 3.0 s / 60 ms (perf 0.92) |

Reading it: the axe rules behind the agentic tree audit pass on the mobile render, which is why A2 is flagged only for desktop width.
The `/games/` CLS of 0.076 is the footer being pushed down when `games.js` injects the cards. It is under the 0.1 line today and uses
76 percent of the budget with one placeholder card and no cover image; real cards will use more.
Home performance is outside this skill (hand to `seo-performance`), but a 5 s main-thread block can matter to agents that time out.

## 4. What already works

- `<html lang="en">`, one `<h1>` per page, descriptive titles and meta descriptions, canonical URLs on every page.
- Skip link is the first element in `<body>` (`href="#main"`, target `<main id="main">`), hidden by transform and shown on focus.
- Landmarks: `header` (banner), `nav aria-label="Primary"`, `main`, and on inner pages `aside aria-label="On this page"` and a top-level `footer` (contentinfo).
  Home also has `nav aria-label="Sections"`; two navs, two distinct labels.
- Every form control has a `<label for>`; name and email carry valid `autocomplete` tokens; `<select>`s and the textarea are labelled.
- Button and icon naming: the menu button has `aria-label`, `aria-controls` and a live `aria-expanded`; all inline SVGs on home and `/games/` (24 of 24) are `aria-hidden="true"`; the logo link has a name.
- Native elements throughout (`<a href>`, `<button>`, `<form>`); no `div onclick` widgets. Static check found no duplicate IDs, no broken in-page anchors, no missing internal link targets, and no `<img>` elements in the static HTML.
- Mobile nav is a real toggle: closed links are `visibility:hidden`, open state is announced via `aria-expanded`, links close it. No focus trap.
- Hero 3D canvas is decorative (`aria-hidden`), all hero text is real HTML. No canvas-only UI.
- Decorative layers (`.bg-glow`, `.bg-grid`, `.hero-fade`) are `pointer-events: none`; no consent banner, modal, CAPTCHA or interstitial.
- Breadcrumbs carry `aria-current="page"` in static HTML on inner pages.
- Privacy and Terms are fully server-rendered with `h2` per section and an `id` on each (`#data-deletion`, `#contact`, ...), a clean target for an agent.
- Real 404: `404.html` exists (and is `noindex`), so Cloudflare Pages, Netlify and GitHub Pages return a genuine 404 for unknown URLs. That keeps `/llms.txt` and `/.well-known/*` from turning into soft-404 200s (confirm after deploy).
- `robots.txt` is a valid file with a `Sitemap:` line; `sitemap.xml` lists all four indexable URLs and not the 404 page. `_headers` sets no `X-Robots-Tag`; the site has no login, auth wall or challenge page.
- Static JSON-LD (Organization with contact email, WebSite, WebPage, Service catalog, BreadcrumbList) states who the studio is and what it offers without any JS. (Schema detail: see `schema.md`.)
- A plain `mailto:` link to support@stonebuildgames.com is visible in the contact block and the footer, so an agent has a no-JS route to the studio.

## 5. Findings by priority

### P0

**A1. Games list is client-rendered only** (check id `server-rendered`; CLS dependency)
- Evidence: `games/index.html:95-97` ships `<div id="games-grid">` containing only a `<noscript>` apology. `js/games.js:44` fills it with `insertAdjacentHTML`.
  VideoGame JSON-LD is also JS-only (`games.js:46-69`) and only for `status: "live"`. Page meta description promises "Store links, genres, platforms and release status for every title".
  Without JS, `/games/` has an `h1`, one lead paragraph and a footer.
- Why it matters: many AI fetchers read raw HTML, and a rendered-tree agent still gets nothing if the script fails or is blocked. The placeholder is the only card now; the first real release puts every store link behind JS.
- Collateral: the injection causes the 0.076 CLS (section 3), and `h3` card titles sit directly under the `h1` (heading-order fail).
- Fix (no build step): ship the cards as static HTML, let JS replace them. Exact patch in section 8a. Alternative: a 30-line pre-deploy Node script that renders `games-data.js` into `games/index.html` between marker comments and emits the live-games JSON-LD, so there is one source of truth.
- Confirm: `curl -s https://stonebuildgames.com/games/ | grep -c 'game-card'` is at least 1; Lighthouse `cumulative-layout-shift` on `/games/` drops toward 0; `heading-order` passes.

**A2. Six section-dot links have no accessible name** (axe `link-name`, inside `agent-accessibility-tree`; target size)
- Evidence: `index.html:141-148`, `<a href="#services" data-label="Services"></a>` and five more. Text exists only as CSS generated content (`css/styles.css:387`, `content: attr(data-label)`, `opacity:0` until hover). axe reads DOM text, `aria-label`, `aria-labelledby` and `title`, not pseudo-elements, so `link-name` is expected to fail at desktop width. Local mobile run passed only because `.dots` is `display:none` at 1100px and below (`styles.css:394`).
  The dots are 10 x 10 px (`styles.css:386`), below the 24 x 24 px threshold visual agents use to drop targets.
- Fix: add `aria-label` to each link and a larger hit area. Exact markup and CSS in section 8b.
- Confirm: desktop Lighthouse run, `agent-accessibility-tree` passes.

**A3. robots.txt has no deliberate AI-purpose groups and no Content-Signal** (`robots-ai-groups`, `content-signal`; policy decision for the owner)
- Evidence: `robots.txt` is `User-agent: *` / `Allow: /` plus `Sitemap:`. Every training, search and user-triggered agent is allowed by default, and no preference is stated.
- Nothing is blocked and nothing private exists to protect, so this is a missing statement of intent, not an outage. Whether to allow training is the owner's decision; this review does not choose.
- Fix: pick one of three options in section 7. Content-Signal is a draft/policy with no confirmed effect (section 9).
- Confirm: `curl -s https://stonebuildgames.com/robots.txt` matches the file. If the zone is on Cloudflare, check that no managed robots.txt or AI-crawler block has been layered on top (see the WAF note below).

**WAF behaviour toward verified bots and signed agents: not tested** (pre-launch). The README recommends Cloudflare Pages. Zone-level bot settings
(AI Crawl Control, Bot Fight Mode, any "block AI bots" toggle, managed robots.txt) can block or rewrite agent traffic regardless of the file in the repo.
After deploy: review those settings, confirm no CAPTCHA or challenge on `/`, `/games/`, `/privacy-policy/`, `/terms/`, and check WAF logs.
Do not run `agentic_check.py --ua-matrix` without owner authorization.

### P1

**B1. No `/llms.txt`** (`llms-txt`; absence is informational)
- Cheap to add and it adds one counted Lighthouse audit. No consumer agent is publicly confirmed to read it, and Google Search ignores it. Proposed file in section 7.
- Confirm: `curl -sI https://stonebuildgames.com/llms.txt` returns 200 and a text type; Lighthouse `llms-txt` passes (H1, at least one Markdown link, 50+ characters).

**B2. Contact form is a mailto handoff with silent status** (manual review item, not measured)
- Evidence: `main.js:126-148` calls `e.preventDefault()` then `location.href = mailto:...`. Validation and success messages go to `<p id="form-note">` (`index.html:395`), which has no `role="status"` or `aria-live`, so a screen reader or agent gets no announcement. An agent cannot confirm the message was sent, because the send happens in an external mail client; in a headless or sandboxed browser nothing may happen at all. Email format is not validated beyond "non-empty".
- Fix now: `<p class="form-note" id="form-note" role="status">`. Keep the visible `mailto:` links (they are the reliable route). Later, when a hosted form endpoint replaces mailto, show an on-page confirmation that persists.

**B3. Disabled store badges are links to `#`** (`games.js:15-19`)
- Evidence: for a game with no store URL the badge renders as `<a href="#" aria-disabled="true" tabindex="-1">GET IT ON Google Play</a>`. The accessible name says "get it on Google Play" and the element is a link. Agents can follow it and land on the top of the page, or read it as an available store link. The first title (Android only, `playStore: ""`) already renders this badge.
- Fix: render a non-link with explicit text. Exact patch in section 8a.

**B4. Markdown delivery: absent** (`markdown-delivery`; opportunity, defer)
- Four pages; the two legal pages are long (about 15 KB each). Content negotiation needs a Worker or Pages Function (or a host feature) because Pages is static. `.md` mirrors are possible but double the maintenance. No consumer agent is publicly confirmed to send `Accept: text/markdown`.
- Recommendation: do not build this now. Revisit if the site grows past a handful of pages. If done later, serve `.md` alternates advertised by `<link rel="alternate" type="text/markdown">` and keep them content-equivalent.

### P2

**C1. Home page has no contentinfo landmark.** `index.html:399-423`: the `<footer>` sits inside `<section id="contact">` inside `<main>`, so it is not a `contentinfo` (HTML-AAM). Inner pages are fine (footer is a body-level `div.inner-footer-wrap > .container > footer`). Fix: move the footer after `</main>` using the same wrapper as inner pages, and check the last snap section visually. Do not add `role="contentinfo"` to the nested footer; axe `aria-allowed-role` (one of the 33 agentic rules) would likely flag it.

**C2. `aria-current` for the nav is JS-only.** `main.js:33-38` sets it on the Games link at runtime. Add it in `games/index.html:69` as `<a href="/games/" aria-current="page">Games</a>`. (Home has no current item by design; that is acceptable.)

**C3. `js/*` cache is 7 days, but the site promises same-day game updates.** `_headers` sets `Cache-Control: public, max-age=604800` for `/js/*`, which includes `games-data.js`. The home copy says "New titles appear here the day they go live" (`index.html:301`). A returning browser, including an agent browser profile, can show "In production" for up to a week after the store link goes live. Fix after A1 is done (becomes less important): on Cloudflare Pages add
```
/js/games-data.js
  ! Cache-Control
  Cache-Control: public, max-age=300, must-revalidate
```
or version the include (`/js/games-data.js?v=2`) on each change. The `!` detach syntax is Cloudflare Pages; verify with `curl -sI` after deploy. Netlify merges differently.

**C4. Home games block is static, and some copy overstates reality.**
- README says the home Games section updates from `games-data.js`; it does not (`index.html` does not load `games-data.js` or `games.js`, and the block at lines 280-293 is hand-written). When the first title ships, the home page will go stale.
- `index.html:299`: "Published under StoneBuild Games on Google Play and the App Store" (present tense, no game live, first title is Android-only per `games-data.js`).
- `index.html:162`: "mobile, PC and console"; meta description and JSON-LD say "Android, iOS and PC"; manifest says "mobile and PC". Agents quote page text verbatim. Make claims consistent and true (owner to confirm facts), for example "Each title is published under StoneBuild Games on its store listing" and drop "console" unless offered.

**C5. WebMCP: not warranted** (decision, no action). See section 6.

**C6. Below-the-fold content starts at opacity 0 and waits for scroll.** `main.js:69-96` uses `gsap.set(items, {opacity:0})` and `ScrollTrigger` (`start: 'top 70%'`). The CSS safety net (`.js.reveal-ready .reveal`) cannot override GSAP's inline styles. The accessibility tree and DOM are unaffected, and scrolling reveals everything, but a full-page screenshot or a vision agent that does not scroll sees blank sections. Not verified in a browser. Either accept it, or reveal at `start: 'top 95%'`, or skip hiding when the window loads taller than the page. Also note `html { scroll-snap-type: y mandatory }` with `scroll-snap-stop: always` at 1024 x 720 and up (`styles.css:115-116`); test an agent's small scroll steps live.

### P3

- **D1 Heading order** (confirmed failing by the local Lighthouse run, not in the agentic rule set). Home and inner pages: footer `h4` and the TOC `h4` follow an `h2`. `/games/`: cards use `h3` directly under `h1`. Fix: add `<h2 class="sr-only" id="games-list-title">Game list</h2>` at the top of the `/games/` list section and point `aria-labelledby` at it; change footer and TOC `h4` to `h3` and update `.site-footer h4` and `.toc h4` (`styles.css:346`, `391`). On home, the games block shows `h3 "Our first title"` before its section `h2`.
- **D2 Breadcrumbs** are `<ol aria-label="Breadcrumb">`. Wrap in `<nav aria-label="Breadcrumb">` so it is a navigation landmark.
- **D3 Marquee** (`index.html:319-323`): the technology list is duplicated for the loop and both copies are read; add `aria-hidden="true"` to the second set. `aria-label` on a plain `<div class="marquee">` names nothing (generic role); use `role="list"` + `role="listitem"` or drop the label.
- **D4 Store links** open `target="_blank"` with no "opens in new tab" cue; add visually hidden text.
- **D5 Feature card link** (`index.html:280`): `aria-label="See all StoneBuild games"` hides the visible status text ("In production", "Coming to Google Play") from the link's name. Use `aria-labelledby` pointing at the card heading, or drop the label.
- **D6 Mobile menu** does not close on Escape (`main.js:19-23`). Not a trap, but expected behaviour.
- **D7 Section dots** could expose the active one with `aria-current="location"` (optional line in section 8b).

## 6. WebMCP: not warranted

Recommendation: do not add WebMCP.
- There is no transaction and no API. The only form hands off to the visitor's mail client via `mailto:`; a tool would just prefill an email and the consequential step (send) happens outside the page.
- Absence of WebMCP is an opportunity, not a defect. The accessibility tree, a labelled form and a visible email address already cover the one task an agent might attempt here (contact the studio).
- Annotating the form with `toolname`/`tooldescription` would add a counted Lighthouse audit but gives nothing real to agents, and an incompletely annotated form scores 0.5 on `webmcp-schema-validity`. If done, annotate fully or not at all.
- Revisit only if the mailto handler is replaced by a hosted form or API (for example Formspree). Then one imperative tool, bound to the same submit path and marked consequential with a human confirmation step, is a P2 enhancement. Chrome only for the declarative form (P3).
- Status: W3C Community Group draft, Chrome origin trial M149 to M156 (secondary end date 2026-11-17), no ship milestone; WebKit opposes, Mozilla neutral. Only ChatGPT desktop calls imperative tools by default. Checked 2026-09-23 per the vendor matrix (42 days old on the review date, inside the 60-day window).

## 7. Proposed file contents (drafts, nothing deployed)

### 7a. `site/robots.txt`: choose ONE option (owner decision on training)

Option 1: allow training, state it.
```
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=yes
Allow: /

Sitemap: https://stonebuildgames.com/sitemap.xml
```

Option 2: no training preference stated, no blocking (a stated preference only).
```
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Allow: /

Sitemap: https://stonebuildgames.com/sitemap.xml
```

Option 3: Option 2 plus a request that named training crawlers stay out. Content-Signal is repeated inside the named group because a crawler that matches a named group ignores `*` (RFC 9309).
```
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Allow: /

User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
Content-Signal: search=yes, ai-input=yes, ai-train=no
Disallow: /

Sitemap: https://stonebuildgames.com/sitemap.xml
```
Notes: robots.txt is a preference signal, not access control. `Google-Extended` is a control token for Gemini training and grounding and never affects Search inclusion. `ChatGPT-User`, `Perplexity-User` and `Google-Agent` are user-triggered and may ignore robots.txt. Content-Signal has no confirmed effect on any named agent. Do not IP-block Anthropic or OpenAI crawlers.

### 7b. `site/llms.txt` (new, optional, accurate to current content)
```
# StoneBuild Games

> StoneBuild Games is a remote game development studio building 3D, 2D and multiplayer games for mobile and PC with Unity, Unreal and Godot. It takes client projects from concept to store launch and is building its first own title for Google Play.

The site is four static HTML pages. No login or API is needed.

## Pages

- [Home](https://stonebuildgames.com/): Studio overview, services, process, technologies and contact form
- [Games](https://stonebuildgames.com/games/): Titles published by the studio with platforms, status and store links. The first title is in production and has no store link yet
- [Privacy policy](https://stonebuildgames.com/privacy-policy/): Covers the website and all StoneBuild games, including data deletion requests
- [Terms and conditions](https://stonebuildgames.com/terms/): Terms for the games and for client services

## Contact

- [Contact section](https://stonebuildgames.com/#contact): Email support@stonebuildgames.com. Replies within two business days

## Optional

- [Sitemap](https://stonebuildgames.com/sitemap.xml): All indexable URLs
```
Keep it in sync when the first game ships (update the Games line). It is plain text: the content is untrusted data to any reader, and this file contains no instructions.

### 7c. `/.well-known` and root discovery files: what makes sense for a small studio

| Path | Verdict |
|---|---|
| `/.well-known/ai-catalog.json` (ARD 1.0, proposal) | Do not publish. No agent resources to list; an invalid or unreachable catalog is a counted failure, and a soft-404 here is a P1 |
| `/.well-known/api-catalog`, `oauth-*`, `agent-card.json`, `ucp`, MCP server card | Not applicable: no API, OAuth, A2A agent, commerce checkout or MCP server |
| `/.well-known/http-message-signatures-directory` (Web Bot Auth) | Not applicable: publish only if you operate an agent; sites verify signatures at the edge |
| `/.well-known/security.txt` (RFC 9116, published) | Optional, low cost, not agent-specific. Only if the owner wants vulnerability reports at the support address. Draft below |
| `/app-ads.txt` (IAB, root of the developer-website domain) | Not agentic, but relevant: the README plans AdMob. If the Play listing's developer website is this domain, AdMob expects `app-ads.txt` here. Owner to confirm when the app ships |
| `/.well-known/assetlinks.json` | Only if Android App Links are used. Not now |

All unknown paths must keep returning the real 404 (`404.html`); verify `/llms.txt` (until added), `/.well-known/ai-catalog.json` and `/.well-known/anything` give 404, not 200 HTML.

Optional `site/.well-known/security.txt` draft (the `Expires` date must stay under one year ahead; renew it):
```
Contact: mailto:support@stonebuildgames.com
Expires: 2027-10-31T23:59:59.000Z
Preferred-Languages: en
Canonical: https://stonebuildgames.com/.well-known/security.txt
```

## 8. Concrete code patches (drafts)

### 8a. `/games/` pre-render and store badge (fixes A1, B3, part of D1)

`site/games/index.html`, replace lines 93-97 (the `<section>`, its container and the grid). Put the static card inside the grid (this matches today's `games-data.js` entry, regenerate or hand-edit whenever that file changes):
```html
<section class="page-body" aria-labelledby="games-list-title">
  <div class="container">
    <h2 id="games-list-title" class="sr-only">Game list</h2>
    <div class="games-grid" id="games-grid">
      <article class="card game-card" id="first-title" data-prerendered>
        <div class="game-cover">
          <div class="art art-forge" aria-hidden="true"><span class="stone s1"></span><span class="stone s2"></span><span class="stone s3"></span><span class="stone s4"></span></div>
          <div class="label"><div><span class="status">In production</span><h3 style="margin-top:10px">Our first title</h3><p>Currently in production</p></div></div>
        </div>
        <div class="body">
          <div class="meta"><span class="tag">To be announced</span><span class="tag">Android</span></div>
          <p>We are building our first game right now. Screenshots, a trailer and store links will appear here the day it goes live on Google Play.</p>
          <div class="store-row"><span class="store-badge disabled"><span><small>GET IT ON</small>Google Play <span class="sr-only">(not available yet)</span></span></span></div>
        </div>
      </article>
    </div>
```
(Remove the `<noscript>` apology; the real content is now in the HTML.)

`site/js/games.js`, three edits:
```js
// after: if (!grid) return;
const prerendered = grid.querySelectorAll('[data-prerendered]');

// card(): replace   <article class="card game-card reveal" id=
//         with      <article class="card game-card${prerendered.length ? '' : ' reveal'}" id=

// line 44: replace the insert with
prerendered.forEach((n) => n.remove());
grid.insertAdjacentHTML('afterbegin', games.map(card).join(''));

// badge(): replace the whole function body (lines 15-19)
function badge(href, icon, small, label) {
  const inner = `${icon}<span><small>${small}</small>${label}`;
  return href
    ? `<a class="store-badge" href="${esc(href)}" target="_blank" rel="noopener">${inner}<span class="sr-only"> (opens in a new tab)</span></span></a>`
    : `<span class="store-badge disabled">${inner} <span class="sr-only">(not available yet)</span></span></span>`;
}
```
The replacement renders identical markup, so no visual change or extra layout shift; the static copy is only the no-JS fallback.

### 8b. Section dots (fixes A2)

`site/index.html:141-148`:
```html
<nav class="dots" aria-label="Sections">
  <a href="#top" data-label="Intro" aria-label="Go to Intro section" class="is-active"></a>
  <a href="#services" data-label="Services" aria-label="Go to Services section"></a>
  <a href="#process" data-label="Process" aria-label="Go to Process section"></a>
  <a href="#games" data-label="Games" aria-label="Go to Games section"></a>
  <a href="#why" data-label="Why us" aria-label="Go to Why us section"></a>
  <a href="#contact" data-label="Contact" aria-label="Go to Contact section"></a>
</nav>
```
`site/css/styles.css`, add near line 386 (24 px hit area without changing the dot size):
```css
.dots { gap: 18px; }
.dots a::before { content: ""; position: absolute; inset: -7px; }
```
Optional `site/js/main.js`, inside the IntersectionObserver callback (line 48): `dots.forEach((d) => d.removeAttribute('aria-current'));` and after line 50: `(byId.get(id) || dots[0]).setAttribute('aria-current', 'location');`

### 8c. Smaller edits
- `site/index.html:395`: `<p class="form-note" id="form-note" role="status">`
- `site/games/index.html:69`: `<a href="/games/" aria-current="page">Games</a>`
- `site/index.html:322`: add `aria-hidden="true"` to each `.marquee-item` in the duplicate (second) set.

## 9. Access policy (three purposes, never merged)

| Purpose | Tokens | Current state |
|---|---|---|
| Training | GPTBot, ClaudeBot, Google-Extended | **Allowed by default, no stated preference.** `User-agent: *` / `Allow: /`; no Content-Signal. Decision pending (A3) |
| Search | OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot, Bingbot | **Allowed.** No `noindex`, no `X-Robots-Tag`; page robots meta is `index, follow, max-image-preview:large`; sitemap declared |
| User-triggered | ChatGPT-User, Claude-User, Perplexity-User, Google-Agent | **Allowed by robots.txt; nothing private to protect** (static public site, no accounts). ChatGPT-User, Perplexity-User and Google-Agent may ignore robots.txt regardless; Claude-User honours it. WAF treatment **not tested** (pre-launch) |

## 10. Standards status (draft or proposal, with check date)

Dates from `vendor-matrix.md`, last full check **2026-09-23** (42 days before this review; refresh before quoting after 2026-11-22).

| Item | Status |
|---|---|
| WebMCP | W3C Web Machine Learning Community Group draft, not a W3C Standard. Chrome origin trial M149 to M156 (end date 2026-11-17 is secondary-sourced). WebKit opposes, Mozilla neutral. Checked 2026-09-23 |
| Content-Signal | Cloudflare CC0 policy (launched 2025-09-24). IETF individual draft expired 2026-04-04. No Google statement found; not in Google's robots.txt spec. A stated preference with no confirmed effect. Checked 2026-09-23 |
| ai-catalog.json / ARD 1.0 | Proposal (agenticresourcediscovery.org). Validated by Lighthouse 13.5. Checked 2026-09-23 |
| MCP Server Card | SEP-2127 open and unmerged (2026-09-12). Checked 2026-09-23 |
| Web Bot Auth | `draft-ietf-webbotauth-httpsig-protocol-00` (2026-09-01). Sites verify at the edge; not applicable to publish. Checked 2026-09-23 |
| llms.txt | Community specification (llmstxt.org), not a standard. Counted by Lighthouse; Google Search ignores it. No consumer agent is publicly confirmed to read it |
| Markdown via `Accept: text/markdown` | No primary source shows any consumer agent sending it |
| Lighthouse | 13.5.0 as of 2026-09-23; Agentic Browsing category "still under development and subject to change" |

No ranking, citation or traffic effect is claimed or implied for any item in this report.

## 11. Not tested, verify after deploy

1. Lighthouse Agentic Browsing X/N, mobile and desktop, home and `/games/` (commands in section 3 and below).
2. Agent-UX heuristic: `"$HOME/.claude/skills/seo/scripts/claude-seo" run agent_ux_check.py https://stonebuildgames.com/ --json`.
3. `agentic_check.py https://stonebuildgames.com/ --json` (server-rendered, robots groups, llms.txt, 404 behaviour, `/.well-known` paths).
4. WAF and bot settings on the host (section 5, P0 note). Real 404 on `/llms.txt` and `/.well-known/ai-catalog.json` until files are added.
5. Served robots.txt equals the repo file (no host-injected groups).
6. Live rendering: scroll-snap with small agent scroll steps, below-fold fade-in with a non-scrolling full-page screenshot, mobile menu open and close.
7. `Content-Type` of `/llms.txt` is a text type with UTF-8.

## 12. Structured findings for `audit-data.json` (AI Search Readiness)

```json
{
  "name": "AI Search Readiness",
  "score": 67,
  "what_works": [
    "Fully server-rendered home, privacy and terms pages with one h1, labelled landmarks, skip link and native controls",
    "Every form field labelled with valid autocomplete tokens; menu button has name and live aria-expanded; all decorative SVGs hidden",
    "Real 404 page, sitemap declared in robots.txt, no noindex or X-Robots-Tag, no CAPTCHA, consent layer or interstitial",
    "Static JSON-LD for Organization, WebSite, Service and BreadcrumbList; visible mailto link as a no-JS contact route"
  ],
  "findings": [
    {
      "title": "Games list is built in the browser only",
      "severity": "High",
      "description": "games/index.html ships an empty #games-grid with a noscript apology; js/games.js:44 injects the cards and js/games.js:46-69 injects VideoGame JSON-LD. Agents that read raw HTML get no titles, platforms, statuses or store links once a game ships. The injection also causes CLS 0.076 on /games/ in the existing local Lighthouse 12.8.2 run (footer shift) and puts h3 cards directly under the h1.",
      "recommendation": "Ship the game card as static HTML in games/index.html with data-prerendered and let games.js replace it with identical markup, or add a small pre-deploy script that renders games-data.js into the HTML. Add a visually hidden h2 above the list."
    },
    {
      "title": "Six section-dot links on the home page have no accessible name",
      "severity": "High",
      "description": "index.html:141-148 links have only data-label; the text is CSS generated content (styles.css:387) so axe link-name is expected to fail at desktop width in Lighthouse agent-accessibility-tree. Dots are 10x10 px. Mobile run does not evaluate them because .dots is display:none at 1100px and below. Predicted, not measured.",
      "recommendation": "Add aria-label=\"Go to <Section> section\" to each link and enlarge the hit area to 24px with a ::before pseudo-element. Re-run Lighthouse at desktop width."
    },
    {
      "title": "robots.txt states no policy for AI training, search or user-triggered agents",
      "severity": "Medium",
      "description": "robots.txt contains only User-agent: * / Allow: / and a Sitemap line. Nothing is blocked and no preference is declared. Content-Signal is a draft/policy with no confirmed effect.",
      "recommendation": "Owner decides the training policy, then adopt one of the three robots.txt options in findings/agentic.md section 7a, repeating Content-Signal inside any named group."
    },
    {
      "title": "No llms.txt",
      "severity": "Low",
      "description": "Absence is informational. A valid /llms.txt adds one counted Lighthouse audit; no consumer agent is publicly confirmed to read it and Google Search ignores it.",
      "recommendation": "Add site/llms.txt using the draft in findings/agentic.md section 7b and keep it in sync when the first game ships."
    },
    {
      "title": "Contact form is a mailto handoff with silent status messages",
      "severity": "Medium",
      "description": "main.js:126-148 prevents submit and sets location.href to a mailto: URL; #form-note has no role=status, and an agent cannot confirm that a message was sent.",
      "recommendation": "Add role=status to #form-note, keep the visible mailto links, and show a persistent on-page confirmation if a hosted form endpoint replaces mailto."
    },
    {
      "title": "Disabled store badges are links to #",
      "severity": "Medium",
      "description": "games.js:15-19 renders a missing store URL as <a href=\"#\" aria-disabled=\"true\">GET IT ON Google Play</a>, which reads as an available store link.",
      "recommendation": "Render a non-link span with visually hidden text '(not available yet)' and add a new-tab cue to real store links."
    },
    {
      "title": "Home footer is inside main, so there is no contentinfo landmark",
      "severity": "Low",
      "description": "index.html:399-423 nests the footer in section#contact within main. Inner pages are correct.",
      "recommendation": "Move the footer after </main> with the inner-page wrapper and check the last snap section; do not add role=contentinfo to the nested footer."
    },
    {
      "title": "games-data.js is cached for 7 days despite a same-day update promise",
      "severity": "Low",
      "description": "_headers applies max-age=604800 to /js/*, which includes js/games-data.js; the home copy says new titles appear the day they go live.",
      "recommendation": "Give /js/games-data.js a short max-age with must-revalidate (Cloudflare Pages: detach Cache-Control then set it) or version the script URL."
    },
    {
      "title": "Home copy and the home Games block are out of step with the data",
      "severity": "Low",
      "description": "index.html:299 says titles are published on Google Play and the App Store while no game is live and the first title is Android-only; index.html:162 mentions console while other metadata says Android, iOS and PC. The home games block is hand-written and will not follow games-data.js despite the README.",
      "recommendation": "Make claims consistent and true, and either generate the home block from the same data or note that it must be edited by hand."
    },
    {
      "title": "WebMCP is not warranted",
      "severity": "Info",
      "description": "The only form hands off to a mail client; there is no transaction or API. Absence is an opportunity, not a defect. WebMCP is a W3C Community Group draft (checked 2026-09-23).",
      "recommendation": "Do not add WebMCP now. Revisit if the form moves to a hosted endpoint."
    },
    {
      "title": "Heading order and minor semantics",
      "severity": "Low",
      "description": "Lighthouse 12.8.2 heading-order fails on / and /games/ (footer h4 after h2/h3; cards h3 under h1). Breadcrumbs are an ol without nav; marquee items are read twice; aria-current for the nav is set by JS only.",
      "recommendation": "Apply the D1-D7 fixes in findings/agentic.md section 5 (P3) and section 8c."
    }
  ]
}
```
