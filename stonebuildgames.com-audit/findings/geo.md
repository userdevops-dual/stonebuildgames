# GEO / AI Search Readiness: stonebuildgames.com (pre-launch)

- Audit date: 2026-11-04
- Scope: on-disk source in `site/` (what will be served). Pages reviewed: `index.html`, `games/index.html`, `privacy-policy/index.html`, `terms/index.html`, `404.html`, `robots.txt`, `sitemap.xml`, `_headers`, `site.webmanifest`, `js/games.js`, `js/games-data.js`.
- Method: read the files, parsed headings and word counts (`parse_html.py`), ran boilerplate-stripped extraction with trafilatura (what a non-JS AI crawler pipeline sees), and searched Wikipedia/Wikidata for name collisions. The domain is not live, so live crawler, CDN, header and AI-visibility checks were not possible. Any score for a specific platform is a readiness estimate, not measured visibility.
- Framing: Google's AI optimization guide says optimizing for generative AI search "is still SEO". Everything below is SEO fundamentals applied to AI surfaces. Scores are heuristics, not Google-internal signals.

## 1. AI Search Readiness score: 45 / 100

| Dimension | Weight | Score | Weighted | Main evidence |
|---|---|---|---|---|
| Citability | 25% | 45 | 11.3 | Good: a definitional sentence in the hero (`index.html:162`). Good: specific process durations (`:246-264`). Missing: question-and-answer blocks, any figures beyond durations, and passages that make sense on their own. |
| Structural Readability | 20% | 55 | 11.0 | Clean hierarchy: one H1, 5 H2s and 16 H3s, plus an ordered list for the process. Every heading is a slogan ("Solid foundations, built to last", "Built in the same forge..."). None is phrased as a question, and the site has no FAQ or table. |
| Multi-Modal | 15% | 15 | 2.3 | No `<img>` on any page. The hero is a decorative three.js canvas, game art is CSS shapes, and there is no video, screenshot or team photo. There is an OG image. |
| Authority & Brand | 20% | 20 | 4.0 | No founder or team, no country, no legal entity, no founding date, no `sameAs`, no portfolio and no shipped game. Wikipedia and Wikidata have no entity. Positives: the brand name and email are consistent, and the legal pages carry "Last updated" dates. |
| Technical Accessibility | 20% | 80 | 16.0 | Good: static HTML for the home and legal pages, `User-agent: * Allow: /`, a sitemap, canonicals and `index,follow`. Weak: the `/games/` list and the VideoGame JSON-LD are injected only by JS. CDN bot defaults are unverified. |
| **Total** | | | **~45** | |

Expected after the P0/P1 on-page fixes below: about 60. Without off-site presence and a shipped game, the realistic ceiling is about 65-70.

**Realistic goal for a new studio.** A new domain with no backlinks will not be cited for queries that don't name the studio ("best game development studio", "how long does it take to build a mobile game") any time soon. Google AI Overviews strongly favour pages that already rank. The near-term goal is narrower. When someone asks an AI assistant "What is StoneBuild Games?", "Who made [first title]?" or "Is StoneBuild Games legit?", the answer should be accurate, consistent and should cite stonebuildgames.com. Most fixes below serve that goal.

## 2. AI crawler access status

The on-disk `robots.txt` (4 lines) contains only `User-agent: *` / `Allow: /` plus a Sitemap line. No bot has its own group, so every compliant crawler falls under `*` and is allowed. Each bot below is listed against the capability it actually controls.

