import re, json, os, sys, html, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from services_content import SERVICE_PAGES
# Generates every HTML page in site/ plus sitemap.xml. Run from anywhere: python3 tools/build_pages.py
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))
MARK='<svg class="brand-mark" viewBox="18 7 180 180" aria-hidden="true"><g stroke="#fff" stroke-width="3" stroke-linejoin="round"><polygon points="100,20 169.28,60 134.64,80 100,60 65.36,80 30.72,60" fill="#FF6A2B"/><polygon points="169.28,60 169.28,140 100,180 100,140 134.64,120 134.64,80" fill="#52525B"/><polygon points="30.72,60 65.36,80 65.36,120 100,140 100,180 30.72,140" fill="#0A0A0B"/><polygon points="100,100 134.64,120 100,140 65.36,120" fill="#9E411A"/><polygon points="100,60 100,100 65.36,120 65.36,80" fill="#27272A"/><polygon points="100,60 134.64,80 134.64,120 100,100" fill="#3F3F46"/><polygon points="172,14 185.86,22 172,30 158.14,22" fill="#FF6A2B"/><polygon points="172,30 185.86,22 185.86,38 172,46" fill="#52525B"/><polygon points="158.14,22 172,30 172,46 158.14,38" fill="#0A0A0B"/></g></svg>'
D='https://stonebuildgames.com'

with open('data/games.json') as _f: _D=json.load(_f)
_S=_D.get('settings',{})
_SOC=_S.get('social') or {}
SOCIAL_DEF=[('instagram','Instagram','<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="#E4405F" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="#E4405F" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.3" fill="#E4405F"/></svg>'),
 ('x','X','<svg viewBox="0 0 24 24" aria-hidden="true" fill="#0A0A0B"><path d="M17.8 3h3.1l-6.8 7.8 8 10.2h-6.3l-4.9-6.4L5.3 21H2.2l7.3-8.3L1.8 3h6.4l4.4 5.9zm-1.1 16.2h1.7L7 4.7H5.2z"/></svg>'),
 ('reddit','Reddit','<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="13.5" r="8.5" fill="#FF4500"/><ellipse cx="12" cy="14.5" rx="5.6" ry="3.9" fill="#fff"/><circle cx="9.7" cy="13.7" r="1.15" fill="#FF4500"/><circle cx="14.3" cy="13.7" r="1.15" fill="#FF4500"/><path d="M9.6 16.2c1.4 1 3.4 1 4.8 0" fill="none" stroke="#FF4500" stroke-width="1" stroke-linecap="round"/><path d="m12 6 1-3.3 3 .8" fill="none" stroke="#FF4500" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="17" cy="3.8" r="1.5" fill="#FF4500"/></svg>'),
 ('tiktok','TikTok','<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 3c.3 2.4 1.7 3.9 4 4.1v2.8c-1.5 0-2.8-.4-4-1.2v6.2a5.6 5.6 0 1 1-4.8-5.5v2.9a2.8 2.8 0 1 0 2 2.7V3z" fill="#25F4EE" transform="translate(-1 -.6)"/><path d="M15 3c.3 2.4 1.7 3.9 4 4.1v2.8c-1.5 0-2.8-.4-4-1.2v6.2a5.6 5.6 0 1 1-4.8-5.5v2.9a2.8 2.8 0 1 0 2 2.7V3z" fill="#FE2C55" transform="translate(1 .6)"/><path d="M15 3c.3 2.4 1.7 3.9 4 4.1v2.8c-1.5 0-2.8-.4-4-1.2v6.2a5.6 5.6 0 1 1-4.8-5.5v2.9a2.8 2.8 0 1 0 2 2.7V3z" fill="#0A0A0B"/></svg>'),
 ('linkedin','LinkedIn','<svg viewBox="0 0 24 24" aria-hidden="true" fill="#0A66C2"><path d="M6.9 21H3.1V8.6h3.8zM5 6.9A2.2 2.2 0 1 1 5 2.5a2.2 2.2 0 0 1 0 4.4zM21 21h-3.8v-6c0-1.4 0-3.3-2-3.3s-2.3 1.6-2.3 3.2V21H9.1V8.6h3.6v1.7h.1a4 4 0 0 1 3.6-2c3.8 0 4.6 2.5 4.6 5.8z"/></svg>'),
 ('youtube','YouTube','<svg viewBox="0 0 24 24" aria-hidden="true" fill="#FF0000"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23.5 12 31 31 0 0 0 23 7.2z"/><path fill="#fff" d="M9.8 15.1V8.9L15.8 12z"/></svg>')]
_soc_on=[(k,l,ic,_SOC[k]) for k,l,ic in SOCIAL_DEF if re.match(r'^https://[^\s"<>]+$',str(_SOC.get(k) or ''))]
SOCIAL_HTML=''.join(f'<a href="{html.escape(u,quote=True)}" target="_blank" rel="noopener me" aria-label="{l}" title="{l}">{ic}</a>' for k,l,ic,u in _soc_on)
STUDIO_SENTENCE='StoneBuild Games is an independent, remote game development studio that builds 3D, 2D and multiplayer games for Android, iOS and PC with Unity, Unreal Engine and Godot.'
def svg(path, sw='1.8', fill='none'):
    return f'<svg viewBox="0 0 24 24" fill="{fill}" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'
I={
 'arrow':svg('<path d="M5 12h14M13 6l6 6-6 6"/>','2'),
 'check':svg('<path d="m5 12 5 5L20 7"/>','2'),
 'chev':svg('<path d="m9 6 6 6-6 6"/>','2.2'),
 'home':svg('<path d="m3 11 9-8 9 8v9a2 2 0 0 1-2 2h-4v-6h-6v6H5a2 2 0 0 1-2-2z"/>'),
 'layers':svg('<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5M3 17l9 5 9-5"/>'),
 'users':svg('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M21.5 20a6.5 6.5 0 0 0-4.5-6.2"/>'),
 'gamepad':svg('<path d="M6 11h4M8 9v4M15 12h.01M18 10h.01M17.3 5H6.7a4 4 0 0 0-4 3.6l-.6 7A3 3 0 0 0 5.1 19c.9 0 1.7-.4 2.3-1l1.6-1.8h6l1.6 1.8c.6.6 1.4 1 2.3 1a3 3 0 0 0 3-3.4l-.6-7a4 4 0 0 0-4-3.6Z"/>'),
 'mail':svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
 'clock':svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 'globe':svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>'),
 'cube':svg('<path d="M12 2 21 7v10l-9 5-9-5V7z"/><path d="M12 12 21 7M12 12v10M12 12 3 7"/>'),
 'phone':svg('<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>'),
 'net':svg('<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/>'),
 'pen':svg('<path d="m3 21 9-9M14.5 4.5l5 5L8 21H3v-5z"/><path d="m16.5 2.5 5 5"/>'),
 'upload':svg('<path d="M12 3v12M8 11l4 4 4-4"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/>'),
 'zap':svg('<path d="M13 2 3 14h8l-1 8 11-14h-8z"/>'),
 'cal':svg('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M8 2v4M16 2v4"/>'),
 'shield':svg('<path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/><path d="m9 12 2 2 4-4"/>'),
 'key':svg('<path d="M20 7h-9M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/>'),
 'apple':'<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M16.4 12.6c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9-.7 0-1.9-.8-3.1-.8-1.6 0-3.1.9-3.9 2.4-1.7 2.9-.4 7.2 1.2 9.6.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.1-.8s1.9.8 3.1.8c1.3 0 2.1-1.2 2.9-2.3.9-1.3 1.3-2.6 1.3-2.7-.1 0-2.7-1-2.7-4.2zM14.1 5.8c.6-.8 1.1-1.8 1-2.8-.9 0-2 .6-2.7 1.4-.6.7-1.1 1.7-1 2.7 1 .1 2-.5 2.7-1.3z"/></svg>',
 'steam':svg('<circle cx="12" cy="12" r="9"/><circle cx="15" cy="10" r="2.5"/><circle cx="8.5" cy="15" r="1.8"/><path d="m10 14 3.2-2.4"/>'),
 'star':'<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="m12 2.8 2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3.1-5.8 3.1 1.1-6.5L2.6 9.6l6.5-.9z"/></svg>',
 'doc':svg('<path d="M6 2h9l4 4v16H6z"/><path d="M15 2v4h4M9 12h7M9 16h7"/>'),
 'help':svg('<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.3-1 .8-1 1.7M12 17h.01"/>'),
 'video':svg('<rect x="3" y="6" width="18" height="12" rx="2"/><path d="m10 9.5 5 2.5-5 2.5z"/>'),
 'bug':svg('<path d="M8 2l1.9 1.9M16 2l-1.9 1.9M9 7h6a3 3 0 0 1 3 3v4a6 6 0 0 1-12 0v-4a3 3 0 0 1 3-3zM3 13h3M18 13h3M4 20l3-2M20 20l-3-2M4 6l3 2M20 6l-3 2"/>'),
 'trash':svg('<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>'),
 'play':'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#34a853" d="M3.6 2.4 13.3 12l-9.7 9.6c-.4-.2-.6-.7-.6-1.3V3.7c0-.6.2-1.1.6-1.3z"/><path fill="#4285f4" d="M16.6 8.7 13.3 12l3.3 3.3 3.9-2.2c1.1-.6 1.1-1.6 0-2.2z"/><path fill="#fbbc04" d="M3.6 2.4c.3-.2.8-.2 1.3.1l11.7 6.2L13.3 12z"/><path fill="#ea4335" d="M13.3 12 3.6 21.6c.3.2.8.2 1.3-.1l11.7-6.2z"/></svg>',
 'playmono':svg('<path d="M4 3.5v17l14-8.5z"/>'),
 'yt':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23.5 12 31 31 0 0 0 23 7.2zM9.8 15.1V8.9L15.8 12z"/></svg>',
 'ig':svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>'),
 'x':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.8 3h3.1l-6.8 7.8 8 10.2h-6.3l-4.9-6.4L5.3 21H2.2l7.3-8.3L1.8 3h6.4l4.4 5.9zm-1.1 16.2h1.7L7 4.7H5.2z"/></svg>',
 'in':'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.9 21H3.1V8.6h3.8zM5 6.9A2.2 2.2 0 1 1 5 2.5a2.2 2.2 0 0 1 0 4.4zM21 21h-3.8v-6c0-1.4 0-3.3-2-3.3s-2.3 1.6-2.3 3.2V21H9.1V8.6h3.6v1.7h.1a4 4 0 0 1 3.6-2c3.8 0 4.6 2.5 4.6 5.8z"/></svg>',
}
NAV=[('/','Home','home'),('/services/','Services','layers'),('/about/','About','users'),('/games/','Games','gamepad'),('/contact/','Contact','mail')]
FONTS='''  <link rel="preload" href="/fonts/chakrapetch-700-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/css/fonts.css">'''

