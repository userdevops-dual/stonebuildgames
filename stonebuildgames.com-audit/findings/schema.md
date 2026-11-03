# Schema / Structured Data Audit: stonebuildgames.com (pre-launch)

Audited from disk: `site/` (exactly what will be served). Date: 2026-11-04. No site files were modified.

## Score: 76 / 100

| Area | Score | Notes |
|---|---|---|
| Syntax and validity | 15 / 15 | 5 of 5 JSON-LD blocks parse; https `@context`; no deprecated types |
| Google required / recommended properties | 17 / 20 | BreadcrumbList and Organization/logo valid; `&amp;` bug and 404 breadcrumb deduct |
| Graph linking (`@id`) | 12 / 15 | Home graph is clean, no dangling refs; inner pages are not linked to it; Service has no `@id` |
| Entity completeness | 13 / 20 | No `sameAs` (no profiles exist), no address/founder/foundingDate (not on site) |
| Page coverage | 11 / 15 | No WebPage/CollectionPage on inner pages; games not in static HTML (none live yet) |
| Runtime-generated VideoGame JSON | 8 / 15 | Works, but 6 latent defects that will ship the day a game goes live |

## 1. Detection results

| File | Format | Blocks | Types | Valid JSON |
|---|---|---|---|---|
| `index.html` (head, line 37) | JSON-LD | 1 (`@graph`, 4 nodes) | Organization, WebSite, WebPage, Service (+ nested ImageObject, ContactPoint, OfferCatalog, Offer, Service) | Yes |
| `games/index.html` (line 33) | JSON-LD | 1 | BreadcrumbList | Yes |
| `privacy-policy/index.html` (line 33) | JSON-LD | 1 | BreadcrumbList | Yes |
| `terms/index.html` (line 33) | JSON-LD | 1 | BreadcrumbList | Yes (but see E1) |
| `404.html` (line 33) | JSON-LD | 1 | BreadcrumbList | Yes (but see W1) |
| `js/games.js` (line 46-69) | JSON-LD injected at runtime | 0 today (no game has `status: "live"`) | ItemList > ListItem > VideoGame > Offer | Output verified by executing the script against sample data |

No Microdata or RDFa anywhere. No FAQPage, HowTo or SpecialAnnouncement present.

## 2. Validation results

### Passes
- All 5 static blocks are syntactically valid JSON; `@context` is `https://schema.org` everywhere.
- Every URL in the JSON-LD is absolute https on the production domain, and every page URL resolves to a file on disk (`/`, `/games/`, `/privacy-policy/`, `/terms/`, `/404.html`). Breadcrumb URLs match each page's `rel="canonical"`.
- Logo: `https://stonebuildgames.com/assets/logo-512.png` exists, is a 512x512 RGBA PNG, square, above Google's 112x112 minimum, and declared dimensions match the file. `og-image.png` (1200x630) also exists.
- `@id` linking on the home page is intact: `#organization`, `#website`, `#webpage` are defined; the only references (`publisher`, `provider`, `isPartOf`, `about`) all resolve. Zero dangling references.
- No placeholder text, no empty values, no relative URLs, no invalid dates (no date properties in static JSON-LD; sitemap `lastmod` values are ISO 8601).
- JSON-LD text matches visible content: name, e-mail, 6 services, "worldwide", breadcrumb labels on games/privacy/terms (each has a visible `<ol class="breadcrumbs">`).
- No deprecated or no-rich-result types recommended or present. The Process section on the home page must NOT be marked up as HowTo (rich results removed Sept 2023).

### Errors and warnings

