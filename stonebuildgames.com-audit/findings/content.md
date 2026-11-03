# Content Quality / E-E-A-T / On-Page Review: stonebuildgames.com (pre-launch)

- Audit date: 2026-11-04
- Source: static HTML in `site/`, read from disk. No live fetch; render_page.py not used.
- Pages: `/` (index.html), `/games/` (games/index.html + js/games-data.js + js/games.js), `/privacy-policy/`, `/terms/`. 404.html was checked only in passing.
- Tools: custom HTML text extraction (main content only: header, nav, footer, aside, script, svg excluded), `content_quality.py` on the extracted text, `metadata_template.py --pairs-file`, a Unicode scan, a Flesch readability script, and the existing Lighthouse JSON in `stonebuildgames.com-audit/lighthouse/`.
- Constraint: the studio has no shipped games, clients or testimonials yet. None of the recommendations below involve inventing reviews, numbers, logos or case studies. Placeholders in [brackets] must be filled with true facts or left out.

## Scores

| Metric | Score | Notes |
|---|---|---|
| Content quality (overall) | 52 / 100 | The writing is clean and readable with no filler. The score is held down by very low E-E-A-T, a thin /games/ page, and a few present-tense claims that are not true yet |
| On-page SEO | 68 / 100 | Unique titles, descriptions and canonicals, valid JSON-LD, Lighthouse SEO 100. Weaker on title/description length, an H1 with no topic keyword, heading order, missing coverage for the target queries, and one entity bug in JSON-LD |
| E-E-A-T composite (internal weights) | 33 / 100 | Experience 20, Expertise 45, Authoritativeness 10, Trust 50 |
| AI citation readiness | 45 / 100 | One good definitional sentence and quotable process timings. No facts about who, where or when, no Q&A content, the game list is JS-only, and inline text runs together when extracted |

### E-E-A-T breakdown (weights are this skill's model; Google publishes no numeric weights)

| Factor | Weight | Score | Evidence |
|---|---|---|---|
| Experience | 20% | 20 | No first-hand proof anywhere: no screenshots, dev log, prototype, game-jam entry or named project. The only game card says "Our first title / In production / Genre: To be announced". The specific process durations ("Week 1", "2 to 3 weeks", "Two-week sprints") are the only experience-flavoured detail. |
| Expertise | 25% | 45 | The vocabulary is correct and specific (vertical slice, netcode, PBR, data safety forms, IDFA / Advertising ID opt-out paths, Play Games Services). There is no named person and no credentials, so the expertise can't be attributed to anyone. |
| Authoritativeness | 25% | 10 | Expected before launch: no profiles, no `sameAs`, no press, no store developer page, no external references. |
| Trustworthiness | 30% | 50 | Positives: contact email on every page, a stated 2-business-day reply, a detailed privacy policy with a data-deletion procedure and 30-day SLA, "you own everything" IP terms, transparent budget ranges in the form, last-updated dates on legal pages. Negatives: no legal entity, country or address anywhere; governing law is left unspecified; some present-tense claims are false (see C2); the privacy policy mentions a cookie notice that doesn't exist and leaves out Google Fonts; the contact form's "Send message" button doesn't send anything (it opens a mailto). |

## Per-page summary

| Page | Title (chars) | Meta description (chars) | H1 | Main words | Readability | Verdict |
|---|---|---|---|---|---|---|
| `/` | "StoneBuild Games \| Game Development Studio for 3D, 2D & Multiplayer Games" (73, likely truncated) | 190 (too long; will truncate around 155-160) | "We build games people can't put down." (no topic keyword) | 663 (486 prose) vs 500 homepage floor | FRE 66.6, FK grade 7.3, avg sentence 13.5 words | Passes the homepage floor. Each service gets only about 20-25 words, and this page is the only commercial URL |
| `/games/` | "Our Games \| StoneBuild Games" (28, no topic) | 141. Promises "Store links, genres, platforms and release status for every title", none of which exist | "Games by StoneBuild" | 53 static, about 95 after JS renders the single placeholder card | n/a | Thin. Placeholder only. The description doesn't match the page |
| `/privacy-policy/` | "Privacy Policy \| StoneBuild Games" (33) | 173 (slightly long) | "Privacy Policy" | 1,061 | FRE 54.8, FK 9.0 | Good structure. Two accuracy gaps (M1) |
| `/terms/` | "Terms & Conditions \| StoneBuild Games" (37) | 169 (slightly long) | "Terms & Conditions" | 989 | FRE 58.5, FK 9.3 | Good structure. Governing law is unspecified. JSON-LD entity bug (L1) |