def head(title, desc, path, ld, robots='index, follow, max-image-preview:large', canonical=True):
    can=f'\n  <link rel="canonical" href="{D}{path}">' if canonical else ''
    ldblock=f'\n  <script type="application/ld+json">\n{json.dumps(ld, indent=2, ensure_ascii=False)}\n  </script>' if ld else ''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">{can}
  <meta name="theme-color" content="#ffffff">
  <meta name="robots" content="{robots}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="StoneBuild Games">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{D}{path}">
  <meta property="og:image" content="{D}/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="StoneBuild Games mined-block logo with the words Building worlds worth playing.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{D}/assets/og-image.png">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
{FONTS}
  <link rel="stylesheet" href="/css/styles.css">
  <script>document.documentElement.classList.add('js');setTimeout(function(){{document.documentElement.classList.add('reveal-ready')}},1200)</script>{ldblock}
</head>
<body>
'''

def header(path):
    parts=[]
    for h,n,ic in NAV:
        cur=' aria-current="page"' if h==path else ''
        parts.append(f'<a href="{h}"{cur}>{I[ic]}{n}</a>')
    return f'''  <a class="skip-link" href="#main">Skip to content</a>
  <div class="bg-glow" aria-hidden="true"></div>
  <div class="bg-noise" aria-hidden="true"></div>

  <header class="site-header" id="top">
    <div class="header-inner">
      <a class="brand" href="/">{MARK}<span class="brand-name"><span class="brand-top">Stone Build</span><span class="brand-sub">Games</span></span></a>
      <nav class="nav" id="nav" aria-label="Primary">{''.join(parts)}</nav>
      <div class="header-actions">
        <a class="btn btn-primary btn-sm" href="/contact/">Start a project</a>
        <button class="nav-toggle" aria-controls="nav" aria-expanded="false" aria-label="Menu"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>
'''

FMARK=MARK
FOOTER=f'''  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <a class="brand" href="/">{FMARK}<span class="brand-name"><span class="brand-top">Stone Build</span><span class="brand-sub">Games</span></span></a>
          <p>Independent, remote game development studio building 3D, 2D and multiplayer games for Android, iOS and PC.</p>
          <div class="socials" aria-label="Social links">{SOCIAL_HTML}<a class="s-mail" href="mailto:support@stonebuildgames.com" aria-label="Email us" title="Email">{I['mail']}</a></div>
        </div>
        <div>
          <p class="footer-h">Studio</p>
          <ul>
            <li><a href="/services/">{I['chev']}Services</a></li>
            <li><a href="/about/">{I['chev']}About</a></li>
            <li><a href="/about/#process">{I['chev']}How we work</a></li>
            <li><a href="/contact/">{I['chev']}Contact</a></li>
          </ul>
        </div>
        <div>
          <p class="footer-h">Games &amp; legal</p>
          <ul>
            <li><a href="/games/">{I['chev']}All games</a></li>
            <li><a href="/#play">{I['chev']}Play Stone Stack</a></li>
            <li><a href="/privacy-policy/">{I['chev']}Privacy policy</a></li>
            <li><a href="/terms/">{I['chev']}Terms &amp; conditions</a></li>
          </ul>
        </div>
        <div>
          <p class="footer-h">Support</p>
          <ul>
            <li><a href="mailto:support@stonebuildgames.com">{I['mail']}support@stonebuildgames.com</a></li>
            <li><a href="mailto:support@stonebuildgames.com?subject=Bug%20report">{I['bug']}Report a bug</a></li>
            <li><a href="/privacy-policy/#data-deletion">{I['trash']}Data deletion request</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-giant" aria-hidden="true">Stone <span>Build</span></div>
      <div class="footer-bottom">
        <span>© <span id="year">2026</span> StoneBuild Games. All rights reserved.</span>
        <span><a href="/privacy-policy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/sitemap.xml">Sitemap</a></span>
      </div>
    </div>
  </footer>
'''
SCRIPTS='''  <script src="/vendor/gsap.min.js" defer></script>
  <script src="/vendor/ScrollTrigger.min.js" defer></script>
  <script src="/js/main.js" defer></script>
'''
ORG={"@type":"Organization","@id":f"{D}/#organization","name":"StoneBuild Games","alternateName":"StoneBuild","url":f"{D}/",
 "logo":{"@type":"ImageObject","@id":f"{D}/#logo","url":f"{D}/assets/logo-512.png","contentUrl":f"{D}/assets/logo-512.png","width":512,"height":512,"caption":"StoneBuild Games logo"},
 "description":STUDIO_SENTENCE,"email":"support@stonebuildgames.com",
 "contactPoint":[{"@type":"ContactPoint","email":"support@stonebuildgames.com","contactType":"customer service","availableLanguage":["English"]},{"@type":"ContactPoint","email":"support@stonebuildgames.com","contactType":"sales","availableLanguage":["English"],"areaServed":"Worldwide"}],
 "knowsAbout":["Game development","Unity","Unreal Engine","Godot","3D game development","Mobile games","Multiplayer games"]}
if _soc_on: ORG['sameAs']=[u for *_,u in _soc_on]
WEBSITE={"@type":"WebSite","@id":f"{D}/#website","url":f"{D}/","name":"StoneBuild Games","alternateName":"StoneBuild","description":"Game development studio for 3D, 2D and multiplayer games.","publisher":{"@id":f"{D}/#organization"},"inLanguage":"en"}
def webpage(path,title,desc,typ='WebPage',extra=None):
    p={"@type":typ,"@id":f"{D}{path}#webpage","url":f"{D}{path}","name":title,"description":desc,"inLanguage":"en","isPartOf":{"@id":f"{D}/#website"},"publisher":{"@id":f"{D}/#organization"}}
    if path!='/': p["breadcrumb"]={"@id":f"{D}{path}#breadcrumb"}
    if extra: p.update(extra)
    return p
def crumbs(path,name):
    return {"@type":"BreadcrumbList","@id":f"{D}{path}#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":f"{D}/"},{"@type":"ListItem","position":2,"name":name,"item":f"{D}{path}"}]}
SERVICES=[
 ('gamepad','Full-Cycle Game Development','Full-cycle game development: concept, design doc, prototype, production and release. One team owns the game from first build to storefront.',['Unity','Unreal','Godot'],['Game design document and scope plan','Playable prototype before full production','Production in two-week sprints with builds','Store submission and launch support']),
 ('cube','3D Game Development','3D game development with stylized or realistic worlds, custom shaders, lighting and physics, tuned to run smoothly on mid-range phones.',['PBR','Shaders','Optimization'],['Environment, character and prop pipelines','Custom shaders, lighting and post-processing','Physics, cameras and controller feel','Draw-call, memory and battery optimization']),
 ('phone','Mobile, 2D &amp; Casual Games','Mobile game development for Android and iOS: fast prototypes, tight game feel and retention loops, with ads and in-app purchases wired in cleanly.',['Android','iOS','Monetization'],['Rapid prototypes in days, not months','Juice: tweens, particles, haptics, sound','Ads mediation and in-app purchases','Analytics and A/B testing hooks']),
 ('net','Multiplayer &amp; Backend','Multiplayer and backend development: real-time netcode, matchmaking, leaderboards, cloud saves and server-side logic that scales with your player base.',['Netcode','Photon','Firebase'],['Real-time and turn-based multiplayer','Matchmaking, lobbies and friends','Leaderboards, achievements, cloud saves','Server-authoritative logic and anti-cheat']),
 ('pen','Game Art &amp; Animation','Game art and animation: characters, environments, UI and VFX in one consistent style, rigged and animated to feel alive in-engine.',['Blender','Rigging','VFX'],['Concept art and style guides','3D modelling, texturing and rigging','UI/UX for small screens','VFX and in-engine animation']),
 ('upload','Porting, QA &amp; Publishing','Porting, QA and publishing: store-ready builds, device testing, policy compliance and launch support for Google Play, the App Store and Steam, plus LiveOps.',['Google Play','App Store','Steam'],['Porting between mobile, PC and web','Device-matrix QA and performance passes','Privacy policy, data safety and age ratings','Store listings, soft launch and LiveOps']),
]
def service_card(i,s,full=False):
    ic,title,desc,tags,bullets=s
    body=f'<ul>{"".join(f"<li>{b}</li>" for b in bullets)}</ul>' if full else ''
    return f'''          <article class="card service tilt reveal">
            <span class="num">0{i+1}</span>
            <div class="icon">{I[ic]}</div>
            <h3>{title}</h3>
            <p>{desc}</p>{body}
            <div class="tags">{" ".join(f'<span class="tag">{t}</span>' for t in tags)}</div>
            <a class="card-link" href="/services/{SERVICE_PAGES[i]['slug']}/">View service {I['arrow']}</a>
          </article>
'''
PROCESS=[('Discovery','We define the core loop, target players, platforms and scope, then agree on a plan and a budget.','First days'),('Prototype','A playable vertical slice that proves the fun before we commit to full production.','About 1 week'),('Production','Two-week sprints. Art, code and design land together, with a new build in your hands every sprint.','Sprint based'),('Polish &amp; QA','Device testing, performance passes, balancing and store policy checks until the game is release-ready.','Final sprints'),('Launch &amp; LiveOps','Store listings, soft launch, analytics and the updates that keep players coming back.','Ongoing')]
SHORT=[('gamepad','Full-cycle development','Concept, prototype, production and release, with one team from first build to storefront.'),('cube','3D games','Stylized or realistic worlds, custom shaders and physics, tuned for mid-range phones.'),('phone','Mobile and casual games','Fast prototypes, tight game feel, and ads and in-app purchases wired in cleanly.'),('net','Multiplayer and backend','Real-time netcode, matchmaking, leaderboards and cloud saves that scale with your players.'),('pen','Game art and animation','Characters, environments, UI and VFX in one style, animated to feel alive in-engine.'),('upload','Porting, QA and publishing','Store-ready builds, device testing and policy compliance for Google Play, App Store and Steam.')]
SVC_SLUGS=[p['slug'] for p in SERVICE_PAGES]
HOME_SERVICES=''.join(f'''          <a class="svc reveal" href="/services/{SVC_SLUGS[n]}/">
            <div class="svc-top"><div class="icon">{I[ic]}</div><span class="num">0{n+1}</span></div>
            <h3>{t}</h3>
            <p>{d}</p>
          </a>