| ID | Sev | File | Issue | Exact fix |
|---|---|---|---|---|
| E1 | Error (low impact) | `terms/index.html` line 39 | `"name": "Terms &amp; Conditions"`. Content of `<script type="application/ld+json">` is raw text; HTML entities are NOT decoded, so the breadcrumb name is the literal string `Terms &amp; Conditions` (mismatches visible text `Terms & Conditions`). | Change to `"name": "Terms & Conditions"`. A raw `&` is valid inside JSON-LD in a script element. |
| W1 | Warning | `404.html` lines 33-42 | BreadcrumbList on a `noindex` error page: it has no visible breadcrumb on the page (Google requires markup to reflect visible content), it points `item` at the error page itself, and the error page is not part of the site hierarchy. Zero rich-result value; risk of misleading breadcrumbs. | Delete the whole `<script type="application/ld+json">...</script>` block (lines 33-42). |
| W2 | Warning (latent) | `js/games.js` line 59 | ``image: `https://stonebuildgames.com${g.cover}` ``: if `cover` is ever an absolute URL (CDN) the output is `https://stonebuildgames.comhttps://cdn...` (reproduced). Also breaks if the path lacks a leading `/`. | Use `new URL(g.cover, 'https://stonebuildgames.com/').href` (see patch below). |
| W3 | Warning (latent) | `js/games.js` line 57 | `applicationCategory: 'Game'` is not one of Google's accepted values. `operatingSystem` is built by joining platform labels, so a PC game yields `"Android, iOS, PC"` ("PC" is not an operating system); empty `platforms` yields `""`. | `applicationCategory: 'GameApplication'`; map `Android->Android`, `iOS->iOS`, `PC->Windows`, `Web->Web browser`; omit if empty. |
| W4 | Warning (latent) | `js/games.js` line 61 | `offers` hard-codes `price: '0'` and `priceCurrency: 'USD'` for every game (wrong for a paid title), and has no `availability`. | Read optional `g.price` / `g.currency` from `games-data.js` (default `"0"` / `"USD"`) and add `availability: "https://schema.org/InStock"`. |
| W5 | Warning (latent) | `js/games.js` line 60 | `author` is a copy of the Organization with no `@id`, so it is not linked to the home-page `#organization` entity. No `publisher`. VideoGame has no `@id`. | `author`/`publisher`: `{"@type":"Organization","@id":"https://stonebuildgames.com/#organization","name":"StoneBuild Games","url":"https://stonebuildgames.com/"}` (self-sufficient, since Google does not resolve cross-page `@id`); give each game `@id` = `https://stonebuildgames.com/games/#<id>`. |
| W6 | Warning | `games/`, `privacy-policy/`, `terms/` | Inner pages carry only a BreadcrumbList. No WebPage node, no `isPartOf` to `#website`, no `publisher`, no `breadcrumb` property, no `inLanguage`, no `dateModified` (legal pages show a visible "Last updated: November 4, 2026"). The inner pages are disconnected from the home-page entity graph. | Replace each block with the `@graph` (WebPage/CollectionPage + BreadcrumbList) in section 4. |
| W7 | Info | `index.html` Service node | Service has no `@id` (cannot be referenced), and the six Offer-wrapped services have no description/url. No price is fine (quote-based), and Google has no Service rich result, so this is entity-clarity only. | Add `"@id": "https://stonebuildgames.com/#services"`, `url`, `description`; add per-service `description` from the visible text (see section 4). |
| W8 | Info | `js/games.js` generally | The ItemList of VideoGame is injected client-side. Googlebot renders JavaScript so it will be read, but non-rendering parsers (many AI/answer crawlers, link-preview tools) will not see it. Also: Google's Carousel rich result does not support VideoGame and requires each item to have its own URL, so this ItemList is for entity understanding only, not a SERP feature. | Acceptable at launch. When there are 1-3 games, consider a build step that writes the same JSON into `games/index.html` statically (and skip runtime injection to avoid duplicates). |
| I1 | Info | `index.html` Organization | `sameAs` missing. Verified by grep: no social, GitHub, store-developer or other profile link exists anywhere in the site, so nothing real can be added yet. | When the profiles exist (Google Play developer page, X, YouTube, LinkedIn, GitHub, itch.io, Steam developer page), add them as a `sameAs` array of full URLs. Do not add unverified or invented profile URLs. |
| I2 | Info | `index.html` Organization | `address`, `legalName`, `foundingDate`, `founder` are absent and no source for them exists on the site (the footer is "Remote studio"; Terms section 16 says "the jurisdiction in which StoneBuild Games is established" without naming it). | Needs owner input. Add `foundingDate` (ISO 8601 year or date), `founder` (Person), and `address` (PostalAddress with at least `addressCountry`) only when the true values are known. Do NOT switch to LocalBusiness: there is no physical location to serve. |
| I3 | Info | `index.html` | Hero copy says "mobile, PC and console"; JSON-LD `description`, meta description and footer say "Android, iOS and PC". | Decide whether console work is offered, then align copy and structured data. |
| I4 | Info | `index.html` WebSite/Organization | No `alternateName`. `site.webmanifest` already uses `short_name: "StoneBuild"`, which is the likely shorthand users search. Helps Google's site-name selection. | Add `"alternateName": "StoneBuild"` to WebSite (and Organization). |
| I5 | Info | `index.html` ContactPoint | `contactType: "customer support"`; Google's examples use "customer service". The same mailbox also receives project enquiries ("Start a project", "we reply within two business days"). | Optional: rename to `customer service` and add a second `sales` ContactPoint (included below). |