| User-agent | What it governs | Status (on-disk) |
|---|---|---|
| Googlebot | Google Search, **AI Overviews and AI Mode** | Allowed (via `*`) |
| Bingbot | Bing Search and **Copilot** grounding | Allowed (via `*`) |
| OAI-SearchBot | **ChatGPT Search citations** | Allowed (via `*`) |
| ChatGPT-User | Fetches triggered by a user in ChatGPT (OpenAI: robots.txt "may not apply") | Allowed (via `*`) |
| GPTBot | OpenAI **model training only** (no effect on ChatGPT Search) | Allowed (via `*`) |
| Claude-SearchBot | **Claude search citations** | Allowed (via `*`) |
| Claude-User | Fetches triggered by a user in Claude (honors robots.txt) | Allowed (via `*`) |
| ClaudeBot | Anthropic **model training only** (no effect on Claude search) | Allowed (via `*`) |
| PerplexityBot | **Perplexity search index** | Allowed (via `*`) |
| Perplexity-User | Fetches triggered by a user in Perplexity (generally ignores robots.txt) | n/a |
| Google-Extended | Gemini/Vertex **training and grounding**, plus training of the models behind Search gen-AI features. It does **not** control Search or AI Overviews inclusion. | Allowed (via `*`) |
| Applebot | Siri, Spotlight, Safari discoverability | Allowed (via `*`) |
| Applebot-Extended | Apple Intelligence **training only** | Allowed (via `*`) |
| CCBot / cohere-ai / Bytespider | Training data | Allowed (via `*`) |

Verdict: the file is correct as written for a site that wants to be cited.

**Pre-launch risk (P0).** `README.md` recommends Cloudflare Pages. Cloudflare can block AI crawlers at the edge, whatever robots.txt says. It offers AI-bot blocking during onboarding of new domains, an "AI Crawl Control" / "Block AI bots" setting, Bot Fight Mode, and a "Managed robots.txt" option that **prepends** its own Disallow rules and Content-Signal lines to your file. Any of these can silently override the intent of this file. After the zone is created, check that Googlebot, Bingbot, OAI-SearchBot, Claude-SearchBot and PerplexityBot are not blocked or challenged. Then fetch the live `/robots.txt` and compare it to the on-disk file.

**Optional: explicit robots.txt.** It works the same as the current file but documents intent. Note that a bot with its own named group ignores the `*` group, so any future Disallow added under `*` must be copied into every named group.

```
# StoneBuild Games robots.txt
# Policy: this is a public studio and legal-information site. All search engines
# and AI assistants may crawl it so the studio can be found, understood and cited.

# Search engines (Googlebot also feeds AI Overviews and AI Mode; Bingbot feeds Copilot)
User-agent: Googlebot
User-agent: Bingbot
User-agent: Applebot
Allow: /

# AI search and answer engines (citations in ChatGPT Search, Claude, Perplexity)
User-agent: OAI-SearchBot
User-agent: Claude-SearchBot
User-agent: PerplexityBot
Allow: /

# Fetches made when a person asks an assistant to open a page
User-agent: ChatGPT-User
User-agent: Claude-User
User-agent: Perplexity-User
Allow: /

# Model training and grounding: allowed on purpose, so models learn the studio exists.
# To opt out of training only, change "Allow: /" to "Disallow: /" in this group.
# That has no effect on ChatGPT Search, Claude search, Perplexity or Google AI Overviews.
# Blocking Google-Extended also removes Gemini app grounding.
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
User-agent: cohere-ai
Allow: /

User-agent: *
Allow: /

Sitemap: https://stonebuildgames.com/sitemap.xml
```

I recommend keeping training crawlers allowed. The site holds marketing copy and legal text, nothing proprietary. A new studio gains more from models knowing it exists than it loses by being trained on.

## 3. llms.txt and RSL status

- `/llms.txt`: **missing**. It carries no weight in the score. Google's AI optimization guide (2026) says Google Search ignores llms.txt and similar AI text files: they "will neither harm nor help" visibility. No major AI search provider has confirmed that its crawlers use third-party llms.txt files. Server-log studies show negligible bot requests for it (OtterlyAI: about 0.1% of AI-bot hits). It takes about 10 minutes to add and is harmless, so add it only as a cheap option for non-Google tools and agents. Do not count it as a citation lever. A proposed file is in section 9.
- RSL 1.0 licensing: **not present, and not recommended.** RSL is for publishers who want to license or charge for AI use of their content. This site wants to be read and cited, so restrictive licence terms would add nothing.

