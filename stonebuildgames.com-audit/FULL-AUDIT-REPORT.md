# StoneBuild Games — Pre-launch SEO Audit

Date: 2026-11-04 · Target: https://stonebuildgames.com (not live; audited from `site/` served at localhost) · Business type: B2B service studio (game development) with upcoming consumer apps.

## Executive summary

Specialist scores before fixes (heuristic, from file review):

| Category | Score | Notes |
|---|---|---|
| Schema / structured data | 76 | Valid JSON-LD everywhere; one encoding bug; thin inner-page graphs |
| Content quality | 52 | Clean writing, but weak trust signals and some claims ahead of reality |
| On-page | 68 | Unique metadata; home title/description too long; H1 without topic keyword |
| AI search readiness (GEO) | 45 | One good definitional sentence; no FAQ; no entity facts off-site |
| Agent readiness | 67 | Good landmarks and labels; JS-only games list; dots without names |
| Lighthouse (mobile, home, v1) | Perf 29 / A11y 98 / BP 100 / SEO 100 | three.js parse/execute on throttled CPU; heading order; label mismatch |
| Lighthouse (mobile, games, v1) | Perf 92 / A11y 98 / BP 100 / SEO 100 | |
| Lighthouse (home, after fixes) | Mobile: Perf 92 / A11y 100 / BP 100 / SEO 100 (LCP 3.0 s) · Desktop: Perf 97 / A11y 100 / BP 100 / SEO 100 (LCP 1.2 s) | three.js lazy on desktop only, fonts self-hosted, LCP-safe hero |

Everything the audit could fix in the files has been applied (see ACTION-PLAN.md). What remains needs facts only the owner has (identity, profiles, jurisdiction) or happens after deploy (Cloudflare bot settings, Search Console).

## Technical SEO
- Static HTML, one H1 per page, canonical on every indexable page, `noindex` on 404 without canonical.
- `robots.txt` with explicit crawler groups and sitemap; `sitemap.xml` with 7 URLs.
- Security headers via `_headers` (nosniff, frame options, referrer policy, permissions policy).
- Self-hosted fonts, pinned self-hosted libraries, no third-party requests at all on first load.
- The technical specialist agent ran out of turns before reporting; its partial notes, if any, are in `findings/technical.md`.

## Content and E-E-A-T
See `findings/content.md`. Key gaps: no named people or legal entity, no shipped titles yet, generic claims. Copy was rewritten to state only what is true today.

## Structured data
See `findings/schema.md`. All recommendations applied except `sameAs`, `founder`, `foundingDate`, `address` (owner input).

## AI search / GEO and agent readiness
See `findings/geo.md` and `findings/agentic.md`. Applied: consistent entity sentence, FAQ, static games card, `llms.txt`, robots policy, accessibility fixes. Pending: off-site presence.

## Performance
Lighthouse reports (JSON) are in `lighthouse/` (ignored by git). After fixes, home scores mobile 92/100/100/100 and desktop 97/100/100/100 (performance / accessibility / best practices / SEO). Remaining mobile LCP cost is the render-blocking stylesheet and font load on a throttled 4G profile.