## 3. Google rich result eligibility summary

| Type | Eligible feature | Status |
|---|---|---|
| BreadcrumbList (games, privacy, terms) | Breadcrumb rich result | Valid (position, name, item present). Fix E1. 404 block should be removed. |
| Organization + logo | Logo / knowledge panel signals (no standalone rich result; no required props) | Valid. Logo meets guidelines. |
| WebSite (home) | Site name in results | Valid (`name` + `url` on the home page). Add `alternateName`. |
| Service / OfferCatalog | None (no Google feature) | Valid schema.org; entity clarity only. |
| VideoGame (runtime) | None. Google's Software App feature supports only SoftwareApplication, MobileApplication, WebApplication and needs `aggregateRating` or `review` plus `offers.price`. | Do not fabricate ratings. Only add `aggregateRating`/`review` if genuine, user-generated and visible on the page. |

## 4. Recommended JSON-LD (complete, copy-pasteable)

All values come from the site itself (names, e-mail, descriptions, services, image sizes, dates). Nothing is invented. `sameAs`, `address`, `founder`, `foundingDate` are intentionally omitted because the data does not exist yet.

Note on cross-page `@id`: inner-page nodes reference `https://stonebuildgames.com/#organization` and `https://stonebuildgames.com/#website`, which are defined on the home page. This is standard practice and costs nothing, but Google does not resolve `@id` across pages, so no rich result depends on it (BreadcrumbList is self-contained).

