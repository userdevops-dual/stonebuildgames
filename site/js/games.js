/* Renders window.STONEBUILD_GAMES into #games-grid and emits VideoGame structured data */
(function () {
  'use strict';
  const grid = document.getElementById('games-grid');
  const games = Array.isArray(window.STONEBUILD_GAMES) ? window.STONEBUILD_GAMES : [];
  if (!grid) return;
  const prerendered = grid.querySelectorAll('[data-prerendered]');

  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const STATUS = { 'live': ['Available now', 'live'], 'coming-soon': ['Coming soon', ''], 'in-production': ['In production', ''] };

  const playIcon = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#34a853" d="M3.6 2.4 13.3 12l-9.7 9.6c-.4-.2-.6-.7-.6-1.3V3.7c0-.6.2-1.1.6-1.3z"/><path fill="#4285f4" d="M16.6 8.7 13.3 12l3.3 3.3 3.9-2.2c1.1-.6 1.1-1.6 0-2.2z"/><path fill="#fbbc04" d="M3.6 2.4c.3-.2.8-.2 1.3.1l11.7 6.2L13.3 12z"/><path fill="#ea4335" d="M13.3 12 3.6 21.6c.3.2.8.2 1.3-.1l11.7-6.2z"/></svg>';
  const appleIcon = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="#fff"><path d="M16.4 12.6c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9-.7 0-1.9-.8-3.1-.8-1.6 0-3.1.9-3.9 2.4-1.7 2.9-.4 7.2 1.2 9.6.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.1-.8s1.9.8 3.1.8c1.3 0 2.1-1.2 2.9-2.3.9-1.3 1.3-2.6 1.3-2.7-.1 0-2.7-1-2.7-4.2zM14.1 5.8c.6-.8 1.1-1.8 1-2.8-.9 0-2 .6-2.7 1.4-.6.7-1.1 1.7-1 2.7 1 .1 2-.5 2.7-1.3z"/></svg>';
  const steamIcon = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="#fff"><path d="M12 2a10 10 0 0 0-10 9.3l5.4 2.2a2.8 2.8 0 0 1 1.6-.5h.2l2.4-3.5v-.1a3.8 3.8 0 1 1 3.8 3.8h-.1l-3.4 2.4v.2a2.8 2.8 0 0 1-5.6.3L2.4 14.6A10 10 0 1 0 12 2zm-5.7 15.2 1.3.5a2.1 2.1 0 1 0 1.2-4l-1.3-.5a1.5 1.5 0 1 1-1.2 4zm9.1-6a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zm0-4.4a1.9 1.9 0 1 1 0 3.8 1.9 1.9 0 0 1 0-3.8z"/></svg>';

  function badge(href, icon, small, label) {
    if (!href) return `<span class="store-badge disabled">${icon}<span><small>COMING TO</small>${label}<span class="sr-only"> (not available yet)</span></span></span>`;
    return `<a class="store-badge" href="${esc(href)}" target="_blank" rel="noopener">${icon}<span><small>${small}</small>${label}<span class="sr-only"> (opens in a new tab)</span></span></a>`;
  }

  function card(g) {
    const [statusLabel, statusCls] = STATUS[g.status] || STATUS['coming-soon'];
    const art = g.cover
      ? `<img class="art art-img" src="${esc(g.cover)}" alt="${esc(g.title)} cover art" loading="lazy" width="1600" height="1000">`
      : `<div class="art" aria-hidden="true"></div>`;
    const stores = [
      badge(g.playStore, playIcon, 'GET IT ON', 'Google Play'),
      g.appStore || g.platforms?.includes('iOS') ? badge(g.appStore, appleIcon, 'Download on the', 'App Store') : '',
      g.steam || g.platforms?.includes('PC') ? badge(g.steam, steamIcon, 'Available on', 'Steam') : ''
    ].join('');
    return `
      <article class="card game-card${prerendered.length ? '' : ' reveal'}" id="${esc(g.id)}">
        <div class="game-cover">${art}
          <div class="label"><div><span class="status ${statusCls}">${statusLabel}</span><h3>${esc(g.title)}</h3><p>${esc(g.tagline)}</p></div></div>
        </div>
        <div class="body">
          <div class="meta"><span class="tag">${esc(g.genre)}</span>${(g.platforms || []).map((p) => `<span class="tag">${esc(p)}</span>`).join('')}</div>
          <p>${esc(g.description)}</p>
          <div class="store-row">${stores}</div>
        </div>
      </article>`;
  }

  prerendered.forEach((n) => n.remove());
  grid.insertAdjacentHTML('afterbegin', games.map(card).join(''));

  // Structured data for live games (VideoGame inside an ItemList)
  const live = games.filter((g) => g.status === 'live');
  if (live.length) {
    const ORG = { '@type': 'Organization', '@id': 'https://stonebuildgames.com/#organization', 'name': 'StoneBuild Games', 'url': 'https://stonebuildgames.com/' };
    const OS = { Android: 'Android', iOS: 'iOS', PC: 'Windows', Web: 'Web browser' };
    const ld = {
      '@context': 'https://schema.org', '@type': 'ItemList', '@id': 'https://stonebuildgames.com/games/#gamelist',
      'mainEntityOfPage': 'https://stonebuildgames.com/games/#webpage',
      'itemListElement': live.map((g, i) => {
        const stores = [g.playStore, g.appStore, g.steam].filter(Boolean);
        const os = (g.platforms || []).map((p) => OS[p]).filter(Boolean);
        const item = {
          '@type': 'VideoGame', '@id': `https://stonebuildgames.com/games/#${g.id}`, 'name': g.title, 'description': g.description, 'genre': g.genre,
          'url': `https://stonebuildgames.com/games/#${g.id}`, 'gamePlatform': g.platforms, 'applicationCategory': 'GameApplication',
          'author': ORG, 'publisher': ORG,
          'offers': { '@type': 'Offer', 'price': String(g.price ?? '0'), 'priceCurrency': g.currency || 'USD', 'availability': 'https://schema.org/InStock', 'url': stores[0] }
        };
        if (os.length) item.operatingSystem = os.join(', ');
        if (g.released) item.datePublished = g.released;
        if (g.cover) item.image = new URL(g.cover, 'https://stonebuildgames.com/').href;
        if (stores.length) { item.installUrl = stores[0]; item.sameAs = stores; }
        return { '@type': 'ListItem', 'position': i + 1, 'item': item };
      })
    };
    const s = document.createElement('script'); s.type = 'application/ld+json'; s.textContent = JSON.stringify(ld); document.head.appendChild(s);
  }
})();