Tool output:
- content_quality.py: home overall 84 (filler 0, ai_pattern 0, density 0.554); games 70 (flags: low-density, thin-content; density 0.189); privacy 86; terms 86.
- metadata_template.py site check: site_risk low, templated_ratio 0.0, shared_cta_phrases none. Three pages have a low-severity `brand_suffix_in_description` flag (games, privacy, terms). No `templated_metadata`, `description_echoes_title` or `description_duplicates_title`. Naming the brand in a legal-page description is reasonable. The flag is informational only.
- Lighthouse (local): SEO 100 on home and games, Accessibility 98. `heading-order` fails on both. `label-content-name-mismatch` fails on the brand link.

## Invisible / non-ASCII character scan

Every HTML, JS, manifest, sitemap and robots file was scanned codepoint by codepoint.
- None found: zero-width characters (U+200B/C/D, U+2060, U+FEFF), BOMs, NBSP, soft hyphens, bidi controls, or any other Cf/Zs/Cc format characters. No numeric entities that encode invisible characters either. The only entity used is `&amp;`.
- Visible non-ASCII, all legitimate under the UTF-8 charset:
  - U+00B7 middle dot: separators on all pages, e.g. index.html:159, 171-172, footer.
  - U+00A9 copyright sign: footer.
  - U+2014 em dash x5 in privacy-policy/index.html lines 132-136 (third-party list).
  - U+2192 arrow x5 in privacy-policy/index.html lines 143-144 (opt-out paths).
  - U+2014 em dash in js/main.js:143, inside the mailto subject the user sees ("Project inquiry: 3D game — Name").
  - Em/en dash and multiplication sign in JS comments only.
- Straight ASCII quotes and apostrophes are used throughout, with no curly quotes.
- Verdict: clean. Swapping the em dashes for colons is purely a style choice with no SEO effect.

## AI-typical phrasing review (QRG Sept 2025: generic phrasing, lack of specificity, no first-hand signals)

content_quality.py matched no AI patterns. Manually, the copy is tight but generic: almost every claim could sit on any studio's site and none can be checked. Stock agency or AI-flavoured constructions:
- "We obsess over those details so your players never notice them." (index.html:318)
- "...are design goals, not afterthoughts." (index.html:329) and "...so launch day is not a surprise." ("X, not Y" framing)
- "No black boxes." (process lead), "Solid foundations, built to last" (H2), "end to end" (H2), "We plug in wherever you are" (index.html:184)
- "Clear contracts, clear IP, no lock-in." and frequent rule-of-three lists
- "industry-standard tools and services" (privacy section 4)
- "We build games people can't put down." Unsupported while nothing has shipped

This is not a penalty risk in itself. AI or templated copy is fine if it shows real E-E-A-T. The problem is that the site has no specifics to back the claims. See H5.

---

## Prioritized findings

### CRITICAL

**C1. No identifiable people, legal entity or location (Trust / E-E-A-T)**
Evidence:
- There is no About or team section and no named person anywhere on the site.
- Contact says only "Remote studio, working with clients worldwide" (index.html:367).
- The privacy section 13 and terms section 18 Contact blocks list only "StoneBuild Games" plus an email.
- Terms section 16 (terms/index.html:152): "governed by the laws of the jurisdiction in which StoneBuild Games is established". No jurisdiction is named.
- The Organization JSON-LD has no `legalName`, `founder`, `address`, `foundingDate` or `sameAs`.
- Meanwhile the form asks for budgets up to "$50k+".

Fix, using real facts only:
- Add a "Who we are" block to the home page (before Contact) or a new `/about/` page:
  > `<h2>Who we are</h2><p>StoneBuild Games is a remote game development studio founded in [year] by [Full name], [true one-line background: role, engines used, years of experience, past projects or game jams if any]. [Legal entity name] is registered in [country].</p>`