''' for n,(ic,t,d) in enumerate(SHORT))
def process_html():
    return '<ol class="process">'+''.join(f'<li class="step reveal"><span class="node">{i+1}</span><h3>{t}</h3><p>{p}</p><span class="dur">{d}</span></li>' for i,(t,p,d) in enumerate(PROCESS))+'</ol>'
WHY=[('zap','Performance first','We target a stable 60 fps on mid-range Android phones, small download sizes and fast first loads, and we measure them on real devices every sprint.'),('cal','A build every sprint','Two-week sprints with a playable build and a written changelog each time. You always know where the game stands.'),('shield','Store compliance built in','Privacy policies, data safety forms, age ratings and content rules are handled during production, so launch day is not a surprise.'),('key','You own everything','Source code, art files and store accounts stay in your name. Clear contracts, clear IP, no lock-in.')]
def why_list(cls='why-list'):
    return f'<ul class="{cls}">'+''.join(f'<li class="card why-item reveal"><div class="icon">{I[ic]}</div><div><h3>{t}</h3><p>{p}</p></div></li>' for ic,t,p in WHY)+'</ul>'
TECH=['Unity','Unreal Engine','Godot','C#','C++','Blender','Firebase','Photon','Play Games Services','AdMob']
MARQUEE='<div class="marquee reveal" aria-label="Technologies we use"><div class="marquee-track">'+''.join(f'<span class="marquee-item"><i></i>{t}</span>' for t in TECH)+''.join(f'<span class="marquee-item" aria-hidden="true"><i></i>{t}</span>' for t in TECH)+'</div></div>'
CTA=f'''      <div class="card cta-band reveal">
        <div><h2>Have a game in mind?</h2><p>Tell us about it. We reply within two business days with questions, a rough scope and next steps.</p></div>
        <div class="actions"><a class="btn btn-primary btn-lg" href="/contact/">Start a project {I['arrow']}</a><a class="btn btn-ghost btn-lg" href="mailto:support@stonebuildgames.com">Email us</a></div>
      </div>
'''
FAQ=[
 ('What does a game development studio do?','A game development studio designs, builds, tests and ships games. StoneBuild Games covers the whole cycle: game design, programming in Unity, Unreal Engine or Godot, art and animation, multiplayer and backend, QA on real devices, and publishing on Google Play, the App Store and Steam.'),
 ('How long does it take to build a mobile game?','A playable prototype takes about one week after discovery. A small casual game can ship in two to three months of two-week sprints; a 3D or multiplayer game usually takes longer. We give a dated plan after discovery.'),
 ('How much does it cost to develop a game?','It depends on scope. Our inquiry form uses four ranges: under $5k for a prototype or a small feature, $5k to $15k for a casual mobile game, $15k to $50k for a mid-size 3D or multiplayer title, and $50k+ for larger productions. Every quote follows a written scope.'),
 ('Who owns the source code and art?','You do. Source code, art files, design documents and store accounts stay in your name, and the contract says so. There is no lock-in.'),
 ('Which engines and platforms do you work with?','Unity, Unreal Engine and Godot, in 2D and 3D, for Android, iOS, PC (Steam) and the web. Backend work uses Firebase, Photon and Google Play Games Services.'),
 ('Where is StoneBuild Games based?','StoneBuild Games is a remote studio and works with clients worldwide over email and video calls. Reach us at support@stonebuildgames.com; we reply within two business days.'),
]
def faq_html(items):
    out=[]
    for n,(q,a) in enumerate(items):
        op=' open' if n==0 else ''
        out.append(f'<details class="faq-item"{op}><summary><span>{q}</span><i aria-hidden="true"></i></summary><div class="faq-a"><p>{a}</p></div></details>')
    return '<div class="faq-list">'+''.join(out)+'</div>'
def faq_section(items, title='Frequently asked questions', intro='Short answers to what studios and founders ask us first. Anything else, just email us.', cls='alt'):
    return f'''    <section class="page-section {cls}" aria-labelledby="faq-title">
      <div class="container faq-layout">
        <div class="faq-head">
          <span class="eyebrow reveal">Questions</span>
          <h2 id="faq-title" class="reveal">{title}</h2>
          <p class="lead reveal">{intro}</p>
          <a class="link-arrow reveal" href="/contact/">Ask us something else {I['arrow']}</a>
        </div>
        <div class="reveal">{faq_html(items)}</div>
      </div>
    </section>
'''

def page_hero(crumb, eyebrow, h1, lead, meta=''):
    return f'''    <section class="page-hero" aria-labelledby="page-title">
      <div class="container">
        <nav aria-label="Breadcrumb" class="reveal"><ol class="breadcrumbs"><li><a href="/">Home</a></li><li aria-current="page">{crumb}</li></ol></nav>
        <span class="eyebrow reveal">{eyebrow}</span>
        <h1 id="page-title" class="reveal">{h1}</h1>
        <p class="lead reveal">{lead}</p>{meta}
      </div>
    </section>
'''
# (kind, size, small-screen size, side, offset from side, top, duration, delay, hide on phones)
ROCK_SETS=[
 [(1,240,110,'r','-140px','10%',19,0,0),(4,64,44,'l','14px','30%',14,-4,1),(5,150,80,'l','-92px','68%',23,-9,1)],
 [(2,260,120,'l','-165px','22%',21,-3,0),(5,110,70,'r','-46px','14%',17,-6,1),(3,170,84,'r','-108px','68%',16,-2,0)],
 [(3,220,110,'r','-135px','52%',22,-5,0),(4,60,44,'l','16px','18%',13,-1,1),(1,180,90,'l','-118px','70%',18,-7,1)],
 [(5,160,84,'r','-92px','16%',20,-2,1),(2,200,100,'l','-128px','46%',17,-8,0),(4,70,48,'r','16px','80%',15,-3,1)],
]
rock_i=[0]
def rock_html(path=''):
    # Long legal text stays clean: rocks only in its header
    st=ROCK_SETS[rock_i[0]%len(ROCK_SETS)]; rock_i[0]+=1; out=[]
    for k,sz,sm,side,off,top,t,d,h in st:
        pos=f'--x:{off}' if side=='l' else f'--xr:{off}'
        out.append(f'<div class="rock k{k}{" hide-m" if h else ""}" style="--s:{sz}px;--sm:{sm}px;{pos};--y:{top};--t:{t}s;--d:{d}s"><i></i></div>')
    return '<div class="rocks" aria-hidden="true">'+''.join(out)+'</div>'
def add_rocks(html):
    rock_i[0]=0
    html=re.sub(r'<div class="rocks" aria-hidden="true">.*?</div></div>\s*(?=<div class="|<ol|\s)', '', html) if False else html
    html=re.sub(r'<div class="rocks" aria-hidden="true">(?:<div class="rock[^>]*><i></i></div>)*</div>', '', html)
    pat=r'(<section class="(?:screen(?! hero)|page-hero|page-section)[^"]*"[^>]*>)'
    return re.sub(pat, lambda m: m.group(1)+rock_html(), html)
def write(path_file, html):
    os.makedirs(os.path.dirname(path_file) or '.', exist_ok=True)
    if path_file.endswith('.html'): html=add_rocks(html)
    open(path_file,'w').write(html)
def dots(items):
    out=[]
    for n,(i,l) in enumerate(items):
        cls=' class="is-active"' if n==0 else ''
        out.append(f'<a href="#{i}" data-label="{l}" aria-label="Go to {l} section"{cls}></a>')
    return '<nav class="dots" aria-label="Sections">'+''.join(out)+'</nav>'


# ====================== GAME DATA ======================
E=lambda v: html.escape(str(v if v is not None else ''), quote=True)
with open('data/games.json') as _f: DATA=json.load(_f)
SET=DATA.get('settings',{})
DEV=SET.get('developerName') or 'StoneBuild Games'
EMAIL=SET.get('supportEmail') or 'support@stonebuildgames.com'
def good_url(u): return bool(re.match(r'^https://[^\s"<>]+$', str(u or '')))
def asset_ok(u): return bool(re.match(r'^/assets/games/[a-z0-9-]+/[a-z0-9._-]+$', str(u or '')))
GAMES=[g for g in DATA.get('games',[]) if g.get('status')=='published' and re.match(r'^[a-z0-9-]+$', g.get('id',''))]
def badge(url, icon, small, label):
    return f'<a class="store-badge" href="{E(url)}" target="_blank" rel="noopener">{I[icon]}<span><small>{small}</small>{label}<span class="sr-only"> (opens in a new tab)</span></span></a>'
def store_links(g):
    out=[]
    if g.get('playOn') and good_url(g.get('playUrl')): out.append(('play',g['playUrl'],'GET IT ON','Google Play'))
    if g.get('appStoreOn') and good_url(g.get('appStoreUrl')): out.append(('apple',g['appStoreUrl'],'Download on the','App Store'))
    if g.get('steamOn') and good_url(g.get('steamUrl')): out.append(('steam',g['steamUrl'],'Available on','Steam'))
    return out
def store_badges(g): return ''.join(badge(u,ic,sm,l) for ic,u,sm,l in store_links(g))
def hero_store(url, icon, label):
    if good_url(url): return badge(url,icon,'GET IT ON' if icon=='play' else 'Download on the',label)
    return f'<a class="store-badge soon" href="/games/">{I[icon]}<span><small>COMING TO</small>{label}</span></a>'
HERO_STORES=hero_store(SET.get('playDeveloperUrl'),'play','Google Play')+hero_store(SET.get('appStoreDeveloperUrl'),'apple','App Store')
CUBE='<svg viewBox="154 10 36 40"><g stroke="#fff" stroke-width="2" stroke-linejoin="round"><polygon points="172,14 185.86,22 172,30 158.14,22" fill="#FF6A2B"/><polygon points="172,30 185.86,22 185.86,38 172,46" fill="#52525B"/><polygon points="158.14,22 172,30 172,46 158.14,38" fill="#0A0A0B"/></g></svg>'
def game_card(g, rv=' reveal'):
    img=f'<img src="{E(g["cover"])}" alt="{E(g["name"])} cover art" loading="lazy" width="1440" height="600">' if asset_ok(g.get('cover')) else '<div class="art"></div>'
    links=store_links(g); first=''
    if links:
        ic,u,_,l=links[0]
        first=f'<a class="btn btn-primary btn-sm" href="{E(u)}" target="_blank" rel="noopener">{I[ic]}{l}<span class="sr-only"> (opens in a new tab)</span></a>'
    return f'''<article class="gc{rv}">{img}<div class="gc-over"><h3>{E(g["name"])}</h3><div class="gc-actions">{first}<a class="btn btn-light btn-sm" href="/games/{E(g["id"])}/">Explore {I['arrow']}</a></div></div></article>'''
def game_grid(items):
    # Same box grid as the services section; a last cell fills any gap in the final row
    left=(3-len(items)%3)%3
    fill=f'<a class="gc-more reveal" href="/games/" style="grid-column:span {left}">More games coming. See all games {I["arrow"]}</a>' if left else ''
    return '<div class="gc-grid">'+''.join(game_card(g) for g in items)+fill+'</div>'
HOME_GAMES=''
if len(GAMES)>=4:
    cards=game_grid(GAMES[:6])
    HOME_GAMES=f'''    <!-- GAMES (shown once at least four games are published) -->
    <section class="screen" id="games" aria-labelledby="games-title">
      <div class="container">
        <div class="section-head split">
          <span class="eyebrow reveal">Our games</span>
          <h2 id="games-title" class="reveal">Games we have built</h2>
          <p class="lead reveal">Our own titles, made with the same team and pipeline we use for client work.</p>
          <a class="link-arrow head-link reveal" href="/games/">See all games {I['arrow']}</a>
        </div>
        {cards}
      </div>
    </section>

