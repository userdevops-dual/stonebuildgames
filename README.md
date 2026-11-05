# StoneBuild Games — Website

Production domain: **https://stonebuildgames.com** · Support email: **support@stonebuildgames.com**

A static, zero-build website for the StoneBuild Games studio: services, games catalogue, privacy policy
and terms (required for Google Play / App Store listings), with a 3D animated hero and full-screen sections.

```
site/                      ← publish this folder
  index.html               Home: 6 full-screen sections (hero, services, Stone Stack game, games, why us, contact)
  services/                Six services overview, plus one detail page per service
  about/index.html         Studio story, values, process, toolbox
  games/                   Games list, plus one folder per published game (generated)
  contact/index.html       Contact details + inquiry form (opens the visitor's email app)
  privacy-policy/index.html, terms/index.html, 404.html
  css/styles.css           Design system + layout (tokens at the top)
  css/fonts.css + fonts/   Self-hosted Inter and Sora (no Google Fonts request)
  js/main.js               Pill navbar, nav, section dots, reveals, page transitions, contact form
  js/hero3d.js             Three.js hero scene (lazy, desktop only; CSS fallback on phones)
  js/game.js               Stone Stack isometric mini-game (canvas)
  admin/                   Admin panel (noindex)
  data/games.json          Games and settings, written by the admin panel
  vendor/                  gsap, ScrollTrigger, three (self-hosted, pinned)
  assets/                  favicon, logo, OG image
  .htaccess                Security, caching and compression (generated)
  robots.txt  sitemap.xml  llms.txt  site.webmanifest  .well-known/security.txt
brand/                     Logo package: SVG, PNG, Google Play icon and feature graphic, zip
tools/                     build_pages.py (generates the pages), make_brand.py (generates logos and icons)
PLAN.md                    Design + architecture plan
stonebuildgames.com-audit/ SEO audit findings and Lighthouse reports (not deployed)
.claude/launch.json        Local preview (python http.server on :8787)
```

## Run locally

```bash
python3 tools/serve.py
```
Open http://localhost:8787

## Add a game (admin panel)

Open `/admin/` (for example https://stonebuildgames.com/admin/, or http://localhost:8787/admin/ when running `python3 tools/serve.py`).

- **Add game:** name, description, features, images, store links, rating, downloads and privacy answers. Save as draft or publish.
- **Stores:** a store button only appears on the website when you switch that store on and add its link.
- **Home page:** the games section appears only once at least 4 games are published. The first 6 in the admin list are shown, in wide boxes like the services section. Use horizontal images.
- **Every published game gets its own pages:** `/games/<name>/` plus `privacy`, `terms`, `support` and `delete-data`. The admin shows these links ready to paste into Play Console and App Store Connect.
- **Settings:** developer name, legal name, country, support email and the hero store buttons.

**Admin login.** The username and password only open the panel. Change them with `python3 tools/set_admin_password.py`; only a salted hash is stored. Publishing online also needs the GitHub token, once per browser, and that token is the real protection.

**How saving works.** The site has no server. Online, the admin commits your changes to this GitHub repository, then the host rebuilds the site (about a minute). You sign in with a GitHub fine-grained token that only has Contents read and write on this repository. It stays in your browser. On your computer (`tools/serve.py`) saving writes to `site/` directly, so you then push with git.

The generated privacy, terms and deletion pages are templates based on your answers. Check them against your Data safety form and have them reviewed if you need legal certainty.

## Google Play listing

Use these public URLs in Play Console:

| Field | URL |
|---|---|
| Privacy policy | Copy from the game in the admin panel |
| Terms | Copy from the game in the admin panel |
| Data deletion (if your game has accounts) | Copy from the game in the admin panel |
| Website | https://stonebuildgames.com |
| Support email | support@stonebuildgames.com |

Before you submit, make sure the game's privacy answers in the admin match your Play "Data safety" form.

## Deploy on Hostinger

`site/.htaccess` (generated) sets the security headers, HTTPS, caching and compression. Only the `site/` folder goes on the server, never the rest of this repository.

**Automatic, recommended.** Every push to `main` runs `.github/workflows/deploy.yml`, which builds the site and publishes it to the `deploy` branch.
1. In Hostinger: Websites, Manage, then Git / GitHub auto-deployment. Connect this repository, branch `deploy`, directory `public_html` (it must be empty the first time).
2. Turn on auto-deployment. Saving in the admin then goes live by itself.

**Manual.** Run `python3 tools/make_upload_zip.py`, upload `hostinger-upload.zip` to `public_html` in File Manager and extract it. Show hidden files to confirm `.htaccess` is there. With this route, online admin saves do not reach the server until you upload again.

**After deploy**
1. Turn on the free SSL certificate and force HTTPS in Hostinger, and turn on its CDN if your plan has it.
2. Submit `https://stonebuildgames.com/sitemap.xml` in Google Search Console and Bing Webmaster Tools.
3. IndexNow: the key file in `site/` is already in place. Ping `https://api.indexnow.org/indexnow?url=https://stonebuildgames.com/&key=<key>` (the key is the file name).

## Security checklist

The site is static: no database, no login server and no secrets on Hostinger. Keep it that way.
- Turn on two-factor login for GitHub and Hostinger. These two accounts are what really control the site.
- GitHub token: fine-grained, this repository only, Contents read and write, 90-day expiry. Revoke it at once if a computer is lost.
- Change the admin password to a long random one: `python3 tools/set_admin_password.py`.
- For an extra lock, add a server password to the `admin` folder in Hostinger, if your plan offers directory protection.

## Email: support@stonebuildgames.com

Free options: **Cloudflare Email Routing** (forward to your Gmail; sending needs a Gmail "send as" setup) or
**Zoho Mail Free** (real mailbox, 5 users). Paid: Google Workspace.
The contact form on the site opens the visitor's email client addressed to this mailbox, so it works with no backend.
If you later want a hosted form, point the form at Formspree or Netlify Forms and remove the mailto handler in `js/main.js`.

## Before launch: fill in the blanks

- Terms section 16 names no country. Add the country where the studio is registered.
- Consider adding founder name and country to the Organization schema in `site/index.html` once you want them public.
- If you deploy on Cloudflare, check that its AI-crawler blocking is off (it can override `robots.txt`).

## Customising

- Colors, fonts, spacing: `:root` tokens at the top of `site/css/styles.css`.
- Services, process steps, why-us copy: edit `site/index.html` directly (plain HTML).
- The hero 3D scene: `site/js/hero3d.js` (stone count, colors, speed).
- Home sections are one screen tall on desktop and scroll freely, with no snapping.
- The Stone Stack game lives in `site/js/game.js` (block size, swing and perfect-drop tolerance at the top of the file).
- Pages share the same header and footer. Change them in `tools/build_pages.py`, then run `python3 tools/build_pages.py`. Logos and icons come from `python3 tools/make_brand.py`.
- Everything respects `prefers-reduced-motion`.