- Include a real photo, plus LinkedIn, GitHub, ArtStation or itch.io links if they exist.
- Put the legal entity and country in the footer, privacy sections 1 and 13, and terms sections 16 and 18. Name the governing-law jurisdiction.
- Mirror these facts in the Organization schema: `legalName`, `foundingDate`, `founder` (Person with `sameAs`), `address.addressCountry`, `sameAs`.

**C2. Present-tense claims that are not true yet**
Evidence:
- index.html:297 says "We ship our own titles too. Every StoneBuild game is made with the pipeline we sell...".
- index.html:299 says "Published under StoneBuild Games on Google Play and the App Store".
- The only title is "In production", and it is Android-only (games-data.js: `platforms: ["Android"]`, card text "Coming to Google Play").
- The hero lead (index.html:162) says "for mobile, PC and console". Console appears nowhere else: the hero stats say "Android · iOS · Steam", the meta says "Android, iOS and PC", and the privacy policy says "mobile, PC and web".

A reader can disprove these claims with one click to /games/.

Replacements:
- index.html:162:
  > "StoneBuild Games is a game development studio building 3D, 2D and multiplayer games for Android, iOS and PC. We take games from the first sketch to store launch, and keep updating them after."

  Only keep "console" if you are a registered developer with Sony, Nintendo or Microsoft.
- index.html:297:
  > "We also make our own games. Our first title is in production now, built with the same pipeline we use for client work: tested on real devices, careful with player data and supported after launch."
- index.html:299:
  > "Our first title will be published under StoneBuild Games on Google Play"

### HIGH

**H1. /games/ is thin, and its metadata promises content that isn't there**
Evidence:
- 53 words of static main content, about 95 after JS renders one placeholder card (genre "To be announced").
- The meta and og descriptions promise "Store links, genres, platforms and release status for every title".
- The callout says "Want a game like these..." (games/index.html:99) when there are none.
- games.js:17/27 renders a disabled "GET IT ON Google Play" badge with `href="#"`. Google Play's badge guidelines expect the badge to link to a real listing.

Fix: choose one of these until launch.
- (a) Preferred: set `<meta name="robots" content="noindex, follow">` (games/index.html:10) and remove `/games/` from sitemap.xml. Revert both on launch day.
- (b) Turn the page into a real development log with dated entries, work-in-progress screenshots or GIFs, the engine and target devices, and what you've learned. That is genuine first-hand Experience content.

Either way:
- Hide store badges when the URL is empty: in games.js, return `''` from `badge()` when `href` is falsy.
- Title (games/index.html:6): "Our Games: First Title in Production | StoneBuild Games" (55)
- Description (line 7): "Our first game is in production for Android. Screenshots, a trailer and the Google Play link will be posted here the day it launches." (133)
- Lead (line 89): "Our first game is in production for Android. Every title we publish will be listed here with its platforms, status and store links on the day it goes live."
- Callout (line 99): "Want a game built for your brand or idea? We build games for clients with the same team and pipeline."

**H2. Home title and meta description are too long**
- Title is 73 characters (index.html:6). Replace with:
  > "3D & Mobile Game Development Studio | StoneBuild Games" (54; write `&amp;` in HTML)
- Meta description is 190 characters (index.html:7). Replace with:
  > "Game development studio building 3D, 2D and multiplayer games for Android, iOS and PC in Unity, Unreal and Godot. From prototype to store launch." (145)
- Update the WebPage JSON-LD `name` and `description`, `og:title` and `twitter:title` to match.

**H3. Home H1 has no topic keyword**
index.html:161 reads "We build games people can't put down." Keep the tagline and add a keyword-bearing kicker inside the H1:

> `<h1 id="hero-title" class="reveal"><span class="h1-kicker">3D &amp; mobile game development studio</span> We build games people <span class="gradient-text">can't put down.</span></h1>`

Style `.h1-kicker` small, like the eyebrow. Optionally soften the superlative until a title has shipped.

**H4. Target queries are barely covered, and one URL carries every service**
Phrase counts across all visible text:

| Phrase | Count |
|---|---|
| "game development studio" | 1 (plus title/meta) |
| "3D game development" | 1 (a card H3) |
| "mobile game development" | 0 |
| "Unity game development" | 0 ("Unity" appears only as tags and in the marquee) |
| "company" | 0 |

Each service card is about 20 words.

Fix:
- Short term, edit naturally without stuffing. Services lead (index.html:184):
  > "Bring an idea, a prototype or a live game. We are a full-cycle game development company building mobile games for Android and iOS and 3D games for PC in Unity, Unreal Engine or Godot, and we take each one to a polished, store-ready release."
- Rename card 03 to "Mobile, 2D & Casual Games".
- Add an FAQ (see M6). Its engine question covers "Unity game development" naturally.
- Medium term: create `/services/mobile-game-development/`, `/services/unity-game-development/` and `/services/3d-game-development/`, but only when each can carry 800+ words of specific, true content: scope, deliverables, engine trade-offs, what affects cost, a process tailored to that service, and an FAQ. Thin pages built to grab keywords (doorway pages) would hurt rather than help.
  - Suggested titles: "Mobile Game Development Services | StoneBuild Games" (51), "Unity Game Development Services | StoneBuild Games" (50).
- Be realistic: head terms like "game development company" are very competitive. Without shipped work, expect long-tail and brand queries first.

**H5. Generic copy with no first-hand evidence**
The copy ranks low on specificity (see the AI-phrasing review above). You can add evidence that doesn't depend on shipped games or clients:
- Name the actual test devices you own and the frame-rate targets you hold. For example, replace "Stable frame rates on mid-range Android devices" with "We profile every build on [real device list] and hold [N] fps", using only true values.
- Publish a real sample changelog from your own project.
- State which engine and stack the first title uses.
- Describe the hero 3D scene as what it is (a real-time three.js scene built by the studio). It is the one piece of visible craft on the site.
- Rewrite the stock lines quoted in the phrasing review using these specifics.

### MEDIUM

**M1. Privacy policy accuracy**
- privacy-policy/index.html:115 refers to "the Site's cookie notice". No cookie notice exists.
- Every page loads Google Fonts from fonts.googleapis.com and fonts.gstatic.com (index.html:31-33 and the same lines on the inner pages), which sends visitors' IPs to Google. The policy says only that hosting logs are kept.

Fix: self-host the two fonts (this also helps performance) and delete the cookie-notice clause. If you keep Google Fonts, use:
> "The Site loads fonts from Google Fonts, so your browser sends your IP address to Google when a page loads (see the Google Privacy Policy). The Site does not set advertising or analytics cookies. If we add analytics, we will update this policy first."

**M2. Game list only exists after JS runs, and the home teaser can go stale**
- /games/ cards are injected by games.js. Non-rendering crawlers, which includes most AI crawlers, see only the 53-word shell and a `<noscript>` "Enable JavaScript" message.
- games-data.js:4 claims the home "Games" section is generated from the data file, but index.html:277-309 is hardcoded. At launch, the home page will still say "In production / Coming to Google Play".

Fix: pre-render the card HTML into games/index.html, either by hand or with a build step, and keep JS for enhancement only. Then either drive the home teaser from the same data or fix the comment and add a launch checklist item.

**M3. Text runs together when extracted (AI-citation hygiene)**
Adjacent inline elements have no whitespace between them, so extraction yields "UnityUnrealGodot", "PBRShadersOptimization", "NetcodePhotonFirebase", "Full-cycleIdea to launch to LiveOps", "Emailsupport@stonebuildgames.com" and "Response timeWithin 2 business days".

Fix:
- Mark up tags as `<ul class="tags"><li>`, or put a space or newline between the `<span class="tag">` elements.
- Add a space between `<b>` and the following `<span>` in the stats and contact lines.
- The marquee repeats the full technology list for its animation loop. Add `aria-hidden="true"` to the second copy, and give the wrapper `role="region"` (or drop the `aria-label` on the plain div).

**M4. Heading hierarchy**
Lighthouse `heading-order` fails on home (footer `<h4>` after `<h3>`) and on games (the card `<h3>` comes straight after the `<h1>`). On home, H3 "Our first title" (index.html:288) appears in the DOM before its section H2 (line 296). The TOC "On this page" on the legal pages is an `<h4>` after `<h3>`.