'''
SDKS={'admob':('Google AdMob','Shows advertising and measures it','https://policies.google.com/technologies/ads'),'unityads':('Unity Ads','Shows advertising and measures it','https://unity.com/legal/game-player-and-app-user-privacy-policy'),'firebase':('Google Firebase','Analytics, crash reports and remote settings','https://firebase.google.com/support/privacy'),'unityanalytics':('Unity Analytics','Gameplay analytics','https://unity.com/legal/game-player-and-app-user-privacy-policy'),'gpgs':('Google Play Games Services','Sign-in, achievements, leaderboards and cloud saves','https://policies.google.com/privacy'),'gamecenter':('Apple Game Center','Sign-in, achievements and leaderboards','https://www.apple.com/legal/privacy/')}
def fmt_date(d):
    m=re.match(r'^(\d{4})-(\d{2})-(\d{2})',str(d or ''))
    if not m: return ''
    return ['January','February','March','April','May','June','July','August','September','October','November','December'][int(m.group(2))-1]+f' {int(m.group(3))}, {m.group(1)}'
def crumbs3(items):
    return {"@type":"BreadcrumbList","@id":f"{D}{items[-1][1]}#breadcrumb","itemListElement":[{"@type":"ListItem","position":n+1,"name":a,"item":f"{D}{b}"} for n,(a,b) in enumerate(items)]}
def crumb_html(items):
    out=[]
    for n,(a,b) in enumerate(items):
        if n==len(items)-1: out.append(f'<li aria-current="page">{a}</li>')
        else: out.append(f'<li><a href="{b}">{a}</a></li>')
    return '<nav aria-label="Breadcrumb" class="reveal"><ol class="breadcrumbs">'+''.join(out)+'</ol></nav>'
def page(path,file,title,desc,ld,body,current='/games/'):
    write(file, head(title,desc,path,ld)+header(current)+'\n  <main id="main">\n'+body+'  </main>\n'+FOOTER+SCRIPTS+'</body>\n</html>\n')
def game_legal_nav(g,cur):
    base=f'/games/{E(g["id"])}'
    items=[('Privacy policy',base+'/privacy/','privacy'),('Terms',base+'/terms/','terms'),('Support',base+'/support/','support'),('Delete my data',base+'/delete-data/','delete')]
    return '<nav class="legal-tabs" aria-label="Game information"><a href="'+base+'/">'+E(g['name'])+'</a>'+''.join(f'<a href="{u}"'+(' aria-current="page"' if k==cur else '')+f'>{t}</a>' for t,u,k in items)+'</nav>'
def legal_shell(g,kind,h1,lead,content,desc):
    path=f'/games/{g["id"]}/'+{'privacy':'privacy','terms':'terms','support':'support','delete':'delete-data'}[kind]+'/'
    title=f'{h1} | {DEV}'
    crumbs=[('Home','/'),('Games','/games/'),(E(g['name']),f'/games/{g["id"]}/'),(E(h1.replace(g['name'],'').strip()) or E(h1),path)]
    ld={"@context":"https://schema.org","@graph":[webpage(path,title,desc,extra={"dateModified":g.get('updated') or TODAY}),crumbs3([(html.unescape(a),b) for a,b in crumbs])]}
    updated=fmt_date(g.get('updated') or TODAY)
    body=f'''    <section class="page-hero" aria-labelledby="page-title">
      <div class="container">
        {crumb_html(crumbs)}
        <h1 id="page-title" class="reveal">{E(h1)}</h1>
        <p class="lead reveal">{lead}</p>
        <p class="meta reveal">Last updated: {updated}</p>
      </div>
    </section>
    <section class="page-body">
      <div class="container">
        {game_legal_nav(g,kind)}
        <article class="prose">{content}</article>
      </div>
    </section>
'''
    page(path,f'games/{g["id"]}/'+path.split('/')[-2]+'/index.html',E(title),E(desc),ld,body)
def write_game(g):
    name=E(g['name']); nm=g['name']; gid=g['id']; base=f'/games/{gid}'
    os.makedirs(f'games/{gid}',exist_ok=True)
    who=E(SET.get('legalName') or DEV); country=E(SET.get('country') or '')
    where=f', {country}' if country else ''
    mail=E(EMAIL)
    mailto=lambda subj: f'mailto:{mail}?subject='+html.escape(subj.replace(' ','%20').replace('&','and'),quote=True)
    # ---- game page ----
    stats=[]
    if g.get('rating'):
        cnt=f'<span>{E(g["ratingCount"])} ratings</span>' if g.get('ratingCount') else '<span>Store rating</span>'
        stats.append(f'<div class="gstat"><b>{I["star"]}{E(g["rating"])}</b>{cnt}</div>')
    if g.get('downloads'): stats.append(f'<div class="gstat"><b>{E(g["downloads"])}</b><span>Downloads</span></div>')
    if g.get('ageRating'): stats.append(f'<div class="gstat"><b>{E(g["ageRating"])}</b><span>Age rating</span></div>')
    if g.get('genre'): stats.append(f'<div class="gstat"><b>{E(g["genre"])}</b><span>Genre</span></div>')
    badges=store_badges(g) or '<span class="status">Coming soon</span>'
    trailer=f'<a class="btn btn-ghost" href="{E(g["trailer"])}" target="_blank" rel="noopener">{I["video"]}Watch trailer</a>' if good_url(g.get('trailer')) else ''
    icon=f'<img class="g-icon" src="{E(g["icon"])}" alt="{name} icon" width="96" height="96">' if asset_ok(g.get('icon')) else ''
    cover=f'<img class="g-cover" src="{E(g["cover"])}" alt="{name} cover art" width="1440" height="600">' if asset_ok(g.get('cover')) else ''
    shots=[u for u in g.get('screenshots',[]) if asset_ok(u)]
    shots_html=''
    if shots:
        imgs=''.join(f'<img src="{E(u)}" alt="{name} screenshot {n+1}" loading="lazy">' for n,u in enumerate(shots))
        shots_html=f'''    <section class="page-section alt" aria-labelledby="shots-title"><div class="container"><h2 id="shots-title" class="reveal g-h2">Screenshots</h2></div><div class="g-shots reveal" tabindex="0">{imgs}</div></section>
'''
    paras=''.join(f'<p>{E(x.strip())}</p>' for x in re.split(r'\n\s*\n|\n',g.get('description','')) if x.strip())
    feats=[f for f in g.get('features',[]) if str(f).strip()]
    feats_html=('<h3>Features</h3><ul class="g-feats">'+''.join(f'<li>{I["check"]}<span>{E(f)}</span></li>' for f in feats)+'</ul>') if feats else ''
    rows=[('Developer',E(DEV)),('Genre',E(g.get('genre'))),('Platforms',E(', '.join(g.get('platforms',[])))),('Version',E(g.get('version'))),('Updated',fmt_date(g.get('updated'))),('Released',fmt_date(g.get('released'))),('Size',E(g.get('size'))),('Age rating',E(g.get('ageRating'))),('Contains ads','Yes' if g.get('ads') else 'No'),('In-app purchases','Yes' if g.get('iap') else 'No')]
    table=''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a,b in rows if b)
    legal=[('Privacy policy',base+'/privacy/','shield'),('Terms of use',base+'/terms/','doc'),('Support',base+'/support/','help'),('Delete my data',base+'/delete-data/','trash')]
    legal_html=''.join(f'<a class="g-legal" href="{u}">{I[ic]}<span>{t}</span>{I["arrow"]}</a>' for t,u,ic in legal)
    desc=(g.get('tagline') or re.sub(r'\s+',' ',g.get('description',''))[:150]).strip()
    os_map={'Android':'Android','iOS':'iOS','PC':'Windows','Web':'Web browser'}
    ldgame={"@type":"VideoGame","@id":f"{D}{base}/#game","name":nm,"url":f"{D}{base}/","description":re.sub(r'\s+',' ',g.get('description',desc))[:500],"author":{"@id":f"{D}/#organization"},"publisher":{"@id":f"{D}/#organization"},"applicationCategory":"GameApplication"}
    if g.get('genre'): ldgame['genre']=g['genre']
    if g.get('platforms'): ldgame['gamePlatform']=g['platforms']; ldgame['operatingSystem']=', '.join(os_map.get(x,x) for x in g['platforms'])
    if asset_ok(g.get('cover')): ldgame['image']=D+g['cover']
    if g.get('released'): ldgame['datePublished']=g['released']
    lnk=[u for _,u,_,_ in store_links(g)]
    if lnk: ldgame['sameAs']=lnk; ldgame['installUrl']=lnk[0]
    crumbs=[('Home','/'),('Games','/games/'),(nm,base+'/')]
    title=f'{nm} | {DEV}'
    ld={"@context":"https://schema.org","@graph":[webpage(base+'/',title,desc),crumbs3(crumbs),ldgame]}
    body=f'''    <section class="page-hero g-hero" aria-labelledby="page-title">
      <div class="container g-hero-grid">
        <div class="g-hero-copy">
          {crumb_html([(E(a),b) for a,b in crumbs])}
          <div class="g-title reveal">{icon}<div><h1 id="page-title">{name}</h1><p class="g-dev">{E(DEV)}</p></div></div>
          <p class="lead reveal">{E(g.get("tagline"))}</p>
          <div class="g-stats reveal">{''.join(stats)}</div>
          <div class="store-row reveal">{badges}{trailer}</div>
        </div>
        <div class="reveal">{cover}</div>
      </div>
    </section>
{shots_html}    <section class="page-section" aria-labelledby="about-title">
      <div class="container g-about">
        <div class="prose"><h2 id="about-title" class="reveal">About {name}</h2><div class="reveal">{paras}{feats_html}</div></div>
        <aside class="card g-details reveal" aria-label="Game details"><p class="toc-title">Details</p><dl>{table}</dl></aside>
      </div>
    </section>
    <section class="page-section page-body alt" aria-labelledby="info-title">
      <div class="container"><h2 id="info-title" class="reveal g-h2">Player information</h2><div class="g-legal-grid reveal">{legal_html}</div></div>
    </section>