## 4. Passage-level citability (homepage)

trafilatura extracted 589 words from `index.html`. Section word counts from the raw HTML: hero 76, services 183, process 127, games 79, why 145, contact 147.

| Passage | Location | Assessment |
|---|---|---|
| "StoneBuild Games is a game development studio crafting 3D, 2D and multiplayer games for mobile, PC and **console**." | `index.html:162` | **Best citable sentence on the site**: an "X is a..." definition in the first 40 words. But "console" contradicts every other description (meta, schema, stats "Mobile & PC", footer). An AI system may repeat "console" as fact. |
| Service cards (6 × 17-20 words) | `:191-226` | Too short to stand alone, and they don't name the service in the sentence. In trafilatura output, **5 of 6 service H3 headings were dropped**, which left orphaned sentences like "Stylized or realistic 3D worlds..." with no label. |
| Process steps with durations (Week 1 / 2 to 3 weeks / two-week sprints) | `:242-271` | The **most specific facts on the site**, but split across five list items. No single passage answers "how does StoneBuild build a game / how long does it take". |
| "We ship our own titles too..." and "Published under StoneBuild Games on Google Play and the App Store" | `:297-299` | **Overclaims.** No title has shipped, and `games-data.js` lists the first title as Android only. An AI system could quote this as fact. Trust risk. |
| Why-us items ("Two-week sprints with a playable build and a written changelog", "Source code, art files and store accounts stay in your name") | `:329-341` | Specific, quotable commitments. Good raw material for FAQ answers. |
| Budget ranges (Under $5k, $5k-$15k, $15k-$50k, $50k+) | `:387` | Exists only as `<option>` values in the form. Not citable text. |
| "Remote studio, working with clients worldwide" | `:367` | The only "where" fact. No country. |

There are no question-and-answer passages. Third-party studies suggest roughly 130-170 words for a passage that can be quoted alone. That is a heuristic, not a rule: Google says content does not need to be chunked for AI. For a homepage FAQ, direct answers of 50-100 words are enough.

## 5. Structural readability

- Hierarchy is clean on every page: one H1, H2 sections, H3 cards. Semantic `<section>`, `<ol>`, `<dl>`, `<article>` and breadcrumbs are used. The legal pages have numbered H2s with anchor IDs and a table of contents, which is excellent.
- The H1 "We build games people can't put down." names neither the studio nor what it does. The lead paragraph right below makes up for this. Changing the H1 is optional and low priority.
- No headings match the questions prospective clients ask, e.g. "how long does it take to build a mobile game", "how much does a game cost", "who owns the source code".
- No FAQ and no comparison table (for example engines vs. platforms, or project type vs. typical timeline).
- Text-extraction artifacts that are minor but real:
  - The logo text `StoneBuild<span>Games</span>` (`index.html:121`, `:403`, and the header and footer of every page) extracts as **"StoneBuildGames"**.
  - The tech marquee (`:321-322`) is duplicated for the animation and has no separators, so it extracts as "UnityUnreal EngineGodotC#C++..." twice. Add `aria-hidden="true"` to the second track.

## 6. Entity clarity

| Fact | Status | Evidence |
|---|---|---|
| Brand name | Consistent: "StoneBuild Games" appears 62 times across the 4 pages. Short form "StoneBuild" appears 14 times. | Logo text extracts as "StoneBuildGames" (see above). |
| Email | Consistent: support@stonebuildgames.com on all pages and in schema. | 7, 3, 12, 8 and 2 occurrences |
| What (platforms) | **Inconsistent** | "mobile, PC and console" (`index.html:162`); "Android, iOS and PC" (meta `:7`, schema `:52/:77`); "mobile and PC" (OG `:15`, footers, `site.webmanifest`); "mobile, PC and web games" (`privacy-policy/index.html:98`) |
| Where | Weak: "Remote studio, working with clients worldwide" only | `index.html:367`. Terms say "the jurisdiction in which StoneBuild Games is established" without naming it (`terms/index.html:152`). |
| Who | **Missing**: no founder, team, legal entity name or founding year | No `founder`, `legalName`, `foundingDate` or `address` in the Organization JSON-LD (`index.html:41-61`) |
| Corroboration | **Missing**: no `sameAs` and no outbound profile links | none |
| Name collision | Clean: no Wikidata entity matches "StoneBuild", and Wikipedia search returns only unrelated fuzzy matches | "StoneBuild" written as one word is an ownable token. Keep it one word everywhere; "Stone Build" as two words is a generic phrase. |

