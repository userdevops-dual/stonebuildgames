import re, json, os, sys
# Generates every HTML page in site/ plus sitemap.xml. Run from anywhere: python3 tools/build_pages.py
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site'))
MARK='<svg class="brand-mark" viewBox="18 7 180 180" aria-hidden="true"><g stroke="#fff" stroke-width="3" stroke-linejoin="round"><polygon points="100,20 169.28,60 134.64,80 100,60 65.36,80 30.72,60" fill="#FF6A2B"/><polygon points="169.28,60 169.28,140 100,180 100,140 134.64,120 134.64,80" fill="#52525B"/><polygon points="30.72,60 65.36,80 65.36,120 100,140 100,180 30.72,140" fill="#0A0A0B"/><polygon points="100,100 134.64,120 100,140 65.36,120" fill="#9E411A"/><polygon points="100,60 100,100 65.36,120 65.36,80" fill="#27272A"/><polygon points="100,60 134.64,80 134.64,120 100,100" fill="#3F3F46"/><polygon points="172,14 185.86,22 172,30 158.14,22" fill="#FF6A2B"/><polygon points="172,30 185.86,22 185.86,38 172,46" fill="#52525B"/><polygon points="158.14,22 172,30 172,46 158.14,38" fill="#0A0A0B"/></g></svg>'
D='https://stonebuildgames.com'
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
  <meta property="og:image:alt" content="StoneBuild Games mined-block logo with the words Dig. Build. Play.">
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
          <!-- Replace the "#" links below with your real profile URLs -->
          <div class="socials" aria-label="Social links">
            <a href="/games/" aria-label="Our games on Google Play" title="Google Play">{I['playmono']}</a>
            <a href="#" rel="nofollow" aria-label="YouTube" title="YouTube">{I['yt']}</a>
            <a href="#" rel="nofollow" aria-label="Instagram" title="Instagram">{I['ig']}</a>
            <a href="#" rel="nofollow" aria-label="X (Twitter)" title="X">{I['x']}</a>
            <a href="#" rel="nofollow" aria-label="LinkedIn" title="LinkedIn">{I['in']}</a>
            <a href="mailto:support@stonebuildgames.com" aria-label="Email us" title="Email">{I['mail']}</a>
          </div>
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
          </article>
'''
PROCESS=[('Discovery','We define the core loop, target players, platforms and scope, then agree on a plan and a budget.','About 1 week'),('Prototype','A playable vertical slice that proves the fun before we commit to full production.','2 to 3 weeks'),('Production','Two-week sprints. Art, code and design land together, with a new build in your hands every sprint.','Sprint based'),('Polish &amp; QA','Device testing, performance passes, balancing and store policy checks until the game is release-ready.','Final sprints'),('Launch &amp; LiveOps','Store listings, soft launch, analytics and the updates that keep players coming back.','Ongoing')]
SHORT=[('gamepad','Full-cycle development','Concept, prototype, production and release, with one team from first build to storefront.'),('cube','3D games','Stylized or realistic worlds, custom shaders and physics, tuned for mid-range phones.'),('phone','Mobile and casual games','Fast prototypes, tight game feel, and ads and in-app purchases wired in cleanly.'),('net','Multiplayer and backend','Real-time netcode, matchmaking, leaderboards and cloud saves that scale with your players.'),('pen','Game art and animation','Characters, environments, UI and VFX in one style, animated to feel alive in-engine.'),('upload','Porting, QA and publishing','Store-ready builds, device testing and policy compliance for Google Play, App Store and Steam.')]
HOME_SERVICES=''.join(f'''          <article class="svc reveal">
            <div class="svc-top"><div class="icon">{I[ic]}</div><span class="num">0{n+1}</span></div>
            <h3>{t}</h3>
            <p>{d}</p>
          </article>
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
 ('How long does it take to build a mobile game?','A playable prototype takes two to three weeks after a one-week discovery. A small casual game can ship in two to three months of two-week sprints; a 3D or multiplayer game usually takes longer. We give a dated plan after discovery.'),
 ('How much does it cost to develop a game?','It depends on scope. Our inquiry form uses four ranges: under $5k for a prototype or a small feature, $5k to $15k for a casual mobile game, $15k to $50k for a mid-size 3D or multiplayer title, and $50k+ for larger productions. Every quote follows a written scope.'),
 ('Who owns the source code and art?','You do. Source code, art files, design documents and store accounts stay in your name, and the contract says so. There is no lock-in.'),
 ('Which engines and platforms do you work with?','Unity, Unreal Engine and Godot, in 2D and 3D, for Android, iOS, PC (Steam) and the web. Backend work uses Firebase, Photon and Google Play Games Services.'),
 ('Where is StoneBuild Games based?','StoneBuild Games is a remote studio and works with clients worldwide over email and video calls. Reach us at support@stonebuildgames.com; we reply within two business days.'),
]
FAQ_HTML='<div class="faq">'+''.join(f'<div class="card q reveal"><h3>{q}</h3><p>{a}</p></div>' for q,a in FAQ)+'</div>'
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
def write(path_file, html):
    os.makedirs(os.path.dirname(path_file) or '.', exist_ok=True)
    open(path_file,'w').write(html)