Fix:
- Change the footer column titles and the TOC title to `<p class="footer-title">` (or a styled `<h2>`).
- On /games/, add `<h2>Titles in development</h2>` above the grid, or render card titles as `<h2>`.
- On home, make the feature-card title a `<p>` or move the copy column first in the DOM.

**M5. CTA clarity and friction**
- "Send message" (index.html:392) doesn't send. It opens a mail client, so webmail users get nothing. The note on line 395 explains this, but the button label promises otherwise. Either connect a real form endpoint or rename the button to "Open email draft" / "Email us".
- Sales leads go to `support@`. A `hello@` or `projects@` address, if you create one, signals that this is a business inbox.
- The hero's secondary CTA "Explore our games" (index.html:167) leads to the placeholder page. Until launch, change it to "See how we work" linking to `#process`.

**M6. Add Q&A and definitional passages for AI citation**
Add an FAQ section to the home page with question headings, answered from facts the site already states:
- "How long does a game prototype take?" (2 to 3 weeks after a 1-week discovery)
- "How do you work during production?" (two-week sprints, playable build plus changelog each sprint)
- "Do I own the source code and store accounts?" (yes)
- "What budget do I need?" (explain what your existing ranges typically cover, truthfully)
- "Should I use Unity, Unreal or Godot for my game?" (your real engineering opinion; this is the natural home for "Unity game development")

FAQPage markup is optional. Since August 2023, Google shows FAQ rich results only for authoritative government and health sites. The value here is extraction and answer quality, not a SERP feature. Also add the "Who we are" facts from C1: founded year, country and founder are what AI answers quote.

### LOW

- **L1.** terms/index.html:39: the BreadcrumbList `"name": "Terms &amp; Conditions"`. HTML entities are not decoded inside `<script type="application/ld+json">`, so the literal "&amp;" becomes the breadcrumb name. Change it to `"Terms & Conditions"`. All other JSON-LD blocks parse as valid JSON.
- **L2.** Trim the legal-page descriptions:
  - Privacy (line 7): "How we collect, use and protect data in our games and on this website: third-party SDKs, ads, children's privacy, your rights and data deletion." (144)
  - Terms (line 7): "Terms for playing our games and using this website: licence, in-app purchases, player conduct, intellectual property and limitation of liability." (145)
- **L3.** The footer "Games" column contains Privacy policy and Terms. Rename it "Legal" or split it. On home, the `<footer>` sits inside `<main>` (index.html:399), so it isn't exposed as a contentinfo landmark. Move it after `</main>` the way the inner pages do.
- **L4.** The brand link `aria-label="StoneBuild Games home"` doesn't match its visible text "StoneBuildGames" (Lighthouse label-content-name-mismatch). Add a space between the brand-name spans and drop the aria-label, or make the label start with the visible text.
- **L5.** 404.html combines `noindex` with `canonical` to /404.html. Remove the canonical.
- **L6.** All sitemap `lastmod` values are the build date. Going forward, only change `lastmod` when a page's content actually changes.
- **L7.** The em dashes and arrows (privacy-policy lines 132-136 and 143-144, main.js:143) are fine. Change them only if the team prefers to avoid the "em-dash AI tell" stereotype.

## What is already good (keep)
- Titles, descriptions and canonicals are unique on every page. robots.txt and sitemap.xml are correct. The Organization, WebSite, WebPage, Service and BreadcrumbList JSON-LD is valid apart from L1.
- Body copy reads well: home is at FK grade 7.3, with short sentences and no filler.
- The process section has specific, quotable durations.
- The privacy policy is concrete: device opt-out paths, a deletion procedure with a 30-day SLA, 24-month retention, named SDKs.
- The terms are clear about virtual items, refunds and client-services carve-outs.
- Legal pages show "Last updated" dates. Breadcrumbs appear on inner pages.
- "Start a project" is used consistently as the CTA.
- No invisible Unicode was found.

## Structured findings (Content Quality category, for audit-data.json)