Google Play will show a public developer name and contact details on the first game's listing, and verified legal name and address for organization accounts. The website's entity facts should match that listing **exactly**. It will be the first authoritative third-party page about the studio.

## 7. Brand mention analysis

Live mention tracking was not possible before launch, and no DataForSEO tools were available.

| Platform | Status | Note |
|---|---|---|
| Wikipedia | None (checked) | Not realistic until independent press coverage exists. Never write your own article (conflict of interest). |
| Wikidata | None (checked) | Possible after the first game ships, citing the Google Play listing as a reference. |
| YouTube | Not checked (results are rendered by JS) | Expected zero. Ahrefs (Dec 2025, 75k brands) found YouTube mentions have the strongest correlation with AI visibility (~0.737). That is correlation, not causation. |
| Reddit | Not checked (fetch blocked) | Expected zero. Perplexity and ChatGPT cite Reddit heavily. |
| LinkedIn | Not checked | Expected zero. A company page and a founder profile are the quickest corroboration. |

## 8. Technical accessibility

- **Static HTML**: the home and legal pages are fully readable without JS. Content uses opacity reveals but stays in the DOM, and there is a 1.2 s fallback. This is ideal for GPTBot, OAI-SearchBot, ClaudeBot and PerplexityBot, which public tests show fetch raw HTML without running JS.
- **`/games/` is rendered only on the client.** `games/index.html:95-97` ships an empty `#games-grid` and the noscript text "Enable JavaScript to see the list of games". `js/games.js:44` injects the cards, and `:46-69` injects the VideoGame JSON-LD. A non-JS crawler sees 51 words. Today this only hides a placeholder. Once the first title is live, its name, description, store link and structured data will be invisible to most AI crawlers. Googlebot renders JS, so Google is less affected. Also, `games.js:61` hard-codes `price: '0'`, which is wrong for any paid game.
- `sitemap.xml` lists all 4 indexable URLs. `404.html` is `noindex`. `_headers` has no `X-Robots-Tag`. No `nosnippet` anywhere. Canonicals are correct.
- After launch: verify in Google Search Console (leave the "Search generative AI" control at its default, include), and in Bing Webmaster Tools. Bing feeds Copilot and is widely reported to feed ChatGPT Search. Enable IndexNow; Cloudflare's "Crawler Hints" does this automatically.

### Platform readiness (qualitative, not measured)

| Platform | Branded queries ("StoneBuild Games") | Non-branded queries |
|---|---|---|
| Google AI Overviews / AI Mode | Ready once indexed (static HTML, Organization schema) | Low (new domain, no rankings) |
| ChatGPT Search | Medium once Bing has indexed the site and entity facts are consistent | Low (leans on Wikipedia and Reddit) |
| Perplexity | Medium | Low (heavy Reddit citation share) |
| Bing Copilot | Medium after Bing Webmaster Tools and IndexNow | Low |
| Claude | Medium | Low |

## 9. Prioritized changes (exact text)

### P0. Launch gate: verify the edge bot policy (15-30 min)
After the Cloudflare zone is created:
1. Open AI Crawl Control / Bots. Make sure AI-bot blocking does not cover OAI-SearchBot, Claude-SearchBot or PerplexityBot.
2. Leave "Managed robots.txt" **off** unless you want Cloudflare's training-bot Disallow rules prepended.
3. Check that Bot Fight Mode is not challenging verified crawlers.
4. Optionally replace `site/robots.txt` with the explicit version in section 2.