'''
    page(base+'/',f'games/{gid}/index.html',E(title),E(desc),ld,body)
    # ---- privacy policy ----
    used=[SDKS[k] for k in g.get('sdks',[]) if k in SDKS]
    collects=['<li><strong>Gameplay data:</strong> progress, scores and settings, used to run the game and save your progress.</li>']
    if used: collects.append('<li><strong>Device and diagnostic data:</strong> device model, operating system, language, crash reports and performance data, used to keep the game working and fix bugs.</li>')
    if g.get('ads'): collects.append('<li><strong>Advertising identifiers:</strong> your device advertising ID, where you allow it, used to show and measure ads and limit repeats.</li>')
    if g.get('iap'): collects.append('<li><strong>Purchase records:</strong> which item you bought and a confirmation from the store. The store handles payment, and we never receive your card details.</li>')
    if g.get('accounts'): collects.append('<li><strong>Account data:</strong> your player name and account identifier, used to sign you in and restore your progress.</li>')
    tp=''.join(f'<li><strong>{a}:</strong> {b}. <a href="{u}" rel="noopener">Privacy policy</a></li>' for a,b,u in used)
    tp_html=(f'<p>{name} uses these third-party services, which may receive the data they need for the purpose shown:</p><ul>{tp}</ul><p>We only use providers that commit to protecting user data to a standard equal to this policy and to the rules of the app stores. We do not sell your personal information.</p>') if used else f'<p>{name} does not use third-party analytics, advertising or sign-in services. We do not sell or share your personal information.</p>'
    ads_html=f'<h2 id="ads">Advertising choices</h2><p>{name} shows ads. You can turn off personalised ads in your device settings. On Android, open Settings, then Google, then Ads. On iOS, open Settings, then Privacy and Security, then Tracking.</p>' if g.get('ads') else ''
    kids=f'<p>{name} is designed to be suitable for children. We do not knowingly collect personal information from children beyond what the game needs to work, and any services used are configured for child-directed use.</p>' if g.get('children') else f'<p>{name} is not directed to children under 13, or the minimum age in your country. If you believe a child has given us personal information, contact us and we will delete it.</p>'
    acct=f'<p>If you have an account, you can ask us to delete the account and its data. Follow the steps on the <a href="{base}/delete-data/">delete my data page</a>. You do not need to reinstall the game.</p>' if g.get('accounts') else ''
    pv=f'''<h2 id="who">Who we are</h2><p>{name} is developed and published by {who}{where}. This privacy policy applies to the {name} game. Our studio-wide policy for the website is on the <a href="/privacy-policy/">{E(DEV)} privacy policy</a> page.</p><p>Privacy contact: <a href="mailto:{mail}">{mail}</a></p>
<h2 id="collect">Data we collect and how</h2><p>The game collects the following data automatically while you play, or when you contact us:</p><ul>{''.join(collects)}<li><strong>Support messages:</strong> your email address and message, if you write to us, used only to reply.</li></ul>
<h2 id="sharing">Who we share data with</h2>{tp_html}{ads_html}
<h2 id="security">How we protect data</h2><p>Data sent over the internet by the game uses encrypted connections (HTTPS). Access to any data we hold is limited to the people who need it to run and support the game.</p>
<h2 id="retention">Data retention and deletion</h2><p>We keep diagnostic and gameplay data for up to 24 months, then delete or anonymise it. Support emails are kept for up to 24 months. Purchase records are kept for as long as tax and accounting law requires. Security logs may be kept for up to 12 months to prevent fraud.</p><p>You can request deletion of your data at any time on the <a href="{base}/delete-data/">delete my data page</a>. We complete requests within 30 days.</p>{acct}
<h2 id="rights">Your rights and choices</h2><p>Depending on where you live, you may have the right to access, correct, export or delete your data, and to withdraw consent. You can revoke consent or stop all further collection at any time by uninstalling the game. To use any of these rights, email <a href="mailto:{mail}">{mail}</a>. You can also complain to your local data protection authority.</p>
<h2 id="children">Children</h2>{kids}
<h2 id="changes">Changes to this policy</h2><p>We will post any change on this page and update the date above. For significant changes, we will also tell you in the game.</p>
<h2 id="contact">Contact</h2><p>{who}{where}<br>Email: <a href="mailto:{mail}">{mail}</a></p>'''
    legal_shell(g,'privacy',f'{nm} Privacy Policy',f'How {name} collects, uses, shares and deletes your data.',pv,f'Privacy policy for {nm} by {DEV}: data collected, third parties, retention, deletion and contact details.')
    # ---- terms ----
    buy=f'<h2 id="purchases">In-app purchases</h2><p>{name} offers optional purchases handled by the app store you use, under that store\'s terms. Virtual items have no real-world value and cannot be exchanged for money. Refunds follow the store\'s policy, except where consumer law gives you more rights.</p>' if g.get('iap') else ''
    ads=f'<h2 id="ads">Advertising</h2><p>{name} shows third-party ads. We are not responsible for the content of those ads or for what they advertise.</p>' if g.get('ads') else ''
    tm=f'''<h2 id="accept">Accepting these terms</h2><p>By installing or playing {name} you agree to these terms, to the <a href="{base}/privacy/">{name} privacy policy</a> and to the <a href="/terms/">{E(DEV)} terms and conditions</a>. If you do not agree, please do not play the game.</p>
<h2 id="licence">Your licence</h2><p>{who} gives you a personal, non-transferable licence to install and play {name} on your own devices for your own entertainment. The game is licensed, not sold.</p>
<h2 id="rules">Rules</h2><ul><li>Do not cheat, hack, or use bots or unauthorised software with the game.</li><li>Do not copy, resell or reverse engineer the game, except where the law allows it.</li><li>Do not harass other players or post illegal content.</li></ul>{buy}{ads}
<h2 id="updates">Updates and availability</h2><p>We may update, change or stop offering the game or any of its features at any time.</p>
<h2 id="liability">Disclaimer</h2><p>The game is provided as it is, without warranties, to the fullest extent the law allows. Nothing in these terms limits rights you have under the consumer law of your country.</p>
<h2 id="contact">Contact</h2><p>Questions about these terms: <a href="mailto:{mail}">{mail}</a></p>'''
    legal_shell(g,'terms',f'{nm} Terms of Use',f'The rules for playing {name}.',tm,f'Terms of use for {nm} by {DEV}: licence, rules, purchases and contact details.')
    # ---- support ----
    restore=f'<h2 id="restore">Restoring purchases</h2><p>Sign in with the same store account you used to buy, reinstall the game, then open the shop. If your purchase does not return, email us with your store receipt.</p>' if g.get('iap') else ''
    sp=f'''<h2 id="contact">Contact support</h2><p>Email us and we will reply within two business days.</p><p><a class="btn btn-primary" href="{mailto('Support: '+nm)}">Email {mail}</a></p>
<h2 id="include">What to include</h2><ul><li>Your device model and operating system version</li><li>The game version{(', currently '+E(g['version'])) if g.get('version') else ''}</li><li>What happened, and a screenshot if you can</li></ul>{restore}
<h2 id="links">More information</h2><ul><li><a href="{base}/privacy/">Privacy policy</a></li><li><a href="{base}/terms/">Terms of use</a></li><li><a href="{base}/delete-data/">Delete my data</a></li></ul>'''
    legal_shell(g,'support',f'{nm} Support',f'Get help with {name} from {E(DEV)}.',sp,f'Support for {nm} by {DEV}: how to contact us and what to include.')
    # ---- delete data ----
    sub=f'<p><strong>If you have a subscription,</strong> cancel it first in your Google Play or App Store account. Deleting game data does not cancel store billing.</p>' if g.get('iap') else ''
    thing='account and data' if g.get('accounts') else 'data'
    dl=f'''<div class="callout"><p><strong>To delete your {name} {thing},</strong> send us the request below. You do not need the game installed.</p></div><p><a class="btn btn-primary" href="{mailto('Data deletion request: '+nm)}">Request deletion by email</a></p>