```json
{
  "category": "Content Quality",
  "scores": { "content_quality": 52, "on_page": 68, "eeat": 33, "eeat_breakdown": { "experience": 20, "expertise": 45, "authoritativeness": 10, "trustworthiness": 50 }, "ai_citation_readiness": 45 },
  "metadata_template": { "site_risk": "low", "templated_ratio": 0.0, "shared_cta_phrases": {}, "secondary_flags": ["brand_suffix_in_description: /games/, /privacy-policy/, /terms/ (low)"] },
  "unicode_scan": { "invisible_or_zero_width": 0, "bom": false, "visible_non_ascii": ["U+00B7", "U+00A9", "U+2014", "U+2192"] },
  "findings": [
    { "id": "C1", "severity": "critical", "page": "/ , /privacy-policy/, /terms/", "issue": "No named people, legal entity, country or address; governing law unspecified; Organization schema lacks founder/address/sameAs", "evidence": "index.html:367; terms/index.html:152; Organization JSON-LD" },
    { "id": "C2", "severity": "critical", "page": "/", "issue": "Present-tense claims not yet true (published on Google Play and App Store, ship our own titles, console)", "evidence": "index.html:162, 297, 299; games-data.js platforms [Android], status in-production" },
    { "id": "H1", "severity": "high", "page": "/games/", "issue": "Thin placeholder page (53 static / ~95 rendered words); description promises store links and genres that do not exist; disabled Play badge href=#", "evidence": "games/index.html:7, 89, 99; games.js:17, 27" },
    { "id": "H2", "severity": "high", "page": "/", "issue": "Title 73 chars, meta description 190 chars", "evidence": "index.html:6-7" },
    { "id": "H3", "severity": "high", "page": "/", "issue": "H1 contains no topical keyword", "evidence": "index.html:161" },
    { "id": "H4", "severity": "high", "page": "/", "issue": "Zero occurrences of 'mobile game development', 'Unity game development', 'company'; single URL for all services", "evidence": "phrase counts on extracted text" },
    { "id": "H5", "severity": "high", "page": "/", "issue": "Generic, unverifiable copy; no first-hand experience signals", "evidence": "index.html:184, 318, 329" },
    { "id": "M1", "severity": "medium", "page": "/privacy-policy/", "issue": "References non-existent cookie notice; Google Fonts IP transfer undisclosed", "evidence": "privacy-policy/index.html:115; fonts.googleapis.com link on all pages" },
    { "id": "M2", "severity": "medium", "page": "/games/, /", "issue": "Game list JS-only; home teaser hardcoded despite data-file comment", "evidence": "games.js:44; games-data.js:4; index.html:277-309" },
    { "id": "M3", "severity": "medium", "page": "/", "issue": "Inline tags/stats concatenate in text extraction; duplicated marquee list", "evidence": "extracted text 'UnityUnrealGodot', 'Emailsupport@...'" },
    { "id": "M4", "severity": "medium", "page": "all", "issue": "Heading order failures (Lighthouse) and H3 before H2 in games section", "evidence": "Lighthouse heading-order; index.html:288 vs 296" },
    { "id": "M5", "severity": "medium", "page": "/", "issue": "mailto form labelled 'Send message'; 'Explore our games' CTA leads to placeholder", "evidence": "index.html:167, 392, 395" },
    { "id": "M6", "severity": "medium", "page": "/", "issue": "No Q&A / definitional fact block for AI citation", "evidence": "no FAQ, no founding/location facts" },
    { "id": "L1", "severity": "low", "page": "/terms/", "issue": "JSON-LD breadcrumb name contains literal '&amp;'", "evidence": "terms/index.html:39" },
    { "id": "L2", "severity": "low", "page": "/privacy-policy/, /terms/", "issue": "Descriptions 173 / 169 chars", "evidence": "line 7 of each" },
    { "id": "L3", "severity": "low", "page": "all", "issue": "Footer IA (legal links under 'Games'); home footer inside main", "evidence": "index.html:399-418" },
    { "id": "L4", "severity": "low", "page": "all", "issue": "Brand link label-content-name mismatch", "evidence": "Lighthouse" },
    { "id": "L5", "severity": "low", "page": "/404.html", "issue": "noindex plus canonical", "evidence": "404.html:8, 10" }
  ]
}
```