### 4.1 `index.html` - replace the existing block (adds alternateName, logo @id, sales ContactPoint, primary image, inLanguage, Service @id/url/descriptions)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://stonebuildgames.com/#organization",
      "name": "StoneBuild Games",
      "alternateName": "StoneBuild",
      "url": "https://stonebuildgames.com/",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://stonebuildgames.com/#logo",
        "url": "https://stonebuildgames.com/assets/logo-512.png",
        "contentUrl": "https://stonebuildgames.com/assets/logo-512.png",
        "width": 512,
        "height": 512,
        "caption": "StoneBuild Games logo"
      },
      "description": "Game development studio building 3D, 2D and multiplayer games for Android, iOS and PC.",
      "email": "support@stonebuildgames.com",
      "contactPoint": [
        {
          "@type": "ContactPoint",
          "email": "support@stonebuildgames.com",
          "contactType": "customer service",
          "availableLanguage": [
            "English"
          ]
        },
        {
          "@type": "ContactPoint",
          "email": "support@stonebuildgames.com",
          "contactType": "sales",
          "availableLanguage": [
            "English"
          ],
          "areaServed": "Worldwide"
        }
      ],
      "knowsAbout": [
        "Game development",
        "Unity",
        "Unreal Engine",
        "Godot",
        "3D game development",
        "Mobile games",
        "Multiplayer games"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://stonebuildgames.com/#website",
      "url": "https://stonebuildgames.com/",
      "name": "StoneBuild Games",
      "alternateName": "StoneBuild",
      "description": "Game development studio for 3D, 2D and multiplayer games.",
      "publisher": {
        "@id": "https://stonebuildgames.com/#organization"
      },
      "inLanguage": "en"
    },
    {
      "@type": "ImageObject",
      "@id": "https://stonebuildgames.com/#primaryimage",
      "url": "https://stonebuildgames.com/assets/og-image.png",
      "contentUrl": "https://stonebuildgames.com/assets/og-image.png",
      "width": 1200,
      "height": 630,
      "caption": "StoneBuild Games logo on a dark background with the words Game Development Studio"
    },
    {
      "@type": "WebPage",
      "@id": "https://stonebuildgames.com/#webpage",
      "url": "https://stonebuildgames.com/",
      "name": "StoneBuild Games | Game Development Studio for 3D, 2D & Multiplayer Games",
      "description": "StoneBuild Games is a game development studio building 3D, 2D and multiplayer games for Android, iOS and PC with Unity, Unreal and Godot.",
      "inLanguage": "en",
      "isPartOf": {
        "@id": "https://stonebuildgames.com/#website"
      },
      "about": {
        "@id": "https://stonebuildgames.com/#organization"
      },
      "primaryImageOfPage": {
        "@id": "https://stonebuildgames.com/#primaryimage"
      },
      "image": {
        "@id": "https://stonebuildgames.com/#primaryimage"
      }
    },
    {
      "@type": "Service",
      "@id": "https://stonebuildgames.com/#services",
      "url": "https://stonebuildgames.com/#services",
      "name": "Game Development Services",
      "description": "Bring an idea, a prototype or a live game. We plug in wherever you are and take it to a polished, store-ready release.",
      "provider": {
        "@id": "https://stonebuildgames.com/#organization"
      },
      "serviceType": "Game development",
      "areaServed": "Worldwide",
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Game development services",
        "itemListElement": [
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "Full-cycle game development",
              "description": "Concept, design doc, prototype, production and release. One team owns the game from first build to storefront."
            }
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "3D game development",
              "description": "Stylized or realistic 3D worlds with custom shaders, lighting and physics, tuned to run smoothly on mid-range phones."
            }
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "2D, casual and hyper-casual game development",
              "description": "Fast prototypes, tight game feel and retention loops for the mobile stores, with ads and in-app purchases wired in cleanly."
            }
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "Multiplayer and backend development",
              "description": "Real-time netcode, matchmaking, leaderboards, cloud saves and server-side logic that scales with your player base."
            }
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "Game art and animation",
              "description": "Characters, environments, UI and VFX in one consistent style, rigged and animated to feel alive in-engine."
            }
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "Porting, QA and publishing",
              "description": "Store-ready builds, device testing, policy compliance and launch support for Google Play, App Store and Steam, plus LiveOps."
            }
          }
        ]
      }
    }
  ]
}
</script>
```

Optional `dateModified` for the home WebPage: only add it if it is kept in sync with `sitemap.xml` `lastmod` (a stale date is worse than none), so it is left out above.

### 4.2 `games/index.html` - replace the existing block (CollectionPage + linked breadcrumb)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "CollectionPage",
      "@id": "https://stonebuildgames.com/games/#webpage",
      "url": "https://stonebuildgames.com/games/",
      "name": "Our Games | StoneBuild Games",
      "description": "Games developed and published by StoneBuild Games for Android, iOS and PC. Store links, genres, platforms and release status for every title.",
      "inLanguage": "en",
      "isPartOf": {
        "@id": "https://stonebuildgames.com/#website"
      },
      "publisher": {
        "@id": "https://stonebuildgames.com/#organization"
      },
      "breadcrumb": {
        "@id": "https://stonebuildgames.com/games/#breadcrumb"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://stonebuildgames.com/games/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://stonebuildgames.com/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Games",
          "item": "https://stonebuildgames.com/games/"
        }
      ]
    }
  ]
}
</script>
```

### 4.3 `privacy-policy/index.html` - replace the existing block