def dots(items):
    out=[]
    for n,(i,l) in enumerate(items):
        cls=' class="is-active"' if n==0 else ''
        out.append(f'<a href="#{i}" data-label="{l}" aria-label="Go to {l} section"{cls}></a>')
    return '<nav class="dots" aria-label="Sections">'+''.join(out)+'</nav>'

# ====================== HOME ======================
T_HOME='3D &amp; Mobile Game Development Studio | StoneBuild Games'
DESC_HOME='Game development studio building 3D, 2D and multiplayer games for Android, iOS and PC in Unity, Unreal and Godot. From prototype to store launch.'
ld_home={"@context":"https://schema.org","@graph":[ORG,WEBSITE,
 {"@type":"ImageObject","@id":f"{D}/#primaryimage","url":f"{D}/assets/og-image.png","contentUrl":f"{D}/assets/og-image.png","width":1200,"height":630,"caption":"StoneBuild Games mined-block logo with the words Dig. Build. Play."},
 webpage('/','3D & Mobile Game Development Studio | StoneBuild Games',DESC_HOME,extra={"about":{"@id":f"{D}/#organization"},"primaryImageOfPage":{"@id":f"{D}/#primaryimage"},"image":{"@id":f"{D}/#primaryimage"}})]}
home_body=f'''
  {dots([('top','Intro'),('services','Services'),('play','Play'),('games','Games'),('why','Why us'),('contact','Contact')])}

  <main id="main">
    <!-- HERO -->
    <section class="screen hero" aria-labelledby="hero-title">
      <div class="hero-canvas" id="hero-canvas" aria-hidden="true"></div>
      <div class="hero-fade" aria-hidden="true"></div>
      <div class="container hero-grid">
        <div class="hero-copy">
          <div class="badge-row reveal">
            <span class="pill"><i class="dot" aria-hidden="true"></i> Accepting new projects</span>
          </div>
          <h1 id="hero-title" class="hero-text"><span class="h1-kicker">3D &amp; mobile game development studio</span><span class="line">Dig. Build.</span> <span class="line line-accent">Play.</span></h1>
          <p class="lead hero-text">We design and build 3D, 2D and multiplayer games for Android, iOS and PC, from the first playable prototype to launch day on the store, and the updates after.</p>
          <div class="hero-cta reveal">
            <a class="btn btn-primary btn-lg" href="/contact/">Start a project {I['arrow']}</a>
            <a class="btn btn-ghost btn-lg" href="/services/">Explore services</a>
          </div>
          <dl class="hero-stats reveal">
            <div class="stat"><dt class="sr-only">Scope</dt><dd><b>Full-cycle</b> <span>Idea to launch to LiveOps</span></dd></div>
            <div class="stat"><dt class="sr-only">Engines</dt><dd><b>3D &amp; 2D</b> <span>Unity · Unreal · Godot</span></dd></div>
            <div class="stat"><dt class="sr-only">Platforms</dt><dd><b>Mobile &amp; PC</b> <span>Android · iOS · Steam</span></dd></div>
          </dl>
        </div>
        <div class="hero-visual reveal" aria-hidden="true">
          <div class="hv-ring"></div>
          <div class="hv-stage">
            <svg class="hv-mark" viewBox="18 7 180 180">
              <g stroke="#fff" stroke-width="2.6" stroke-linejoin="round">
                <g class="hv-block">
                  <polygon points="100,20 169.28,60 134.64,80 100,60 65.36,80 30.72,60" fill="#FF6A2B"/>
                  <polygon points="169.28,60 169.28,140 100,180 100,140 134.64,120 134.64,80" fill="#52525B"/>
                  <polygon points="30.72,60 65.36,80 65.36,120 100,140 100,180 30.72,140" fill="#0A0A0B"/>
                  <polygon class="hv-floor" points="100,100 134.64,120 100,140 65.36,120" fill="#9E411A"/>
                  <polygon points="100,60 100,100 65.36,120 65.36,80" fill="#27272A"/>
                  <polygon points="100,60 134.64,80 134.64,120 100,100" fill="#3F3F46"/>
                </g>
                <g class="hv-piece">
                  <polygon points="172,14 185.86,22 172,30 158.14,22" fill="#FF6A2B"/>
                  <polygon points="172,30 185.86,22 185.86,38 172,46" fill="#52525B"/>
                  <polygon points="158.14,22 172,30 172,46 158.14,38" fill="#0A0A0B"/>
                </g>
              </g>
            </svg>
            <div class="hv-shadow"></div>
          </div>
          <div class="hv-chip c1"><i>{I['zap']}</i><span><b>Prototype</b> in 2 to 3 weeks</span></div>
          <div class="hv-chip c2"><i>{I['cube']}</i><span><b>Unity</b> · Unreal · Godot</span></div>
          <div class="hv-chip c3"><i>{I['phone']}</i><span><b>Android</b> · iOS · PC</span></div>
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

    <!-- GAMES -->
    <section class="screen" id="games" aria-labelledby="games-title">
      <div class="container">
        <div class="games-layout">
          <div class="games-copy">
            <span class="eyebrow reveal">Our games</span>
            <h2 id="games-title" class="reveal">Built in the same forge we offer to clients</h2>
            <p class="lead reveal">StoneBuild Games also develops its own games. Our first original title is in production for Android and will be published on Google Play under the StoneBuild Games developer name, built with the same pipeline we use for client work.</p>
            <ul class="reveal">
              <li>{I['check']} <span>Tested on real devices before every release</span></li>
              <li>{I['check']} <span>Public privacy policy and support email for every game</span></li>
              <li>{I['check']} <span>New titles appear on the games page the day they go live</span></li>
            </ul>
            <a class="link-arrow reveal" href="/games/">See all games {I['arrow']}</a>
          </div>
          <a class="card game-feature tilt reveal" href="/games/">
            <div class="game-cover">
              <div class="art" aria-hidden="true"></div>
              <div class="label"><div><span class="status">In production</span><h3>Our first title</h3><p>Coming to Google Play</p></div></div>
            </div>
          </a>
        </div>
      </div>
    </section>

    <!-- WHY -->
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
          <p class="lead reveal">Every StoneBuild Games project follows five stages: discovery (about one week), a playable prototype (two to three weeks), production in two-week sprints, polish and QA, then launch and LiveOps. You get a playable build and a written changelog at the end of every sprint.</p>
        </div>
        {process_html()}
      </div>
    </section>
    <section class="page-section alt" aria-labelledby="faq-title">
      <div class="container">
        <div class="section-head">
          <span class="eyebrow reveal">Questions</span>
          <h2 id="faq-title" class="reveal">Frequently asked questions</h2>
        </div>
        {FAQ_HTML}
      </div>
    </section>
    <section class="page-section page-body" aria-label="Call to action"><div class="container">{CTA}</div></section>
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
body=page_hero('Contact','Contact',"Let's build your game",'Tell us about the game you want to make. We reply within two business days with questions, a rough scope and next steps.')
body+=f'''    <section class="page-section page-body" aria-label="Contact details and form">
      <div class="container contact-layout">
        <div class="contact-copy">
          <div class="contact-lines">
            <div class="card contact-line reveal"><div class="icon">{I['mail']}</div><div><b>Email</b> <a href="mailto:support@stonebuildgames.com">support@stonebuildgames.com</a></div></div>
            <div class="card contact-line reveal"><div class="icon">{I['clock']}</div><div><b>Response time</b> <span>Within 2 business days</span></div></div>
            <div class="card contact-line reveal"><div class="icon">{I['globe']}</div><div><b>Where</b> <span>Remote studio, working with clients worldwide</span></div></div>
          </div>
          <div class="prose reveal">
            <h2 style="font-size:1.1rem;margin:1.6em 0 .5em">What helps us reply faster</h2>
            <ul>
              <li>Genre and a few reference games</li>
              <li>Platforms: Android, iOS, PC, web</li>
              <li>Where you are: idea, design doc, prototype or live game</li>
              <li>Timeline and budget range, even rough</li>
            </ul>
          </div>
        </div>
        <form class="card form reveal" id="contact-form" novalidate>
          <div class="form-row">
            <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
          </div>
          <div class="form-row">
            <div class="field"><label for="f-type">Project type</label><select id="f-type" name="type"><option>3D game</option><option>2D / casual game</option><option>Multiplayer game</option><option>Art &amp; animation</option><option>Porting / publishing</option><option>Something else</option></select></div>
            <div class="field"><label for="f-budget">Budget range</label><select id="f-budget" name="budget"><option>Not sure yet</option><option>Under $5k</option><option>$5k to $15k</option><option>$15k to $50k</option><option>$50k+</option></select></div>
          </div>
          <div class="field"><label for="f-msg">Tell us about the game</label><textarea id="f-msg" name="message" required placeholder="Genre, platforms, references, timeline..."></textarea></div>
          <button class="btn btn-primary btn-lg" type="submit">Send via email {I['arrow']}</button>
          <p class="form-note" id="form-note" role="status">Opens your email app with the message prefilled. Or write to us directly at support@stonebuildgames.com.</p>
        </form>
      </div>
    </section>
  </main>