<h2 id="steps">How it works</h2><ol class="steps-list"><li>Email <a href="mailto:{mail}">{mail}</a> with the subject "Data deletion request: {name}".</li><li>Include your player name or ID if the game shows one, so we can find your data.</li><li>We confirm your request, and we complete the deletion within 30 days.</li></ol>{sub}
<h2 id="deleted">What is deleted</h2><ul><li>Your game progress, scores and settings held on our systems</li><li>Your player name and account identifier, if you have one</li><li>Support emails linked to your request, once it is closed</li></ul>
<h2 id="kept">What we keep, and for how long</h2><ul><li>Purchase records, for as long as tax and accounting law requires</li><li>Security and fraud-prevention logs, for up to 12 months</li><li>Data held by third-party services and app stores, which is handled under their own policies</li></ul><p>Progress saved only on your device is removed when you uninstall the game. This page is provided by {who}, the developer of {name} on Google Play and the App Store.</p>'''
    legal_shell(g,'delete',f'Delete your {nm} data',f'Request deletion of your {name} {thing} from {E(DEV)}, without reinstalling the game.',dl,f'How to request deletion of your {nm} account and data, what is deleted, and what is kept.')
import datetime
TODAY=datetime.date.today().isoformat()
for _d in os.listdir('games'):
    if os.path.isdir(f'games/{_d}') and _d not in {g['id'] for g in GAMES}: shutil.rmtree(f'games/{_d}')

# ====================== HOME ======================
T_HOME='3D &amp; Mobile Game Development Studio | StoneBuild Games'
DESC_HOME='Game development studio building 3D, 2D and multiplayer games for Android, iOS and PC in Unity, Unreal and Godot. From prototype to store launch.'
ld_home={"@context":"https://schema.org","@graph":[ORG,WEBSITE,
 {"@type":"ImageObject","@id":f"{D}/#primaryimage","url":f"{D}/assets/og-image.png","contentUrl":f"{D}/assets/og-image.png","width":1200,"height":630,"caption":"StoneBuild Games mined-block logo with the words Building worlds worth playing."},
 webpage('/','3D & Mobile Game Development Studio | StoneBuild Games',DESC_HOME,extra={"about":{"@id":f"{D}/#organization"},"primaryImageOfPage":{"@id":f"{D}/#primaryimage"},"image":{"@id":f"{D}/#primaryimage"}})]}
home_body=f'''
  {dots([('top','Intro'),('services','Services'),('play','Play')]+([('games','Games')] if HOME_GAMES else [])+[('why','Why us'),('contact','Contact')])}

  <main id="main">
    <!-- HERO -->
    <section class="screen hero" aria-labelledby="hero-title">
      <div class="hero-canvas" id="hero-canvas" aria-hidden="true"></div>
      <div class="container hero-grid">
        <div class="hero-copy">
          <div class="badge-row reveal">
            <span class="pill"><i class="dot" aria-hidden="true"></i> Accepting new projects</span>
          </div>
          <h1 id="hero-title" class="hero-text"><span class="h1-kicker">3D &amp; mobile game development studio</span><span class="line">Building worlds</span> <span class="line line-accent">worth playing.</span></h1>
          <p class="lead hero-text">We design and build 3D, 2D and multiplayer games for Android, iOS and PC, from the first playable prototype to launch day on the store, and the updates after.</p>
          <div class="hero-cta reveal">
            <a class="btn btn-primary btn-lg" href="/contact/">Start a project {I['arrow']}</a>
            <a class="btn btn-ghost btn-lg" href="/services/">Explore services</a>
          </div>
          <div class="hero-stores reveal">{HERO_STORES}</div>
          <dl class="hero-stats reveal">
            <div class="stat"><dt class="sr-only">Prototype</dt><dd><b>1 week</b> <span>To a playable prototype</span></dd></div>
            <div class="stat"><dt class="sr-only">Engines</dt><dd><b>3 engines</b> <span>Unity · Unreal · Godot</span></dd></div>
            <div class="stat"><dt class="sr-only">Platforms</dt><dd><b>3 platforms</b> <span>Android · iOS · PC</span></dd></div>
          </dl>
        </div>
        <div class="hero-visual reveal" aria-hidden="true">
          <div class="hv-disc d1"></div><div class="hv-disc d2"></div><div class="hv-disc d3"></div>
          <div class="hv-orbit o1"><i>{CUBE}</i></div>
          <div class="hv-orbit o2"><i>{CUBE}</i></div>
          <span class="hv-node n1"><svg viewBox="0 0 24 24"><path d="M9 3h6v6h6v6h-6v6H9v-6H3V9h6z"/></svg></span>
          <span class="hv-node n2"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/></svg></span>
          <span class="hv-node n3"><svg viewBox="0 0 24 24"><path d="M12 4l9 16H3z"/></svg></span>
          <div class="hv-stage">
            <svg class="hv-mark" viewBox="10 10 180 180">
              <g stroke="#fff" stroke-width="2.6" stroke-linejoin="round">
                <g class="hv-block"><polygon style="--fx:-46px;--fy:26px;--dl:0.00s" points="30.72,60 65.36,80 65.36,120 100,140 100,180 30.72,140" fill="#0A0A0B"/><polygon style="--fx:46px;--fy:26px;--dl:0.12s" points="169.28,60 169.28,140 100,180 100,140 134.64,120 134.64,80" fill="#52525B"/><polygon style="--fx:-30px;--fy:-40px;--dl:0.30s" points="100,60 100,100 65.36,120 65.36,80" fill="#27272A"/><polygon style="--fx:30px;--fy:-40px;--dl:0.42s" points="100,60 134.64,80 134.64,120 100,100" fill="#3F3F46"/><polygon style="--fx:0px;--fy:-60px;--dl:0.56s" class="hv-floor" points="100,100 134.64,120 100,140 65.36,120" fill="#9E411A"/><polygon style="--fx:0px;--fy:-70px;--dl:0.74s" points="100,20 169.28,60 134.64,80 100,60 65.36,80 30.72,60" fill="#FF6A2B"/></g>
                <g class="hv-piece-in"><g class="hv-piece">
                  <polygon points="172,14 185.86,22 172,30 158.14,22" fill="#FF6A2B"/>
                  <polygon points="172,30 185.86,22 185.86,38 172,46" fill="#52525B"/>
                  <polygon points="158.14,22 172,30 172,46 158.14,38" fill="#0A0A0B"/>
                </g></g>
              </g>
            </svg>
            <div class="hv-shadow"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- SERVICES -->
    <section class="screen" id="services" aria-labelledby="services-title">
      <div class="container">
        <div class="section-head split">
          <span class="eyebrow reveal">What we do</span>
          <h2 id="services-title" class="reveal">Game development services, end to end</h2>
          <p class="lead reveal">We are a full-cycle game development company building mobile games for Android and iOS and 3D games for PC in Unity, Unreal Engine or Godot. Bring an idea, a prototype or a live game; we take it to a store-ready release.</p>
          <a class="link-arrow head-link reveal" href="/services/">See every service in detail {I['arrow']}</a>
        </div>
        <div class="svc-grid">
{HOME_SERVICES}        </div>
      </div>
    </section>

    <!-- PLAY -->
    <section class="screen" id="play" aria-labelledby="play-title">
      <div class="container">
        <div class="play-layout">
          <div class="play-copy">
            <span class="eyebrow reveal">Play it here</span>
            <h2 id="play-title" class="reveal">How high can you build?</h2>
            <p class="lead reveal">Stone Stack is a small game we made the way we prototype everything: fast, tight and playable on any device. Yours to beat, right in the browser.</p>
            <ol class="reveal">
              <li><b>1</b> <span>Tap, click or press <kbd>Space</kbd> to drop the moving block.</span></li>
              <li><b>2</b> <span>Whatever hangs over the edge gets cut off, so line it up.</span></li>
              <li><b>3</b> <span>A perfect drop scores double. Three in a row grows your block back.</span></li>
            </ol>
          </div>
          <div class="game reveal" id="stack-game" tabindex="0" role="application" aria-label="Stone Stack game. Press Space or tap to drop the block.">
            <canvas aria-hidden="true"></canvas>
            <div class="game-top">
              <span class="game-best">Best <b data-best>0</b></span>
              <button class="game-sound" type="button" aria-pressed="false" aria-label="Turn sound off">
                <svg class="on" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4zM16 9a4 4 0 0 1 0 6M19 6a8 8 0 0 1 0 12"/></svg>
                <svg class="off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4zM16 9l5 6M21 9l-5 6"/></svg>
              </button>
            </div>
            <div class="game-score" aria-hidden="true">0</div>
            <div class="game-panel game-start">
              <div class="game-logo">Stone <span>Stack</span></div>
              <p>Drop each block on the one below.</p>
            </div>
            <div class="game-cta"><button class="btn btn-primary btn-lg" type="button">Play now {I['arrow']}</button></div>
            <div class="game-panel game-over" role="status">
              <div class="new-best">New best</div>
              <div class="label">Your score</div>
              <div class="final" data-final>0</div>
              <div class="sub" data-sub></div>
              <button class="btn btn-primary" type="button">Play again {I['arrow']}</button>
            </div>
          </div>
        </div>
      </div>
    </section>

{HOME_GAMES}    <!-- WHY -->
    <section class="screen" id="why" aria-labelledby="why-title">
      <div class="container">
        <div class="why-layout">
          <div class="why-copy">
            <span class="eyebrow reveal">Why StoneBuild</span>
            <h2 id="why-title" class="reveal">Solid foundations, built to last</h2>
            <p class="lead reveal">Games fail on details: frame drops, broken saves, a rejected store review. We test on real mid-range devices, ship a build every sprint and handle store compliance during production, not the week of launch.</p>
            {MARQUEE}
            <a class="link-arrow reveal" href="/about/">More about the studio {I['arrow']}</a>
          </div>
          {why_list()}
        </div>
      </div>
    </section>

    <!-- CONTACT -->
    <section class="screen" id="contact" aria-labelledby="cta-title">
      <div class="container">
        <div class="card cta-band reveal">
          <div><h2 id="cta-title">Let's build your game</h2><p>Share the genre, platforms and timeline you have in mind. We reply within two business days with questions, a rough scope and a plan.</p></div>
          <div class="actions"><a class="btn btn-primary btn-lg" href="/contact/">Start a project {I['arrow']}</a><a class="btn btn-ghost btn-lg" href="mailto:support@stonebuildgames.com">Email us</a></div>
        </div>
      </div>
{FOOTER}    </section>
  </main>

  <script src="/js/game.js" defer></script>
'''
home=head(T_HOME,DESC_HOME,'/',ld_home)+header('/')+home_body+SCRIPTS+'''  <script type="importmap">{ "imports": { "three": "/vendor/three.module.min.js" } }</script>
  <script type="module" src="/js/hero3d.js"></script>