`dateModified` matches the visible "Last updated: November 4, 2026". Update it whenever that date changes.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "https://stonebuildgames.com/privacy-policy/#webpage",
      "url": "https://stonebuildgames.com/privacy-policy/",
      "name": "Privacy Policy | StoneBuild Games",
      "description": "How StoneBuild Games collects, uses and protects information in our games and on our website, including third-party SDKs, ads, children's privacy and data deletion requests.",
      "inLanguage": "en",
      "isPartOf": {
        "@id": "https://stonebuildgames.com/#website"
      },
      "publisher": {
        "@id": "https://stonebuildgames.com/#organization"
      },
      "breadcrumb": {
        "@id": "https://stonebuildgames.com/privacy-policy/#breadcrumb"
      },
      "dateModified": "2026-11-04"
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://stonebuildgames.com/privacy-policy/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://stonebuildgames.com/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Privacy Policy",
          "item": "https://stonebuildgames.com/privacy-policy/"
        }
      ]
    }
  ]
}
</script>
```

### 4.4 `terms/index.html` - replace the existing block (also fixes E1)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "https://stonebuildgames.com/terms/#webpage",
      "url": "https://stonebuildgames.com/terms/",
      "name": "Terms & Conditions | StoneBuild Games",
      "description": "Terms and conditions for using StoneBuild Games' games and website, including licence, in-app purchases, user conduct, intellectual property and limitation of liability.",
      "inLanguage": "en",
      "isPartOf": {
        "@id": "https://stonebuildgames.com/#website"
      },
      "publisher": {
        "@id": "https://stonebuildgames.com/#organization"
      },
      "breadcrumb": {
        "@id": "https://stonebuildgames.com/terms/#breadcrumb"
      },
      "dateModified": "2026-11-04"
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://stonebuildgames.com/terms/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://stonebuildgames.com/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Terms & Conditions",
          "item": "https://stonebuildgames.com/terms/"
        }
      ]
    }
  ]
}
</script>
```

Minimum fix if you only want to correct E1 and change nothing else:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://stonebuildgames.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Terms & Conditions",
      "item": "https://stonebuildgames.com/terms/"
    }
  ]
}
</script>
```

### 4.5 `404.html`

Delete lines 33-42 (the BreadcrumbList script). Nothing replaces it. Keep `<meta name="robots" content="noindex">`.

### 4.6 `js/games.js` - replace the "Structured data for live games" section (lines 46-69, up to but not including the closing `})();`)

Tested by executing it in Node against sample data (relative cover, absolute cover, no cover/store/date, multiple platforms). Current data (`in-production`) still injects nothing.

```js
  // Structured data for live games (recommended replacement)
  const ORIGIN = 'https://stonebuildgames.com';
  const OS = { Android: 'Android', iOS: 'iOS', PC: 'Windows', Web: 'Web browser' };
  const abs = (p) => { try { return new URL(p, ORIGIN + '/').href; } catch (e) { return undefined; } };
  const ORG = { '@type': 'Organization', '@id': ORIGIN + '/#organization', 'name': 'StoneBuild Games', 'url': ORIGIN + '/' };

  const live = games.filter((g) => g.status === 'live');
  if (live.length) {
    const ld = {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      '@id': ORIGIN + '/games/#gamelist',
      'mainEntityOfPage': { '@id': ORIGIN + '/games/#webpage' },
      'numberOfItems': live.length,
      'itemListElement': live.map((g, i) => {
        const stores = [g.playStore, g.appStore, g.steam].filter(Boolean);
        return {
          '@type': 'ListItem', 'position': i + 1,
          'item': {
            '@type': 'VideoGame',
            '@id': `${ORIGIN}/games/#${g.id}`,
            'name': g.title,
            'description': g.description,
            'genre': g.genre,
            'url': `${ORIGIN}/games/#${g.id}`,
            'inLanguage': 'en',
            'gamePlatform': g.platforms,
            'applicationCategory': 'GameApplication',
            'operatingSystem': (g.platforms || []).map((p) => OS[p] || p).join(', ') || undefined,
            'datePublished': /^\d{4}-\d{2}-\d{2}$/.test(g.released || '') ? g.released : undefined,
            'image': g.cover ? abs(g.cover) : undefined,
            'author': ORG,
            'publisher': ORG,
            'installUrl': stores.length ? stores : undefined,
            'sameAs': stores.length ? stores : undefined,
            'offers': {
              '@type': 'Offer',
              'price': String(g.price ?? '0'),
              'priceCurrency': g.currency || 'USD',
              'availability': 'https://schema.org/InStock',
              'url': stores[0]
            }
          }
        };
      })
    };
    const s = document.createElement('script');
    s.type = 'application/ld+json';
    s.textContent = JSON.stringify(ld);
    document.head.appendChild(s);
  }