Post-launch checks:
```
curl -s https://stonebuildgames.com/robots.txt
for ua in "OAI-SearchBot/1.0" "Claude-SearchBot/1.0" "PerplexityBot/1.0" "GPTBot/1.1" "ClaudeBot/1.0" "Googlebot/2.1" "bingbot/2.0"; do
  printf "%-22s " "$ua"; curl -s -o /dev/null -w "%{http_code}\n" -A "Mozilla/5.0 (compatible; $ua)" https://stonebuildgames.com/; done
```
A spoofed user agent only catches blocks based on the user-agent string. Cloudflare verifies real bots by IP, so the authoritative check is the Cloudflare dashboard and logs.

### P1. One canonical entity description, plus who and where (about 1 hour, plus owner decisions)
Canonical sentence. Use it verbatim, or its short form, everywhere:
> StoneBuild Games is a remote game development studio that builds 3D, 2D and multiplayer games for Android, iOS and PC with Unity, Unreal Engine and Godot.

Short form, for footers, the manifest and OG: "Game development studio building 3D, 2D and multiplayer games for Android, iOS and PC."

- `index.html:162`: replace the hero lead with the passage in P2a below. This removes "console". If console work is real, add console to every description instead.
- Footers (`index.html:405`, `games/index.html:115`, `privacy-policy/index.html:203`, `terms/index.html:193`, `404.html:104`), `site.webmanifest` "description", and OG/Twitter descriptions (`index.html:15,23`): change "mobile and PC" to "Android, iOS and PC".
- `index.html:121` and `:403` (and the same logo markup on the other pages): change to `<span class="brand-name">StoneBuild <span>Games</span></span>` so the text reads "StoneBuild Games".
- Organization JSON-LD (`index.html:41-61`): add only facts that are true and public. Don't publish placeholder URLs.
```json
"legalName": "[Registered company name, as on the Google Play developer account]",
"foundingDate": "[YYYY]",
"founder": {
  "@type": "Person",
  "name": "[Founder name]",
  "jobTitle": "Founder",
  "sameAs": ["https://www.linkedin.com/in/[handle]"]
},
"address": { "@type": "PostalAddress", "addressCountry": "[ISO country code]" },
"areaServed": "Worldwide",
"sameAs": [
  "https://www.linkedin.com/company/[stonebuild-games]",
  "https://www.youtube.com/@[handle]",
  "https://play.google.com/store/apps/dev?id=[developer id]"
]
```
- `terms/index.html:152`: name the governing jurisdiction ("the laws of [country/state]"). This is good legal practice and also states the "where" fact.

### P1. Rewrite three homepage passages and add an FAQ (2-3 hours)

**P2a. Hero lead (`index.html:162`)**, 51 words:
> StoneBuild Games is a remote game development studio that builds 3D, 2D and multiplayer games for Android, iOS and PC with Unity, Unreal Engine and Godot. We take client games from first concept to launch on Google Play, the App Store or Steam, and keep supporting them with updates after release.

Variant if you disclose location: "...is a game development studio based in [City, Country] that builds..., working remotely with clients worldwide."

**P2b. Process section (`index.html:238-239`)**
- H2: `How we build a game, from idea to launch`
- Lead (55 words):
> Every StoneBuild Games project follows five stages: discovery (about one week), a playable prototype (two to three weeks), production in two-week sprints, polish and QA, then launch and LiveOps. You get a playable build and a written changelog at the end of every sprint, so you always know what is done and what ships next.

**P2c. Games section, made honest (`index.html:297-299`)**
- Lead:
> StoneBuild Games also develops its own games. Our first original title is in production for Android and will be published on Google Play under the StoneBuild Games developer name. It is built with the same pipeline we use for client work: tested on real devices, backed by a public privacy policy and supported after launch.
- List item 1: `Published under the StoneBuild Games developer account on Google Play`. Add the App Store once an iOS title exists.

**P2d. New FAQ section.** Insert between `#why` and `#contact`, with plain `<h3>` and `<p>` elements, visible and not collapsed. Do **not** expect FAQ rich results: since 2023 Google shows them only for authoritative government and health sites. Optional FAQPage JSON-LD is harmless. A two-column card grid keeps it to one screen in the snap layout.