</body>
</html>
'''
write('index.html', home)

# ====================== SERVICES ======================
T='Game Development Services | StoneBuild Games'
DESC='Full-cycle game development services: 3D and mobile games, multiplayer and backend, game art, porting, QA and publishing on Google Play, App Store and Steam.'
ld={"@context":"https://schema.org","@graph":[webpage('/services/','Game Development Services | StoneBuild Games',DESC),crumbs('/services/','Services'),
 {"@type":"Service","@id":f"{D}/services/#service","url":f"{D}/services/","name":"Game Development Services","description":"Full-cycle game development for Android, iOS and PC: from concept and prototype to a polished, store-ready release.","provider":{"@id":f"{D}/#organization"},"serviceType":"Game development","areaServed":"Worldwide",
  "hasOfferCatalog":{"@type":"OfferCatalog","name":"Game development services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s[1].replace('&amp;','&'),"description":s[2]}} for s in SERVICES]}}]}
body=page_hero('Services','Services','Game development services, end to end','We are a full-cycle game development company building mobile games for Android and iOS and 3D games for PC in Unity, Unreal Engine or Godot. Bring an idea, a prototype or a live game; we take it to a polished, store-ready release.')
body+=f'''    <section class="page-section" aria-labelledby="list-title">
      <div class="container">
        <h2 id="list-title" class="sr-only">Our six services</h2>
        <div class="services-grid">
{"".join(service_card(i,s,full=True) for i,s in enumerate(SERVICES))}        </div>
      </div>
    </section>
    <section class="page-section alt" aria-labelledby="models-title">
      <div class="container">
        <div class="section-head split">
          <span class="eyebrow reveal">Engagement models</span>
          <h2 id="models-title" class="reveal">Three ways to work with us</h2>
          <p class="lead reveal">Every project starts with a short discovery call and a written scope. Pricing follows the scope, not the other way round.</p>
        </div>
        <div class="models">
          <article class="card model tilt reveal"><h3>Fixed-scope project</h3><p class="price">Quote after discovery</p><p class="muted small">Best for a clearly defined game or feature with a launch date.</p><ul><li>{I['check']} <span>Milestones with playable builds</span></li><li>{I['check']} <span>Fixed price per milestone</span></li><li>{I['check']} <span>Change requests handled transparently</span></li></ul></article>
          <article class="card model tilt reveal"><h3>Dedicated team</h3><p class="price">Monthly</p><p class="muted small">Best for live games and studios that need ongoing capacity.</p><ul><li>{I['check']} <span>Developers, artists and QA on your roadmap</span></li><li>{I['check']} <span>Two-week sprints, weekly syncs</span></li><li>{I['check']} <span>Scale the team up or down each month</span></li></ul></article>
          <article class="card model tilt reveal"><h3>Co-development &amp; rescue</h3><p class="price">Quote after a code review</p><p class="muted small">Best for a stuck project, a port or a performance problem.</p><ul><li>{I['check']} <span>Codebase and performance audit first</span></li><li>{I['check']} <span>Clear plan with risks and timeline</span></li><li>{I['check']} <span>We work inside your repo and pipeline</span></li></ul></article>
        </div>
      </div>
    </section>
    <section class="page-section" aria-labelledby="process-title" id="process">
      <div class="container">
        <div class="section-head center">
          <span class="eyebrow reveal">How we work</span>
          <h2 id="process-title" class="reveal">How we build a game, from idea to launch</h2>
          <p class="lead reveal">Every StoneBuild Games project follows five stages: discovery, a playable prototype in about one week, production in two-week sprints, polish and QA, then launch and LiveOps. You get a playable build and a written changelog at the end of every sprint.</p>
        </div>
        {process_html()}
      </div>
    </section>
{faq_section(FAQ)}    <section class="page-section page-body" aria-label="Call to action"><div class="container">{CTA}</div></section>
  </main>
'''
write('services/index.html', head(T,DESC,'/services/',ld)+header('/services/')+'\n  <main id="main">\n'+body+FOOTER+SCRIPTS+'</body>\n</html>\n')

# ====================== ABOUT ======================
T='About StoneBuild Games | Independent Game Development Studio'
DESC='StoneBuild Games is an independent, remote game studio that builds its own titles and develops games for clients. How we work, what we value, the tools we use.'
ld={"@context":"https://schema.org","@graph":[webpage('/about/',T,DESC,'AboutPage',{"about":{"@id":f"{D}/#organization"}}),crumbs('/about/','About')]}
body=page_hero('About','About the studio','A studio built on solid foundations',STUDIO_SENTENCE+' We build our own titles and develop games for clients, with the same team, the same pipeline and the same standards.')
body+=f'''    <section class="page-section" aria-labelledby="story-title">
      <div class="container why-layout">
        <div class="prose">
          <h2 id="story-title" class="reveal">Why we exist</h2>
          <p class="reveal">Most games do not fail on the big idea. They fail on details: a frame drop on a mid-range phone, a save that does not restore, a store review that gets rejected the week of launch. StoneBuild exists to get those details right, so the idea gets a fair chance.</p>
          <p class="reveal">The name says what we do. Stone, because we build things meant to last: clean code, documented systems and assets you can keep working with for years. Build, because we ship. Every sprint ends with a playable build, and every project ends on a storefront.</p>
          <p class="reveal">We work with Unity, Unreal Engine and Godot, in 2D and 3D, for Android, iOS, PC and the web. We are deliberately small, so the people who scope your game are the people who build it. The 3D scene on our home page and the Stone Stack mini-game are our own real-time work.</p>
        </div>
        {why_list('why-list')}
      </div>
    </section>
    <section class="page-section alt" aria-labelledby="process-title" id="process">
      <div class="container">
        <div class="section-head center">
          <span class="eyebrow reveal">How we work</span>
          <h2 id="process-title" class="reveal">From idea to launch, in the open</h2>
          <p class="lead reveal">Discovery, prototype, production, polish, launch. You see a playable build every sprint and know exactly what ships next.</p>
        </div>
        {process_html()}
      </div>
    </section>
    <section class="page-section" aria-labelledby="tech-title">
      <div class="container">
        <div class="section-head center">
          <span class="eyebrow reveal">Toolbox</span>
          <h2 id="tech-title" class="reveal">Engines and services we build with</h2>
        </div>
        {MARQUEE}
      </div>
    </section>
    <section class="page-section page-body" aria-label="Call to action"><div class="container">{CTA}</div></section>
  </main>
'''
write('about/index.html', head(T,DESC,'/about/',ld)+header('/about/')+'\n  <main id="main">\n'+body+FOOTER+SCRIPTS+'</body>\n</html>\n')

# ====================== CONTACT ======================
T='Contact StoneBuild Games | Start a Game Project'
DESC='Tell us about the game you want to build. StoneBuild Games replies within two business days with questions, a rough scope and next steps.'
ld={"@context":"https://schema.org","@graph":[webpage('/contact/',T,DESC,'ContactPage'),crumbs('/contact/','Contact')]}
_chips=lambda name,opts: ''.join(f'<label class="chip"><input type="radio" name="{name}" value="{o}"{" checked" if n==0 else ""}><span>{o}</span></label>' for n,o in enumerate(opts))
body=f'''    <section class="page-hero contact-hero" aria-labelledby="page-title">
      <div class="container">
        <nav aria-label="Breadcrumb" class="reveal"><ol class="breadcrumbs"><li><a href="/">Home</a></li><li aria-current="page">Contact</li></ol></nav>
        <h1 id="page-title" class="reveal">Let's build your game</h1>
        <p class="lead reveal">Tell us what you have in mind. We reply within two business days with questions, a rough scope and next steps.</p>
      </div>
    </section>
    <section class="page-section contact-section" aria-label="Contact form">
      <div class="container">
        <div class="contact-panel reveal">
          <aside class="contact-side">
            <p class="eyebrow">What happens next</p>
            <ol class="contact-steps">
              <li><b>1</b><div><h2>We read your message</h2><p>A real person reads it, usually the same day.</p></div></li>
              <li><b>2</b><div><h2>We reply in 2 business days</h2><p>You get our questions and a rough scope.</p></div></li>
              <li><b>3</b><div><h2>A short call</h2><p>We agree on the plan. A prototype takes about a week.</p></div></li>
            </ol>
            <div class="contact-mail"><span>Prefer email?</span><a href="mailto:support@stonebuildgames.com">support@stonebuildgames.com</a></div>
          </aside>
          <form class="contact-form" id="contact-form" novalidate>
            <div class="form-row">
              <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
              <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
            </div>
            <fieldset class="chips"><legend>What do you need?</legend>{_chips('type',['3D game','Mobile or casual game','Multiplayer game','Art and animation','Porting or publishing','Something else'])}</fieldset>
            <fieldset class="chips"><legend>Budget range</legend>{_chips('budget',['Not sure yet','Under $5k','$5k to $15k','$15k to $50k','$50k+'])}</fieldset>
            <div class="field"><label for="f-msg">Tell us about the game</label><textarea id="f-msg" name="message" required placeholder="Genre, platforms, reference games, timeline..."></textarea></div>
            <div class="form-end"><button class="btn btn-primary btn-lg" type="submit">Send via email {I['arrow']}</button><p class="form-note" id="form-note" role="status">Opens your email app with your message ready to send.</p></div>
          </form>
        </div>
      </div>
    </section>
    <section class="page-section page-body" aria-labelledby="other-title">
      <div class="container">
        <h2 id="other-title" class="reveal g-h2">Looking for something else?</h2>
        <div class="g-legal-grid three reveal">
          <a class="g-legal" href="mailto:support@stonebuildgames.com?subject=Game%20support">{I['help']}<span>Help with one of our games</span>{I['arrow']}</a>
          <a class="g-legal" href="/privacy-policy/#data-deletion">{I['trash']}<span>Delete my data</span>{I['arrow']}</a>
          <a class="g-legal" href="/services/">{I['layers']}<span>See all our services</span>{I['arrow']}</a>
        </div>
      </div>
    </section>
  </main>