```

Optional additions to `games-data.js` (and its header comment) to support it: `price: "0"`, `currency: "USD"` (read via `g.price`/`g.currency`). `released` must stay `YYYY-MM-DD` or `""`. Do not set `status: "live"` until the store URL exists, otherwise `offers.url`, `installUrl` and `sameAs` are omitted.

Output shape for the template game in `games-data.js` (status `live`, Android/iOS/PC, Play Store URL, released 2026-12-01):

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "@id": "https://stonebuildgames.com/games/#gamelist",
  "mainEntityOfPage": { "@id": "https://stonebuildgames.com/games/#webpage" },
  "numberOfItems": 1,
  "itemListElement": [{
    "@type": "ListItem", "position": 1,
    "item": {
      "@type": "VideoGame",
      "@id": "https://stonebuildgames.com/games/#my-game",
      "name": "My Game", "description": "What the game is.", "genre": "Puzzle",
      "url": "https://stonebuildgames.com/games/#my-game", "inLanguage": "en",
      "gamePlatform": ["Android", "iOS", "PC"],
      "applicationCategory": "GameApplication",
      "operatingSystem": "Android, iOS, Windows",
      "datePublished": "2026-12-01",
      "image": "https://stonebuildgames.com/assets/games/my-game.webp",
      "author": { "@type": "Organization", "@id": "https://stonebuildgames.com/#organization", "name": "StoneBuild Games", "url": "https://stonebuildgames.com/" },
      "publisher": { "@type": "Organization", "@id": "https://stonebuildgames.com/#organization", "name": "StoneBuild Games", "url": "https://stonebuildgames.com/" },
      "installUrl": ["https://play.google.com/store/apps/details?id=com.stonebuildgames.mygame"],
      "sameAs": ["https://play.google.com/store/apps/details?id=com.stonebuildgames.mygame"],
      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": "https://play.google.com/store/apps/details?id=com.stonebuildgames.mygame" }
    }
  }]
}
```

(The `image` in this sample is the template's placeholder path from the `games-data.js` comment, used only to demonstrate URL building. It is not a real asset.)

## 5. Missing opportunities, prioritised

1. Fix E1 (1-word change) and delete the 404 block (W1). Quick wins, pre-launch.
2. Add the WebPage/CollectionPage + breadcrumb graphs to the three inner pages (W6).
3. Apply the games.js patch before the first game goes live (W2-W5). Add real `screenshot`, `trailer` (VideoObject) and `playMode` (SinglePlayer/MultiPlayer/CoOp) once the game has them; they are valid VideoGame properties and need real assets.
4. Add `sameAs` the day the first social/store-developer profile exists (I1). This is the single highest-value Organization addition for entity disambiguation.
5. Supply `foundingDate`, `founder`, `address.addressCountry` when decided (I2).
6. Later, if each game gets its own page (`/games/<id>/`): move the VideoGame to that page with `url` = that page, a self-contained BreadcrumbList (Home > Games > Game), and, only if real user ratings are shown on the page, `aggregateRating` (this is what makes a Software App rich result possible, using `["VideoGame","MobileApplication"]`).

Not recommended: HowTo for the Process section (deprecated), FAQPage (no SERP feature since May 2026; the site has no FAQ anyway), SpecialAnnouncement, LocalBusiness (no address), Review/AggregateRating on Organization (self-serving, no genuine reviews), SearchAction (no on-site search).