'''
write('contact/index.html', head(T,DESC,'/contact/',ld)+header('/contact/')+'\n  <main id="main">\n'+body+FOOTER+SCRIPTS+'</body>\n</html>\n')

# ====================== GAMES ======================
T='Our Games: First Title in Production | StoneBuild Games'
DESC='Our first game is in production for Android. Screenshots, a trailer and the Google Play link will be posted here the day it launches.'
ld={"@context":"https://schema.org","@graph":[webpage('/games/',T,DESC,'CollectionPage'),crumbs('/games/','Games')]}
body=page_hero('Games','Our games','Games by StoneBuild','Every title we publish lives here with its platforms, status and store links. Our first original title is in production for Android; its Google Play link, screenshots and trailer will be posted here the day it launches.')
body+=f'''    <section class="page-body" aria-labelledby="grid-title">
      <div class="container">
        <h2 id="grid-title" class="sr-only">All titles</h2>
        <div class="games-grid" id="games-grid">
          <article class="card game-card" id="first-title" data-prerendered>
            <div class="game-cover">
              <div class="art" aria-hidden="true"></div>
              <div class="label"><div><span class="status">In production</span><h3>Our first title</h3><p>Currently in production</p></div></div>
            </div>
            <div class="body">
              <div class="meta"><span class="tag">To be announced</span> <span class="tag">Android</span></div>
              <p>We are building our first game right now. Screenshots, a trailer and the Google Play link will appear here the day it goes live.</p>
              <div class="store-row"><span class="store-badge disabled">{I['playmono']}<span><small>COMING TO</small>Google Play<span class="sr-only"> (not available yet)</span></span></span></div>
            </div>
          </article>
        </div>
        <div class="callout reveal" style="max-width:760px;margin-top:40px">
          <p><strong>Want a game built for your brand or idea?</strong> We build games for clients with the same team and pipeline. <a class="link-arrow" href="/contact/" style="display:inline-flex;margin-left:6px">Start a project {I['arrow']}</a></p>
        </div>
      </div>
    </section>
  </main>
'''
write('games/index.html', head(T,DESC,'/games/',ld)+header('/games/')+'\n  <main id="main">\n'+body+'\n  <script src="/js/games-data.js"></script>\n  <script src="/js/games.js" defer></script>\n'+FOOTER+SCRIPTS+'</body>\n</html>\n')

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

# sitemap
today='2026-11-04'
urls=[('/','1.0','monthly'),('/services/','0.9','monthly'),('/about/','0.7','monthly'),('/games/','0.9','weekly'),('/contact/','0.8','monthly'),('/privacy-policy/','0.4','yearly'),('/terms/','0.4','yearly')]
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{D}{u}</loc><lastmod>{today}</lastmod><changefreq>{c}</changefreq><priority>{p}</priority></url>\n' for u,p,c in urls)+'</urlset>\n')
print('pages written')