- Eyebrow: `FAQ`. H2: `Questions about working with StoneBuild Games`

1. **What does a game development studio do?**
   A game development studio designs, programs, creates art for, tests and releases video games, either its own titles or games made for clients. At StoneBuild Games that covers the full cycle: game design and prototyping, engineering in Unity, Unreal Engine or Godot, 2D and 3D art and animation, multiplayer backend, QA on real devices, and publishing on Google Play, the App Store and Steam. You can hire us for the whole game or for one part of it.
2. **How long does it take to build a mobile game?**
   It depends on scope. Discovery takes about one week and a playable prototype takes two to three weeks, so you can judge whether the game is fun within roughly a month. Production then runs in two-week sprints. As a rough guide, a small hyper-casual game can be store-ready in [1-3] months, a casual 2D game with progression and monetization in [3-6] months, and a 3D or multiplayer game usually takes [6+] months. We give you a sprint-by-sprint estimate after discovery.
   *(The bracketed ranges are typical industry ballparks. Replace them with numbers you will stand behind before publishing.)*
3. **How much does it cost to develop a game?**
   Cost depends on scope, platforms and art style, and we agree a plan and budget at the end of discovery. We quote projects in four ranges: under $5,000 [for a prototype or small casual game], $5,000 to $15,000, $15,000 to $50,000, and $50,000 or more [for larger 3D or multiplayer games]. Pick your range in the contact form and we will tell you honestly what it can deliver.
   *(The ranges match the existing form options at `index.html:387`. Confirm the bracketed mapping.)*
4. **Who owns the game, source code and art?**
   You do. Source code, art files and store accounts stay in your name, under a written contract with clear intellectual property terms. There is no lock-in, so you can continue development in-house or with another team at any time.