'''
write('contact/index.html', head(T,DESC,'/contact/',ld)+header('/contact/')+'\n  <main id="main">\n'+body+FOOTER+SCRIPTS+'</body>\n</html>\n')

# ====================== GAMES ======================
for g in GAMES: write_game(g)
T='Our Games | StoneBuild Games' if GAMES else 'Our Games: First Title in Production | StoneBuild Games'
DESC=('Games developed and published by StoneBuild Games. Explore each game, its store links, privacy policy and support.' if GAMES else 'Our first game is in production for Android. Screenshots, a trailer and the Google Play link will be posted here the day it launches.')
ld={"@context":"https://schema.org","@graph":[webpage('/games/',T,DESC,'CollectionPage'),crumbs('/games/','Games')]}
_lead='Every title we publish lives here. Hover a game to open its store page or explore it.' if GAMES else 'Our first original title is in production for Android. Its Google Play link, screenshots and trailer will be posted here the day it launches.'
body=page_hero('Games','Our games','Games by StoneBuild',_lead)
if GAMES:
    _grid=game_grid(GAMES)
else:
    _grid=f'''<div class="games-grid"><article class="card game-card"><div class="game-cover"><div class="art" aria-hidden="true"></div><div class="label"><div><span class="status">In production</span><h3>Our first title</h3><p>Coming to Google Play</p></div></div></div></article></div>'''
body+=f'''    <section class="page-body" aria-labelledby="grid-title">
      <div class="container">
        <h2 id="grid-title" class="sr-only">All titles</h2>
        {_grid}
        <div class="callout reveal" style="max-width:760px;margin-top:40px">
          <p><strong>Want a game built for your brand or idea?</strong> We build games for clients with the same team and pipeline. <a class="link-arrow" href="/contact/" style="display:inline-flex;margin-left:6px">Start a project {I['arrow']}</a></p>
        </div>
      </div>
    </section>
  </main>
'''
write('games/index.html', head(T,DESC,'/games/',ld)+header('/games/')+'\n  <main id="main">\n'+body+FOOTER+SCRIPTS+'</body>\n</html>\n')

# ====================== PRIVACY / TERMS / 404 (reuse main content) ======================
def main_of(f):
    s=open(f).read(); m=re.search(r'(<main id="main">.*?</main>)', s, re.S); return m.group(1)
pp=main_of('privacy-policy/index.html')
pp=pp.replace('<ol class="breadcrumbs reveal" aria-label="Breadcrumb"><li><a href="/">Home</a></li><li aria-current="page">Privacy Policy</li></ol>','<nav aria-label="Breadcrumb" class="reveal"><ol class="breadcrumbs"><li><a href="/">Home</a></li><li aria-current="page">Privacy Policy</li></ol></nav>')
pp=pp.replace('<h4>On this page</h4>','<p class="toc-title">On this page</p>')
pp=pp.replace("The Site is a static website. Our hosting provider may keep standard server logs (IP address, browser type, pages requested, time of request) for security and reliability. The Site does not set advertising cookies. If we add analytics in the future, this policy and the Site's cookie notice will be updated first.",
 "The Site is a static website. Fonts, scripts and images are served from our own domain, and the Site sets no cookies and uses no analytics or advertising trackers. Our hosting provider may keep standard server logs (IP address, browser type, pages requested, time of request) for security and reliability. The Stone Stack mini-game stores your best score only in your own browser (local storage); it is never sent to us. If we add analytics in the future, this policy will be updated first.")
pp=pp.replace("We develop and publish mobile, PC and web games (the \"Games\")","We develop and publish games for Android, iOS and PC (the \"Games\")")
T='Privacy Policy | StoneBuild Games'; DESC="How we collect, use and protect data in our games and on this website: third-party SDKs, ads, children's privacy, your rights and data deletion."
ld={"@context":"https://schema.org","@graph":[webpage('/privacy-policy/',T,DESC,extra={"dateModified":"2026-11-04"}),crumbs('/privacy-policy/','Privacy Policy')]}
write('privacy-policy/index.html', head(T,DESC,'/privacy-policy/',ld)+header('/privacy-policy/')+'\n  '+pp+'\n'+FOOTER+SCRIPTS+'</body>\n</html>\n')
tc=main_of('terms/index.html')
tc=tc.replace('<ol class="breadcrumbs reveal" aria-label="Breadcrumb"><li><a href="/">Home</a></li><li aria-current="page">Terms &amp; Conditions</li></ol>','<nav aria-label="Breadcrumb" class="reveal"><ol class="breadcrumbs"><li><a href="/">Home</a></li><li aria-current="page">Terms &amp; Conditions</li></ol></nav>')
tc=tc.replace('<h4>On this page</h4>','<p class="toc-title">On this page</p>')
T='Terms &amp; Conditions | StoneBuild Games'; DESC='Terms for playing our games and using this website: licence, in-app purchases, player conduct, intellectual property and limitation of liability.'
ld={"@context":"https://schema.org","@graph":[webpage('/terms/','Terms & Conditions | StoneBuild Games',DESC,extra={"dateModified":"2026-11-04"}),crumbs('/terms/','Terms & Conditions')]}
write('terms/index.html', head(T,DESC,'/terms/',ld)+header('/terms/')+'\n  '+tc+'\n'+FOOTER+SCRIPTS+'</body>\n</html>\n')
nf=main_of('404.html').replace('code gradient-text','code')
write('404.html', head('Page not found | StoneBuild Games','The page you were looking for does not exist on stonebuildgames.com.','/404.html',None,robots='noindex',canonical=False)+header('/404.html')+'\n  '+nf+'\n'+FOOTER+SCRIPTS+'</body>\n</html>\n')

# ====================== SERVICE PAGES ======================
for n,sp in enumerate(SERVICE_PAGES):
    path=f"/services/{sp['slug']}/"
    cr=[('Home','/'),('Services','/services/'),(sp['title'],path)]
    ld={"@context":"https://schema.org","@graph":[webpage(path,sp['meta'],sp['desc']),crumbs3([(a.replace('&amp;','&'),b) for a,b in cr]),
      {"@type":"Service","@id":f"{D}{path}#service","name":sp['h1'],"description":sp['desc'],"serviceType":sp['title'],"provider":{"@id":f"{D}/#organization"},"areaServed":"Worldwide","url":f"{D}{path}"}]}
    incl=''.join(f'<div class="svc static reveal"><div class="svc-top"><span class="num">0{i+1}</span></div><h3>{t}</h3><p>{d}</p></div>' for i,(t,d) in enumerate(sp['includes']))
    steps=''.join(f'<li class="step reveal"><span class="node">{i+1}</span><h3>{t}</h3><p>{d}</p></li>' for i,(t,d) in enumerate(sp['steps']))
    tools=''.join(f'<span class="tool">{t}</span>' for t in sp['tools'])
    fit=''.join(f'<li>{I["check"]}<span>{f}</span></li>' for f in sp['fit'])
    others=[o for o in SERVICE_PAGES if o['slug']!=sp['slug']]
    rel=[others[(n+k)%len(others)] for k in range(3)]
    rel_html=''.join(f'<a class="g-legal" href="/services/{o["slug"]}/">{I[o["icon"]]}<span>{o["title"]}</span>{I["arrow"]}</a>' for o in rel)
    body=f'''    <section class="page-hero svc-hero" aria-labelledby="page-title">
      <div class="container svc-hero-grid">
        <div class="svc-hero-copy">
          {crumb_html(cr)}
          <span class="eyebrow reveal">Service 0{n+1}</span>
          <h1 id="page-title" class="reveal">{sp['h1']}</h1>
          <p class="lead reveal">{sp['lead']}</p>
          <div class="hero-cta reveal"><a class="btn btn-primary btn-lg" href="/contact/">Start a project {I['arrow']}</a><a class="btn btn-ghost btn-lg" href="/services/">All services</a></div>
        </div>
        <div class="svc-emblem reveal" aria-hidden="true"><div class="hv-disc d1"></div><div class="hv-disc d2"></div><div class="hv-disc d3"></div><div class="hv-orbit o1"><i>{CUBE}</i></div><div class="svc-tile">{I[sp['icon']]}</div></div>
      </div>
    </section>
    <section class="page-section alt" aria-labelledby="why-title">
      <div class="container svc-why"><h2 id="why-title" class="reveal">Why it matters</h2><p class="lead reveal">{sp['why']}</p></div>
    </section>
    <section class="page-section" aria-labelledby="inc-title">
      <div class="container">
        <div class="section-head"><span class="eyebrow reveal">What you get</span><h2 id="inc-title" class="reveal">What is included</h2></div>
        <div class="svc-grid">{incl}</div>
      </div>
    </section>
    <section class="page-section alt" aria-labelledby="how-title">
      <div class="container">
        <div class="section-head"><span class="eyebrow reveal">How it works</span><h2 id="how-title" class="reveal">Four clear steps</h2></div>
        <ol class="process four">{steps}</ol>
      </div>
    </section>
    <section class="page-section" aria-labelledby="fit-title">
      <div class="container svc-two">
        <div><span class="eyebrow reveal">A good fit if</span><h2 id="fit-title" class="reveal">Who this is for</h2><ul class="fit-list reveal">{fit}</ul></div>
        <div><span class="eyebrow reveal">Toolbox</span><h2 class="reveal">What we use</h2><div class="tool-list reveal">{tools}</div></div>
      </div>
    </section>
{faq_section(sp['faq'],title='Common questions',intro='What people usually ask us about '+(sp['title'] if sp['title'][0].isdigit() else sp['title'][0].lower()+sp['title'][1:])+'.')}    <section class="page-section" aria-labelledby="rel-title"><div class="container"><h2 id="rel-title" class="reveal g-h2">Related services</h2><div class="g-legal-grid three reveal">{rel_html}</div></div></section>
    <section class="page-section page-body" aria-label="Call to action"><div class="container">{CTA}</div></section>
'''
    page(path,f"services/{sp['slug']}/index.html",sp['meta'],sp['desc'],ld,body,current='/services/')

# sitemap
today='2026-11-04'
urls=[(f"/services/{p['slug']}/",'0.8','monthly') for p in SERVICE_PAGES]+[(f'/games/{g["id"]}/','0.9','monthly') for g in GAMES]+[(f'/games/{g["id"]}/{k}/','0.3','yearly') for g in GAMES for k in ('privacy','terms','support','delete-data')]+[('/','1.0','monthly'),('/services/','0.9','monthly'),('/about/','0.7','monthly'),('/games/','0.9','weekly'),('/contact/','0.8','monthly'),('/privacy-policy/','0.4','yearly'),('/terms/','0.4','yearly')]
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{D}{u}</loc><lastmod>{today}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n' for u,p,c in urls)+'</urlset>\n')
print('pages written')