5. **Which engines and platforms does StoneBuild Games work with?**
   We build in Unity (C#), Unreal Engine (C++) and Godot, use Blender for 3D art, Photon for real-time multiplayer and Firebase for analytics, crash reporting and cloud services. We ship to Android through Google Play, iOS through the App Store and PC through Steam.
6. **Where is StoneBuild Games based?**
   StoneBuild Games is a remote studio [registered in Country] that works with clients worldwide in English. Email support@stonebuildgames.com and we reply within two business days.

The answers reuse facts already on the page: durations, budget ranges, ownership, tools and response time. They add no unverified claims beyond the bracketed items.

**Optional: service cards that name themselves (`index.html:191-226`).** Start each sentence with the service name, so it survives extraction without its H3. Example for `:198`:
> 3D game development: stylized or realistic 3D worlds with custom shaders, lighting and physics, optimized to run smoothly on mid-range phones.

### P1. Render /games/ as static HTML (30-60 min, required before the first title goes live)
- Put the card markup directly inside `#games-grid` in `games/index.html:95`, using the HTML `games.js` produces. Put the `ItemList`/`VideoGame` JSON-LD as a static `<script type="application/ld+json">` in the `<head>`.
- Then either stop `games.js` from inserting cards (only inject if the grid is empty), or add a small pre-deploy step that writes the HTML from `games-data.js`.
- Fix `games.js:61` so the price comes from the data.
- Add a short definitional sentence per game, e.g. "[Title] is a [genre] game for Android by StoneBuild Games, released on [date]."

### P1. Seed the entity off-site (first steps 2-3 hours, then ongoing)
Ranked by realistic value for a studio with no shipped games:
1. **Google Play developer account** named exactly "StoneBuild Games", with website https://stonebuildgames.com and the same support email. Add the developer page URL to `sameAs` when live.
2. **LinkedIn** company page "StoneBuild Games", plus a founder profile that lists it. Add both to `sameAs`.
3. **YouTube devlog** for the first title (short gameplay clips, "how we built X"). This is the strongest correlated mention signal, and it is also the multi-modal fix.
4. **Reddit and community**: real participation in r/gamedev, r/IndieDev, r/Unity3D and r/androiddev, sharing actual lessons. Google explicitly warns against chasing inauthentic mentions, so do not spam.
5. **B2B directories**: Clutch, GoodFirms, plus an itch.io studio page. AI answers to "game development studios for hire" queries often cite these lists.
6. Submit the site to Google Search Console and Bing Webmaster Tools on launch day.

### P2. First-hand content (ongoing)
Google's guide rewards unique, first-hand content over commodity content. Before any non-branded citation is likely, the studio needs content only it can write: a devlog or case study about building the first title. Examples: "How we got our Unity game under [N] MB for Google Play"; "Running Google Play's closed test before production access (if your account is subject to the 12-tester / 14-day requirement)"; "Prototype to soft launch: what our first [N] sprints looked like". Give each post a byline and date.

### P2. Multi-modal (once assets exist)
Add real screenshots or a GIF of the prototype with descriptive `alt` text and captions, a founder or team photo on an About block, and an embedded trailer when one exists. Use `<img>` with width and height, not CSS backgrounds.

### P3. llms.txt (10 min, zero Google weight)
`site/llms.txt`. Delete any line you can't fill truthfully:
```
# StoneBuild Games

> StoneBuild Games is a remote game development studio that builds 3D, 2D and multiplayer games for Android, iOS and PC with Unity, Unreal Engine and Godot. It offers full-cycle game development for clients, from concept and prototype to store launch and LiveOps, and is developing its first original game for Google Play.

Key facts (as of November 2026):
- Name: StoneBuild Games ("StoneBuild" is one word)
- Website: https://stonebuildgames.com
- Contact: support@stonebuildgames.com (replies within 2 business days)
- Location: remote studio [registered in Country], working with clients worldwide
- Engines and tools: Unity, Unreal Engine, Godot, Blender, Photon, Firebase
- Platforms: Android (Google Play), iOS (App Store), PC (Steam)
- Status: accepting client projects; first original title in production for Google Play, not yet released

## Studio
- [Game development services](https://stonebuildgames.com/#services): full-cycle development, 3D, 2D/casual/hyper-casual, multiplayer and backend, game art and animation, porting, QA and publishing
- [Development process](https://stonebuildgames.com/#process): discovery (about 1 week), prototype (2-3 weeks), two-week production sprints, polish and QA, launch and LiveOps
- [Contact](https://stonebuildgames.com/#contact): how to start a project and budget ranges

## Games
- [Games by StoneBuild](https://stonebuildgames.com/games/): every StoneBuild title with platforms, release status and store links

## Legal
- [Privacy Policy](https://stonebuildgames.com/privacy-policy/): data collected by StoneBuild games and this site, third-party SDKs, data deletion requests
- [Terms & Conditions](https://stonebuildgames.com/terms/): licence, purchases, conduct and liability for StoneBuild games
```
Keep it in sync with the site. A stale llms.txt that contradicts the homepage is worse than having none.

### P3. Small DOM text fixes (15 min)
- Add `aria-hidden="true"` to the second `.marquee-track` copy (`index.html:322`). This is an accessibility fix as well.
- Optional: name the studio in the H1, e.g. a visible eyebrow above it reading "StoneBuild Games · Game development studio". Do not use visually hidden text for this.

## 10. Structured findings (for audit-data.json, category "AI Search Readiness")

```json
{
  "category": "AI Search Readiness",
  "score": 45,
  "projected_score_after_onpage_fixes": 60,
  "dimensions": {
    "citability": 45, "structural_readability": 55, "multi_modal": 15,
    "authority_brand": 20, "technical_accessibility": 80
  },
  "measured_live": false,
  "findings": [
    {"id": "geo-edge-bot-policy", "severity": "high", "priority": "P0", "effort": "15-30 min",
     "title": "CDN-level AI bot blocking unverified (Cloudflare recommended in README)",
     "evidence": "robots.txt allows all; Cloudflare AI-bot blocking, Managed robots.txt and Bot Fight Mode can override it at the edge",
     "recommendation": "Verify OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot and Bingbot are allowed in the Cloudflare dashboard; compare live /robots.txt to the on-disk file"},
    {"id": "geo-entity-inconsistent-platforms", "severity": "high", "priority": "P1", "effort": "30 min",
     "title": "Studio description inconsistent across pages",
     "evidence": "index.html:162 'mobile, PC and console'; meta/schema 'Android, iOS and PC'; footers/manifest 'mobile and PC'; privacy:98 'mobile, PC and web'",
     "recommendation": "Use one canonical description verbatim everywhere"},
    {"id": "geo-entity-who-where-missing", "severity": "high", "priority": "P1", "effort": "1 h + decisions",
     "title": "No founder, country, legal entity, founding date or sameAs",
     "evidence": "Organization JSON-LD index.html:41-61 lacks founder/legalName/foundingDate/address/sameAs; only 'Remote studio' at :367; terms:152 jurisdiction unnamed",
     "recommendation": "Publish true who/where facts matching the Google Play developer listing; add sameAs when profiles exist"},
    {"id": "geo-no-question-headings-faq", "severity": "medium", "priority": "P1", "effort": "2-3 h",
     "title": "No question-based headings or self-contained answers",
     "evidence": "All H2s are slogans; process facts split across 5 list items; budget ranges only in <option> values (index.html:387)",
     "recommendation": "Add a 6-question FAQ and rewrite the hero, process and games leads (exact text in geo.md section 9)"},
    {"id": "geo-games-overclaim", "severity": "medium", "priority": "P1", "effort": "10 min",
     "title": "Homepage claims shipped titles and App Store publishing before any release",
     "evidence": "index.html:297 'We ship our own titles too'; :299 'Published ... on Google Play and the App Store'; games-data.js first title Android, in production",
     "recommendation": "Use honest present-tense copy (P2c)"},
    {"id": "geo-games-csr", "severity": "medium", "priority": "P1", "effort": "30-60 min",
     "title": "/games/ list and VideoGame JSON-LD rendered only by JavaScript",
     "evidence": "games/index.html:95-97 empty grid + noscript; games.js:44 and :46-69 inject content; non-JS extraction = 51 words; games.js:61 hard-codes price 0",
     "recommendation": "Ship game cards and JSON-LD as static HTML before the first title goes live"},
    {"id": "geo-no-offsite-entity", "severity": "high", "priority": "P1", "effort": "ongoing",
     "title": "No off-site entity presence (expected pre-launch)",
     "evidence": "No Wikidata entity or Wikipedia article for StoneBuild; no sameAs; YouTube/Reddit/LinkedIn not measurable pre-launch",
     "recommendation": "Google Play developer page, LinkedIn, YouTube devlog, genuine Reddit participation, Clutch/GoodFirms; GSC + Bing Webmaster Tools"},
    {"id": "geo-no-media", "severity": "medium", "priority": "P2", "effort": "when assets exist",
     "title": "No images or video on any page",
     "evidence": "parse_html images=0 on all 4 pages; hero is a decorative canvas",
     "recommendation": "Screenshots/GIFs with alt text, team photo, trailer embed"},
    {"id": "geo-llms-txt-missing", "severity": "info", "priority": "P3", "effort": "10 min",
     "title": "llms.txt missing (no Google weight)",
     "evidence": "No site/llms.txt; Google Search ignores llms.txt per its AI optimization guide",
     "recommendation": "Optional: add the file from geo.md section 9"},
    {"id": "geo-dom-text-artifacts", "severity": "low", "priority": "P3", "effort": "15 min",
     "title": "Brand logo text extracts as 'StoneBuildGames'; marquee duplicated in text",
     "evidence": "index.html:121,403 StoneBuild<span>Games</span>; :321-322 duplicate marquee; trafilatura drops 5 of 6 service H3s",
     "recommendation": "Add a space in the logo text, aria-hidden on the second marquee track, self-naming service sentences"}
  ]
}
```
