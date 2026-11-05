/* StoneBuild Games admin: manage games, saved as site/data/games.json and images in the repository.
   Local mode (tools/serve.py) writes straight to disk. Online mode commits through the GitHub API;
   the host rebuilds the site after each commit. The token stays in this browser only. */
(function () {
  'use strict';
  const app = document.getElementById('app');
  const DATA_PATH = 'site/data/games.json';
  const NEED = 4;
  const IC = {
    games: '<path d="M6 11h4M8 9v4M15 12h.01M18 10h.01M17.3 5H6.7a4 4 0 0 0-4 3.6l-.6 7A3 3 0 0 0 5.1 19c.9 0 1.7-.4 2.3-1l1.6-1.8h6l1.6 1.8c.6.6 1.4 1 2.3 1a3 3 0 0 0 3-3.4l-.6-7a4 4 0 0 0-4-3.6Z"/>',
    set: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/>',
    up: '<path d="m6 15 6-6 6 6"/>', down: '<path d="m6 9 6 6 6-6"/>',
    edit: '<path d="m3 21 4-1L20 7l-3-3L4 17zM14 6l3 3"/>', copy: '<rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V6a2 2 0 0 1 2-2h8"/>',
    view: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>', del: '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
    site: '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    check: '<path d="m5 12 5 5L20 7"/>', file: '<path d="M6 2h9l4 4v16H6z"/><path d="M15 2v4h4"/>', home: '<path d="m3 11 9-8 9 8v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>', signout: '<path d="M15 4h4a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1h-4M10 17l5-5-5-5M15 12H3"/>'
  };
  const ic = (n) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${IC[n]}</svg>`;
  const esc = (v) => String(v == null ? '' : v).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const SDKS = [['admob', 'Google AdMob'], ['unityads', 'Unity Ads'], ['firebase', 'Firebase'], ['unityanalytics', 'Unity Analytics'], ['gpgs', 'Play Games Services'], ['gamecenter', 'Game Center']];
  const STORES = [['play', 'Google Play', 'https://play.google.com/store/apps/details?id=...', /^https:\/\/play\.google\.com\//], ['appStore', 'App Store', 'https://apps.apple.com/app/...', /^https:\/\/apps\.apple\.com\//], ['steam', 'Steam', 'https://store.steampowered.com/app/...', /^https:\/\/store\.steampowered\.com\//]];

  const MARK = '<svg viewBox="10 7 180 180" aria-hidden="true"><g stroke="#0a0a0b" stroke-width="3" stroke-linejoin="round"><polygon points="100,20 169.28,60 134.64,80 100,60 65.36,80 30.72,60" fill="#FF6A2B"/><polygon points="169.28,60 169.28,140 100,180 100,140 134.64,120 134.64,80" fill="#8B8B95"/><polygon points="30.72,60 65.36,80 65.36,120 100,140 100,180 30.72,140" fill="#FFFFFF"/><polygon points="100,100 134.64,120 100,140 65.36,120" fill="#9E411A"/><polygon points="100,60 100,100 65.36,120 65.36,80" fill="#55555E"/><polygon points="100,60 134.64,80 134.64,120 100,100" fill="#D4D4D8"/><polygon points="172,14 185.86,22 172,30 158.14,22" fill="#FF6A2B"/><polygon points="172,30 185.86,22 185.86,38 172,46" fill="#8B8B95"/><polygon points="158.14,22 172,30 172,46 158.14,38" fill="#FFFFFF"/></g></svg>';
  const S = { tab: 'basics', mode: null, gh: null, data: { settings: {}, games: [] }, view: 'list', edit: null, isNew: false, pending: {}, removed: [], previews: {}, q: '', dirty: false };

  /* ---------- helpers ---------- */
  function toast(msg, bad) { const t = document.getElementById('toast'); t.textContent = msg; t.className = 'on' + (bad ? ' bad' : ''); clearTimeout(toast.t); toast.t = setTimeout(() => { t.className = ''; }, bad ? 6000 : 3200); }
  function confirmBox(title, msg) { return new Promise((res) => { const d = document.getElementById('confirm'); document.getElementById('confirm-t').textContent = title; document.getElementById('confirm-m').textContent = msg; d.returnValue = 'no'; d.showModal(); d.addEventListener('close', () => res(d.returnValue === 'yes'), { once: true }); }); }
  const b64 = (str) => btoa(unescape(encodeURIComponent(str)));
  const slugify = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60);
  function imgSrc(p) { return S.previews[p] || p; }
  function imgFallback(root) { root.querySelectorAll('img[data-path]').forEach((im) => { im.onerror = () => { if (S.mode === 'github' && !im.dataset.tried) { im.dataset.tried = '1'; im.src = `https://raw.githubusercontent.com/${S.gh.owner}/${S.gh.repo}/${S.gh.branch}/site${im.dataset.path}`; } }; }); }
  const liveUrl = (p) => location.origin + p;
  const publicBase = 'https://stonebuildgames.com';

  /* ---------- storage ---------- */
  async function ghFetch(path, opts) {
    const r = await fetch(`https://api.github.com/repos/${S.gh.owner}/${S.gh.repo}${path}`, { ...opts, headers: { Authorization: `Bearer ${S.gh.token}`, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', ...(opts && opts.headers) } });
    if (!r.ok) { const e = new Error(r.status === 401 ? 'GitHub rejected this token.' : r.status === 403 || r.status === 404 ? 'This token cannot access that repository. Check its name and the token permissions.' : `GitHub error ${r.status}`); e.status = r.status; throw e; }
    return r.json();
  }
  async function loadData() {
    if (S.mode === 'local') { S.data = await (await fetch('/data/games.json', { cache: 'no-store' })).json(); }
    else { const f = await ghFetch(`/contents/${DATA_PATH}?ref=${encodeURIComponent(S.gh.branch)}`); S.data = JSON.parse(decodeURIComponent(escape(atob(f.content.replace(/\n/g, ''))))); }
    S.data.settings = S.data.settings || {}; S.data.games = S.data.games || [];
  }
  async function commit(message, extraDeletes) {
    const files = Object.entries(S.pending).map(([path, content]) => ({ path, content }));
    files.push({ path: DATA_PATH, content: b64(JSON.stringify(S.data, null, 2) + '\n') });
    const deletes = (extraDeletes || []).filter((d) => !S.pending[d]);
    if (S.mode === 'local') {
      const r = await fetch('/__admin/commit', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Admin-Local': '1' }, body: JSON.stringify({ files, deletes }) });
      const j = await r.json(); if (!r.ok) throw new Error(j.error || 'Save failed');
    } else {
      const ref = await ghFetch(`/git/ref/heads/${S.gh.branch}`);
      const head = await ghFetch(`/git/commits/${ref.object.sha}`);
      const tree = [];
      for (const f of files) { const b = await ghFetch('/git/blobs', { method: 'POST', body: JSON.stringify({ content: f.content, encoding: 'base64' }) }); tree.push({ path: f.path, mode: '100644', type: 'blob', sha: b.sha }); }
      for (const d of deletes) {
        try { await ghFetch(`/contents/${d}?ref=${encodeURIComponent(S.gh.branch)}`); tree.push({ path: d, mode: '100644', type: 'blob', sha: null }); } catch (e) { if (e.status !== 404) throw e; }
      }
      const t = await ghFetch('/git/trees', { method: 'POST', body: JSON.stringify({ base_tree: head.tree.sha, tree }) });
      const c = await ghFetch('/git/commits', { method: 'POST', body: JSON.stringify({ message: `Admin: ${message}`, tree: t.sha, parents: [head.sha] }) });
      await ghFetch(`/git/refs/heads/${S.gh.branch}`, { method: 'PATCH', body: JSON.stringify({ sha: c.sha }) });
    }
    S.pending = {};
  }
  async function saveAll(message, okMsg, deletes) {
    try { await commit(message, deletes); toast(okMsg || (S.mode === 'local' ? 'Saved. Site rebuilt on this computer.' : 'Saved. The live site updates in about a minute.')); return true; }
    catch (e) { toast(e.message || 'Save failed', true); return false; }
  }
  const gamePaths = (g) => [g.cover, g.icon, ...(g.screenshots || [])].filter(Boolean).map((p) => 'site' + p);

  /* ---------- images: resized in the browser before upload ---------- */
  async function processImage(file, w, h, fit) {
    if (!file.type.startsWith('image/')) throw new Error('Please choose an image file.');
    const bmp = await createImageBitmap(file);
    let cw, ch, sx = 0, sy = 0, sw = bmp.width, sh = bmp.height;
    if (fit === 'cover') { cw = w; ch = h; const r = Math.max(w / bmp.width, h / bmp.height); sw = w / r; sh = h / r; sx = (bmp.width - sw) / 2; sy = (bmp.height - sh) / 2; }
    else { const r = Math.min(1, w / Math.max(bmp.width, bmp.height)); cw = Math.round(bmp.width * r); ch = Math.round(bmp.height * r); }
    const c = document.createElement('canvas'); c.width = cw; c.height = ch; c.getContext('2d').drawImage(bmp, sx, sy, sw, sh, 0, 0, cw, ch);
    const url = c.toDataURL('image/webp', 0.86); const webp = url.startsWith('data:image/webp');
    const out = webp ? url : c.toDataURL('image/jpeg', 0.88);
    return { dataUrl: out, base64: out.split(',')[1], ext: webp ? 'webp' : 'jpg' };
  }
  function queueImage(id, name, res) {
    const fname = `${name}-${Date.now().toString(36)}.${res.ext}`; const pub = `/assets/games/${id}/${fname}`;
    S.pending['site' + pub] = res.base64; S.previews[pub] = res.dataUrl; return pub;
  }

  /* ---------- sign in ---------- */
  function loginShell(inner) {
    app.innerHTML = `<div class="a-login"><aside class="a-login-art"><img src="/assets/logo-dark.svg" alt="StoneBuild Games"><div class="a-login-mark">${MARK}</div><div><h2>Your games,<br><span>one place.</span></h2><p>Post games, manage store links and keep every privacy page up to date.</p></div></aside><div class="a-login-form">${inner}</div></div>`;
  }
  async function checkPassword(user, pass) {
    const A = window.SB_AUTH; const enc = new TextEncoder();
    const key = await crypto.subtle.importKey('raw', enc.encode(`${user}\n${pass}`), 'PBKDF2', false, ['deriveBits']);
    const salt = Uint8Array.from(atob(A.salt), (c) => c.charCodeAt(0));
    const bits = await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations: A.iter }, key, 256);
    return btoa(String.fromCharCode(...new Uint8Array(bits))) === A.hash;
  }
  /* Failed attempts slow down guessing in this browser. The token below is what actually protects publishing. */
  function attempts() { try { return JSON.parse(localStorage.getItem('sb-attempts')) || { n: 0, until: 0 }; } catch (e) { return { n: 0, until: 0 }; } }
  function saveAttempts(a) { try { localStorage.setItem('sb-attempts', JSON.stringify(a)); } catch (e) { /* storage blocked */ } }
  /* The GitHub token is only kept in memory, or encrypted with the admin password when remembered. */
  async function vaultCrypto(salt) { return crypto.subtle.deriveKey({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations: 600000 }, S.vaultKey, { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt']); }
  const toB64 = (u) => btoa(String.fromCharCode(...new Uint8Array(u))); const fromB64 = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
  async function vaultSave(obj) { const salt = crypto.getRandomValues(new Uint8Array(16)), iv = crypto.getRandomValues(new Uint8Array(12)); const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, await vaultCrypto(salt), new TextEncoder().encode(JSON.stringify(obj))); localStorage.setItem('sb-vault', JSON.stringify({ salt: toB64(salt), iv: toB64(iv), ct: toB64(ct) })); }
  async function vaultLoad() { const v = JSON.parse(localStorage.getItem('sb-vault')); const pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: fromB64(v.iv) }, await vaultCrypto(fromB64(v.salt)), fromB64(v.ct)); return JSON.parse(new TextDecoder().decode(pt)); }
  /* Lock after 20 idle minutes: reloading clears the token and key from memory. */
  function startIdleLock() { let t; const arm = () => { clearTimeout(t); t = setTimeout(() => { S.dirty = false; location.reload(); }, 20 * 60000); }; ['pointerdown', 'keydown'].forEach((ev) => window.addEventListener(ev, arm, { passive: true })); arm(); }
  function renderGate(error) {
    loginShell(`<form id="gate" autocomplete="on"><h1>Welcome back</h1><p class="sub">Sign in to manage your games.</p>${error ? `<p class="err-msg" role="alert">${esc(error)}</p>` : ''}
      <div class="field"><label for="g-user">Username</label><input id="g-user" name="username" autocomplete="username" required autofocus></div>
      <div class="field"><label for="g-pass">Password</label><input id="g-pass" name="password" type="password" autocomplete="current-password" required></div>
      <button class="btn btn-primary btn-lg">Sign in</button></form>`);
    document.getElementById('gate').addEventListener('submit', async (e) => {
      e.preventDefault(); const btn = e.target.querySelector('button'); btn.disabled = true; btn.textContent = 'Signing in...';
      const lock = attempts(); if (lock.until > Date.now()) return renderGate(`Too many attempts. Try again in ${Math.ceil((lock.until - Date.now()) / 60000)} minutes.`);
      const user = document.getElementById('g-user').value.trim(), pass = document.getElementById('g-pass').value;
      let ok = false; try { ok = await checkPassword(user, pass); } catch (err) { return renderGate('Sign in needs a secure connection (https).'); }
      if (!ok) { lock.n += 1; if (lock.n >= 5) { lock.until = Date.now() + 15 * 60000; lock.n = 0; } saveAttempts(lock); return renderGate('Wrong username or password.'); }
      saveAttempts({ n: 0, until: 0 });
      S.vaultKey = await crypto.subtle.importKey('raw', new TextEncoder().encode(`${user}\n${pass}`), 'PBKDF2', false, ['deriveKey']);
      startIdleLock(); boot();
    });
  }
  function renderLogin(error) {
    const saved = S.gh || {};
    loginShell(`<form id="login"><h1>Connect GitHub</h1><p class="sub">One step, once per browser. Saving publishes through your repository, so this needs an access token.</p>
      ${error ? `<p class="err-msg" role="alert">${esc(error)}</p>` : ''}
      <div class="a-grid2"><div class="field"><label for="l-repo">Repository</label><input id="l-repo" value="${esc(saved.owner ? saved.owner + '/' + saved.repo : 'userdevops-dual/stonebuildgames')}" required></div>
      <div class="field"><label for="l-branch">Branch</label><input id="l-branch" value="${esc(saved.branch || 'main')}" required></div></div>
      <div class="field"><label for="l-token">Access token</label><input id="l-token" type="password" autocomplete="off" required></div>
      <ol><li>Open <a href="https://github.com/settings/personal-access-tokens/new" target="_blank" rel="noopener">GitHub fine-grained tokens</a>.</li><li>Select only this repository.</li><li>Give it <b>Contents: Read and write</b> and a 90-day expiry, then create it.</li></ol>
      <label class="switch" style="margin-top:14px"><input type="checkbox" id="l-rem" ${localStorage.getItem('sb-vault') ? 'checked' : ''}>Remember on this computer, encrypted with your password</label>
      <button class="btn btn-primary btn-lg">Connect</button>
      <p class="hint" style="margin-top:12px">The token is only sent to GitHub, and it is never stored unencrypted.</p></form>`);
    document.getElementById('login').addEventListener('submit', async (e) => {
      e.preventDefault();
      const [owner, repo] = document.getElementById('l-repo').value.trim().split('/');
      S.gh = { owner, repo, branch: document.getElementById('l-branch').value.trim(), token: document.getElementById('l-token').value.trim() };
      const btn = e.target.querySelector('button'); btn.disabled = true; btn.textContent = 'Connecting...';
      try { S.mode = 'github'; await loadData(); if (document.getElementById('l-rem').checked) await vaultSave(S.gh); else localStorage.removeItem('sb-vault'); render(); }
      catch (err) { S.mode = null; renderLogin(err.message); }
    });
  }
  function signOut() { S.dirty = false; location.reload(); }

  /* ---------- shell ---------- */
  function shell(inner) {
    app.innerHTML = `<div class="a-shell"><aside class="a-side">
      <a class="a-logo" href="/" target="_blank" rel="noopener"><img src="/assets/logo-dark.svg" alt="StoneBuild Games"></a>
      <nav class="a-nav" aria-label="Admin">
        <button data-nav="list" class="${S.view === 'list' || S.view === 'edit' ? 'on' : ''}">${ic('games')}Games</button>
        <button data-nav="settings" class="${S.view === 'settings' ? 'on' : ''}">${ic('set')}Settings</button>
        <button data-nav="site">${ic('site')}View site</button>
      </nav>
      <div class="a-mode"><span>${S.mode === 'local' ? 'Local mode<b>Saving to this computer</b>' : `Connected to<b>${esc(S.gh.owner)}/${esc(S.gh.repo)}</b>`}</span><button class="a-signout" data-signout>Sign out</button></div>
    </aside><main class="a-main">${inner}</main></div>`;
    app.querySelectorAll('[data-nav]').forEach((b) => b.addEventListener('click', async () => {
      if (b.dataset.nav === 'site') return window.open('/', '_blank', 'noopener');
      if (S.dirty && !(await leaveOk())) return;
      S.view = b.dataset.nav; S.edit = null; S.dirty = false; S.pending = {}; render();
    }));
    const so = app.querySelector('[data-signout]'); if (so) so.addEventListener('click', signOut);
    imgFallback(app);
  }
  function leaveOk() { return Promise.resolve(window.confirm('You have unsaved changes. Leave without saving?')); }
  function render() { if (S.view === 'edit') renderEdit(); else if (S.view === 'settings') renderSettings(); else renderList(); }

  /* ---------- game list ---------- */
  function renderList() {
    const all = S.data.games, pub = all.filter((g) => g.status === 'published').length, left = Math.max(0, NEED - pub);
    const q = S.q.toLowerCase(), list = all.filter((g) => !q || (g.name || '').toLowerCase().includes(q));
    const rows = list.map((g) => {
      const i = all.indexOf(g); const st = STORES.filter(([k]) => g[k + 'On'] && g[k + 'Url']).map(([, l]) => `<span>${l}</span>`).join('') || '<span>No stores</span>';
      return `<div class="a-row" data-id="${esc(g.id)}">
        ${g.cover ? `<img src="${esc(imgSrc(g.cover))}" data-path="${esc(g.cover)}" alt="">` : '<div class="a-thumb"></div>'}
        <div><h3>${esc(g.name) || 'Untitled'}</h3><small>${esc(g.genre)}${g.version ? ' · v' + esc(g.version) : ''}</small></div>
        <div class="h-m"><span class="a-pill ${g.status === 'published' ? 'pub' : ''}">${g.status === 'published' ? 'Published' : 'Draft'}</span></div>
        <div class="h-m"><small>${g.rating ? '★ ' + esc(g.rating) : 'No rating'}</small><small>${g.downloads ? esc(g.downloads) + ' downloads' : ''}</small></div>
        <div class="a-stores h-m" style="flex-wrap:wrap">${st}</div>
        <div class="a-rowact">
          <button class="icon-btn" data-act="up" title="Move up" aria-label="Move ${esc(g.name)} up" ${i === 0 ? 'disabled' : ''}>${ic('up')}</button>
          <button class="icon-btn" data-act="down" title="Move down" aria-label="Move ${esc(g.name)} down" ${i === all.length - 1 ? 'disabled' : ''}>${ic('down')}</button>
          <button class="icon-btn" data-act="edit" title="Edit" aria-label="Edit ${esc(g.name)}">${ic('edit')}</button>
          <button class="icon-btn" data-act="dup" title="Duplicate" aria-label="Duplicate ${esc(g.name)}">${ic('copy')}</button>
          ${g.status === 'published' ? `<a class="icon-btn" href="/games/${esc(g.id)}/" target="_blank" rel="noopener" title="View page" aria-label="View ${esc(g.name)} page">${ic('view')}</a>` : ''}
          <button class="icon-btn danger" data-act="del" title="Delete" aria-label="Delete ${esc(g.name)}">${ic('del')}</button>
        </div></div>`;
    }).join('');
    shell(`<div class="a-top"><div><h1>Games</h1><p>Post, edit and order the games on your website.</p></div><div class="a-actions"><input class="a-search" id="search" type="search" placeholder="Search games" aria-label="Search games" value="${esc(S.q)}"><button class="btn btn-primary" id="new">Add game</button></div></div>
      <div class="a-stats">
        <div class="a-stat"><i>${ic('games')}</i><div><b>${all.length}</b><span>Total games</span></div></div>
        <div class="a-stat"><i>${ic('check')}</i><div><b>${pub}</b><span>Published</span></div></div>
        <div class="a-stat"><i>${ic('file')}</i><div><b>${all.length - pub}</b><span>Drafts</span></div></div>
        <div class="a-stat hot"><i>${ic('home')}</i><div><b>${Math.min(pub, NEED)}/${NEED}</b><span>${left ? `${left} more to show on the home page` : 'Showing on the home page'}</span><div class="a-bar"><i style="width:${Math.min(100, pub / NEED * 100)}%"></i></div></div></div>
      </div>
      <div class="a-list">${rows ? `<div class="a-head"><span>Game</span><span>Status</span><span>Rating</span><span>Stores</span><span></span></div>${rows}` : (all.length ? '<div class="a-empty"><p>No game matches your search.</p></div>' : `<div class="a-empty"><div style="width:84px">${MARK}</div><h2>No games yet</h2><p>Add your first game. It stays a draft until you publish it.</p><button class="btn btn-primary" id="new2">Add your first game</button></div>`)}</div>
      ${all.length > 1 ? '<p class="hint" style="margin-top:10px">The first six published games appear on the home page, in this order.</p>' : ''}`);
    document.getElementById('new').addEventListener('click', () => openEdit(null));
    const n2 = document.getElementById('new2'); if (n2) n2.addEventListener('click', () => openEdit(null));
    const se = document.getElementById('search'); se.addEventListener('input', () => { S.q = se.value; renderList(); const n = document.getElementById('search'); n.focus(); n.setSelectionRange(n.value.length, n.value.length); });
    app.querySelectorAll('.a-row').forEach((row) => {
      const id = row.dataset.id, g = all.find((x) => x.id === id);
      row.querySelectorAll('[data-act]').forEach((b) => b.addEventListener('click', async () => {
        const a = b.dataset.act, i = all.indexOf(g);
        if (a === 'edit') return openEdit(g);
        if (a === 'up' || a === 'down') { const j = a === 'up' ? i - 1 : i + 1; [all[i], all[j]] = [all[j], all[i]]; renderList(); await saveAll(`reorder games`); return; }
        if (a === 'dup') { const c = JSON.parse(JSON.stringify(g)); c.name = g.name + ' copy'; c.id = uniqueId(slugify(c.name)); c.status = 'draft'; all.splice(i + 1, 0, c); renderList(); await saveAll(`duplicate ${g.name}`); return; }
        if (a === 'del' && await confirmBox(`Delete ${g.name}?`, 'This removes the game, its images and all its public pages, including its privacy policy. If the game is on a store, its store listing will point to a missing page.')) { all.splice(i, 1); renderList(); const shared = new Set(all.flatMap(gamePaths)); await saveAll(`delete ${g.name}`, null, gamePaths(g).filter((x) => !shared.has(x))); renderList(); }
      }));
    });
  }
  function uniqueId(base) { let id = base || 'game', n = 2; while (S.data.games.some((g) => g.id === id)) id = `${base}-${n++}`; return id; }

  /* ---------- settings ---------- */
  function renderSettings() {
    const s = S.data.settings;
    const f = (id, label, val, hint, type) => `<div class="field"><label for="${id}">${label}</label><input id="${id}" type="${type || 'text'}" value="${esc(val)}">${hint ? `<small>${hint}</small>` : ''}</div>`;
    const soc = s.social || {};
    const socials = [['instagram', 'Instagram'], ['x', 'X'], ['reddit', 'Reddit'], ['tiktok', 'TikTok'], ['linkedin', 'LinkedIn'], ['youtube', 'YouTube']].map(([k, l]) => f('so-' + k, l, soc[k], '', 'url')).join('');
    shell(`<div class="a-top"><div><h1>Settings</h1><p>Details used across the whole website.</p></div><button class="btn btn-primary" id="save">Save settings</button></div>
      <div class="a-panel"><h2>Developer details</h2><p class="hint">Shown on game pages and in every privacy policy. Google requires these to match your store listing.</p>
        <div class="a-grid2">${f('s-dev', 'Developer name', s.developerName, 'Exactly as on Google Play')}${f('s-legal', 'Legal name', s.legalName, 'Your company or full legal name')}${f('s-country', 'Country', s.country)}${f('s-mail', 'Support email', s.supportEmail, '', 'email')}</div></div>
      <div class="a-panel"><h2>Social links</h2><p class="hint">Each link you fill in appears as an icon in the website footer. Leave a field empty to hide its icon.</p><div class="a-grid2">${socials}</div></div>
      <div class="a-panel"><h2>Home page store buttons</h2><p class="hint">Your developer pages. While a field is empty, its button says "Coming to" and opens the games page.</p>
        <div class="a-grid2">${f('s-play', 'Google Play developer page', s.playDeveloperUrl, 'https://play.google.com/store/apps/dev?id=...', 'url')}${f('s-app', 'App Store developer page', s.appStoreDeveloperUrl, 'https://apps.apple.com/developer/...', 'url')}</div></div>`);
    document.getElementById('save').addEventListener('click', async (e) => {
      const urls = ['s-play', 's-app'].map((i) => document.getElementById(i).value.trim());
      const social = {}; ['instagram', 'x', 'reddit', 'tiktok', 'linkedin', 'youtube'].forEach((k) => { social[k] = document.getElementById('so-' + k).value.trim(); });
      if ([...urls, ...Object.values(social)].some((u) => u && !/^https:\/\//.test(u))) return toast('Links must start with https://', true);
      Object.assign(s, { developerName: document.getElementById('s-dev').value.trim(), legalName: document.getElementById('s-legal').value.trim(), country: document.getElementById('s-country').value.trim(), supportEmail: document.getElementById('s-mail').value.trim(), playDeveloperUrl: urls[0], appStoreDeveloperUrl: urls[1], social });
      e.target.disabled = true; await saveAll('update settings'); e.target.disabled = false;
    });
  }

  /* ---------- editor ---------- */
  function blank() { return { id: '', name: '', tagline: '', description: '', features: [], genre: '', platforms: ['Android'], status: 'draft', released: '', updated: new Date().toISOString().slice(0, 10), version: '', size: '', ageRating: '', rating: '', ratingCount: '', downloads: '', cover: '', icon: '', screenshots: [], trailer: '', playOn: false, playUrl: '', appStoreOn: false, appStoreUrl: '', steamOn: false, steamUrl: '', ads: false, iap: false, accounts: false, children: false, sdks: [] }; }
  function openEdit(g) { S.isNew = !g; S.edit = g ? { ...blank(), ...JSON.parse(JSON.stringify(g)) } : blank(); S.editOrig = g; S.removed = []; S.pending = {}; S.dirty = false; S.tab = 'basics'; S.view = 'edit'; render(); window.scrollTo(0, 0); }
  function publishChecks(g) { return [['Name', !!g.name.trim()], ['Short tagline', !!g.tagline.trim()], ['Description', g.description.trim().length >= 40], ['Card image', !!g.cover]]; }
  function storeProblem(g) { for (const [k, label, , rx] of STORES) { if (g[k + 'On']) { const u = (g[k + 'Url'] || '').trim(); if (!u) return `${label} is on, so add its link or switch it off.`; if (!rx.test(u)) return `The ${label} link does not look right. It should start with ${String(rx.source).replace(/\\/g, '').replace('^', '')}`; } } if (g.trailer && !/^https:\/\//.test(g.trailer)) return 'The trailer link must start with https://'; const r = parseFloat(g.rating); if (g.rating !== '' && (isNaN(r) || r < 0 || r > 5)) return 'Rating must be between 0 and 5.'; return ''; }
  function renderEdit() {
    const g = S.edit;
    const fld = (k, label, hint, attrs) => `<div class="field"><label for="f-${k}">${label}</label><input id="f-${k}" data-k="${k}" value="${esc(g[k])}" ${attrs || ''}>${hint ? `<small>${hint}</small>` : ''}</div>`;
    const stores = STORES.map(([k, l, ph]) => `<div class="a-store"><label class="switch"><input type="checkbox" data-c="${k}On" ${g[k + 'On'] ? 'checked' : ''}>On ${l}</label><div class="field" ${g[k + 'On'] ? '' : 'hidden'} data-store="${k}"><label for="f-${k}Url">${l} link</label><input id="f-${k}Url" data-k="${k}Url" type="url" value="${esc(g[k + 'Url'])}" placeholder="${ph}"></div></div>`).join('');
    const sw = (k, l) => `<label class="switch"><input type="checkbox" data-c="${k}" ${g[k] ? 'checked' : ''}>${l}</label>`;
    const shots = (g.screenshots || []).map((p, i) => `<div class="a-shot"><img src="${esc(imgSrc(p))}" data-path="${esc(p)}" alt="Screenshot ${i + 1}"><div class="bar"><button type="button" data-shot="left" data-i="${i}" aria-label="Move left">←</button><button type="button" data-shot="del" data-i="${i}" aria-label="Remove screenshot">✕</button><button type="button" data-shot="right" data-i="${i}" aria-label="Move right">→</button></div></div>`).join('');
    const legal = g.id ? ['privacy', 'terms', 'support', 'delete-data'].map((k) => `<div class="a-url"><span>${{ privacy: 'Privacy policy', terms: 'Terms', support: 'Support', 'delete-data': 'Delete data' }[k]}</span><code><span>${publicBase}/games/${esc(g.id)}/${k}/</span><button type="button" data-copy="${publicBase}/games/${esc(g.id)}/${k}/">Copy</button></code></div>`).join('') : '<p class="hint">Links appear after the first save.</p>';
    const tabs = [['basics', 'Basics'], ['images', 'Images'], ['stores', 'Stores'], ['stats', 'Rating and downloads'], ['privacy', 'Privacy']];
    const pane = (k, html) => `<div data-pane="${k}" ${S.tab === k ? '' : 'hidden'}>${html}</div>`;
    shell(`<div class="a-bar-top"><div><button class="a-link" id="back">← All games</button><h1>${S.isNew ? 'Add game' : esc(S.editOrig.name)} <span class="a-pill ${g.status === 'published' ? 'pub' : ''}">${g.status === 'published' ? 'Published' : 'Draft'}</span></h1></div>
        <div class="a-actions"><span class="a-dirty" id="dirty" ${S.dirty ? '' : 'hidden'}>Unsaved changes</span><button class="btn btn-ghost" id="draft">Save as draft</button><button class="btn btn-primary" id="publish">${g.status === 'published' ? 'Save and publish' : 'Publish'}</button></div></div>
      <div class="a-edit"><div>
        <div class="a-tabs" role="tablist">${tabs.map(([k, l]) => `<button type="button" role="tab" data-tab="${k}" aria-selected="${S.tab === k}" class="${S.tab === k ? 'on' : ''}">${l}</button>`).join('')}</div>
        ${pane('basics', `<div class="a-panel"><h2>Game details</h2>
          ${fld('name', 'Game name', '', 'required maxlength="60"')}
          ${fld('tagline', 'Short tagline', 'One line under the name', 'maxlength="110"')}
          <div class="field"><label for="f-description">Description</label><textarea id="f-description" data-k="description" rows="7">${esc(g.description)}</textarea><small>Leave a blank line between paragraphs.</small></div>
          <div class="field"><label for="f-features">Features</label><textarea id="f-features" rows="4" placeholder="One feature on each line">${esc((g.features || []).join('\n'))}</textarea></div>
        </div><div class="a-panel"><h2>Facts</h2>
          <div class="a-grid3">${fld('genre', 'Genre', '', 'placeholder="Puzzle"')}${fld('version', 'Version', '', 'placeholder="1.0.0"')}${fld('size', 'Size', '', 'placeholder="85 MB"')}${fld('ageRating', 'Age rating', '', 'placeholder="Everyone"')}${fld('released', 'Release date', '', 'type="date"')}${fld('updated', 'Last updated', '', 'type="date"')}</div>
          <div class="a-label" style="margin-top:16px">Platforms</div><div class="a-checks" style="margin-top:0;grid-template-columns:repeat(4,auto);justify-content:start">${['Android', 'iOS', 'PC', 'Web'].map((p) => `<label class="switch"><input type="checkbox" data-p="${p}" ${(g.platforms || []).includes(p) ? 'checked' : ''}>${p}</label>`).join('')}</div>
        </div>`)}
        ${pane('images', `<div class="a-panel"><h2>Images</h2><p class="hint">Click a box or drop a file on it. Images are resized for you, and the card image is cropped to a wide horizontal shape (12:5).</p>
          <div class="a-media">
            <div><div class="a-label">Card image</div><label class="drop cover">${g.cover ? `<img src="${esc(imgSrc(g.cover))}" data-path="${esc(g.cover)}" alt="Card image">` : '<span>Upload wide image</span>'}<input type="file" accept="image/*" data-img="cover" aria-label="Upload card image"></label></div>
            <div><div class="a-label">App icon</div><label class="drop icon">${g.icon ? `<img src="${esc(imgSrc(g.icon))}" data-path="${esc(g.icon)}" alt="App icon">` : '<span>Upload square</span>'}<input type="file" accept="image/*" data-img="icon" aria-label="Upload app icon"></label></div>
            <div><div class="a-label">Screenshots</div><div class="a-shots">${shots}<label class="drop add"><span>+ Add</span><input type="file" accept="image/*" multiple data-img="shots" aria-label="Add screenshots"></label></div></div>
          </div>
          ${fld('trailer', 'Trailer link', 'Optional YouTube link', 'type="url" placeholder="https://www.youtube.com/watch?v=..."')}</div>`)}
        ${pane('stores', `<div class="a-panel"><h2>Stores</h2><p class="hint">Only the stores you switch on appear on the website.</p>${stores}</div>`)}
        ${pane('stats', `<div class="a-panel"><h2>Rating and downloads</h2><p class="hint">Copy these from your store listing, and keep them true. Leave empty to hide them.</p>
          <div class="a-grid3">${fld('rating', 'Rating (0 to 5)', '', 'type="number" min="0" max="5" step="0.1"')}${fld('ratingCount', 'Number of ratings', '', 'placeholder="1,200"')}${fld('downloads', 'Downloads', '', 'placeholder="10K+"')}</div></div>`)}
        ${pane('privacy', `<div class="a-panel"><h2>Privacy details</h2><p class="hint">These answers write this game's privacy policy. They must match your Google Play Data safety form.</p>
          <div class="a-checks">${sw('ads', 'Shows ads')}${sw('iap', 'In-app purchases')}${sw('accounts', 'Players can create accounts')}${sw('children', 'Made for children')}</div>
          <div class="a-label" style="margin-top:18px">Services used in the game</div><div class="a-checks" style="margin-top:0">${SDKS.map(([k, l]) => `<label class="switch"><input type="checkbox" data-s="${k}" ${(g.sdks || []).includes(k) ? 'checked' : ''}>${l}</label>`).join('')}</div></div>`)}
      </div>
      <div class="a-side-col">
        <div class="a-prev"><div class="a-label">Card preview</div><div class="gc" id="prev"></div></div>
        <div class="a-panel" style="margin:0"><h2>Ready to publish</h2><ul class="a-check" id="checks"></ul></div>
        <div class="a-panel" style="margin:0"><h2>Links for your store listing</h2><p class="hint">Paste these into Play Console and App Store Connect.</p>${legal}</div>
      </div></div>`);
    wireEdit();
  }
  function refreshSide() {
    const g = S.edit, p = document.getElementById('prev'); if (!p) return;
    const first = STORES.find(([k]) => g[k + 'On'] && g[k + 'Url']);
    p.innerHTML = (g.cover ? `<img src="${esc(imgSrc(g.cover))}" data-path="${esc(g.cover)}" alt="">` : '<div class="art-empty">No image yet</div>') + `<div class="gc-over"><h3>${esc(g.name) || 'Game name'}</h3><div class="gc-actions">${first ? `<span class="btn btn-primary btn-sm">${first[1]}</span>` : ''}<span class="btn btn-light btn-sm">Explore</span></div></div>`;
    imgFallback(p);
    document.getElementById('checks').innerHTML = publishChecks(g).map(([l, ok]) => `<li class="${ok ? 'ok' : ''}"><i></i>${l}</li>`).join('');
  }
  function wireEdit() {
    const g = S.edit;
    const touch = () => { S.dirty = true; const d = document.getElementById('dirty'); if (d) d.hidden = false; refreshSide(); };
    app.querySelectorAll('[data-tab]').forEach((b) => b.addEventListener('click', () => { S.tab = b.dataset.tab; app.querySelectorAll('[data-tab]').forEach((x) => { const on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-selected', on); }); app.querySelectorAll('[data-pane]').forEach((p) => { p.hidden = p.dataset.pane !== S.tab; }); }));
    app.querySelectorAll('[data-k]').forEach((el) => el.addEventListener('input', () => { g[el.dataset.k] = el.value; touch(); }));
    document.getElementById('f-features').addEventListener('input', (e) => { g.features = e.target.value.split('\n').map((x) => x.trim()).filter(Boolean); touch(); });
    app.querySelectorAll('[data-c]').forEach((el) => el.addEventListener('change', () => { g[el.dataset.c] = el.checked; const m = el.dataset.c.match(/^(play|appStore|steam)On$/); if (m) app.querySelector(`[data-store="${m[1]}"]`).hidden = !el.checked; touch(); }));
    app.querySelectorAll('[data-p]').forEach((el) => el.addEventListener('change', () => { const s = new Set(g.platforms); el.checked ? s.add(el.dataset.p) : s.delete(el.dataset.p); g.platforms = ['Android', 'iOS', 'PC', 'Web'].filter((x) => s.has(x)); touch(); }));
    app.querySelectorAll('[data-s]').forEach((el) => el.addEventListener('change', () => { const s = new Set(g.sdks); el.checked ? s.add(el.dataset.s) : s.delete(el.dataset.s); g.sdks = [...s]; touch(); }));
    app.querySelectorAll('[data-copy]').forEach((b) => b.addEventListener('click', async () => { try { await navigator.clipboard.writeText(b.dataset.copy); toast('Link copied'); } catch (e) { toast('Could not copy. Select the text instead.', true); } }));
    app.querySelectorAll('[data-img]').forEach((el) => el.addEventListener('change', async () => {
      const kind = el.dataset.img; const files = [...el.files]; if (!files.length) return;
      const id = g.id || (g.id = uniqueId(slugify(g.name) || 'game'));
      try {
        if (kind === 'cover') { const r = await processImage(files[0], 1440, 600, 'cover'); if (g.cover) { S.removed.push('site' + g.cover); delete S.pending['site' + g.cover]; } g.cover = queueImage(id, 'cover', r); }
        else if (kind === 'icon') { const r = await processImage(files[0], 512, 512, 'cover'); if (g.icon) { S.removed.push('site' + g.icon); delete S.pending['site' + g.icon]; } g.icon = queueImage(id, 'icon', r); }
        else { for (let i = 0; i < files.length; i++) { const r = await processImage(files[i], 1600, 1600, 'fit'); g.screenshots.push(queueImage(id, `shot-${i}`, r)); } }
        S.dirty = true; renderEdit();
      } catch (e) { toast(e.message || 'That image could not be read.', true); }
    }));
    app.querySelectorAll('[data-shot]').forEach((b) => b.addEventListener('click', () => {
      const i = +b.dataset.i, a = g.screenshots, act = b.dataset.shot;
      if (act === 'del') { S.removed.push('site' + a[i]); delete S.pending['site' + a[i]]; a.splice(i, 1); }
      else { const j = act === 'left' ? i - 1 : i + 1; if (j < 0 || j >= a.length) return; [a[i], a[j]] = [a[j], a[i]]; }
      S.dirty = true; renderEdit();
    }));
    document.getElementById('back').addEventListener('click', async () => { if (S.dirty && !(await leaveOk())) return; S.view = 'list'; S.edit = null; S.dirty = false; S.pending = {}; render(); });
    document.getElementById('draft').addEventListener('click', (e) => saveGame('draft', e.target));
    document.getElementById('publish').addEventListener('click', (e) => saveGame('published', e.target));
    refreshSide();
  }
  async function saveGame(status, btn) {
    const g = S.edit;
    if (!g.name.trim()) { toast('Add a game name first.', true); S.tab = 'basics'; app.querySelector('[data-tab=basics]').click(); document.getElementById('f-name').focus(); return; }
    const bad = storeProblem(g); if (bad) return toast(bad, true);
    if (status === 'published') { const miss = publishChecks(g).filter(([, ok]) => !ok).map(([l]) => l); if (miss.length) return toast(`To publish, still needed: ${miss.join(', ')}. The description needs at least 40 characters.`, true); }
    if (S.isNew && !g.id) g.id = uniqueId(slugify(g.name));
    if (S.isNew && S.data.games.some((x) => x.id === g.id)) g.id = uniqueId(g.id);
    g.status = status; ['name', 'tagline', 'genre', 'playUrl', 'appStoreUrl', 'steamUrl', 'trailer'].forEach((k) => { g[k] = (g[k] || '').trim(); });
    const list = S.data.games, backup = JSON.stringify(list), i = S.editOrig ? list.indexOf(S.editOrig) : -1;
    const copy = JSON.parse(JSON.stringify(g));
    if (i >= 0) list[i] = copy; else list.push(copy);
    const removed = [...new Set(S.removed)].filter((p) => !gamePaths(g).includes(p));
    btn.disabled = true; const label = btn.textContent; btn.textContent = 'Saving...';
    const ok = await saveAll(`${S.isNew ? 'add' : 'update'} ${g.name}`, status === 'published' ? (S.mode === 'local' ? 'Published. Site rebuilt on this computer.' : 'Published. The live site updates in about a minute.') : 'Draft saved.', removed);
    btn.disabled = false; btn.textContent = label;
    if (!ok) { S.data.games = JSON.parse(backup); S.editOrig = S.editOrig ? S.data.games[i] : null; return; }
    S.dirty = false; S.view = 'list'; S.edit = null; render();
  }
  window.addEventListener('beforeunload', (e) => { if (S.dirty) { e.preventDefault(); e.returnValue = ''; } });

  /* ---------- start ---------- */
  async function boot() {
    try { const r = await fetch('/__admin/ping', { cache: 'no-store' }); if (r.ok) { S.mode = 'local'; await loadData(); return render(); } } catch (e) { /* not running locally */ }
    if (localStorage.getItem('sb-vault')) {
      try { S.gh = await vaultLoad(); S.mode = 'github'; await loadData(); return render(); }
      catch (e) { S.mode = null; if (e.name === 'OperationError') { localStorage.removeItem('sb-vault'); S.gh = null; return renderLogin(); } return renderLogin(e.message); }
    }
    renderLogin();
  }
  (function start() {
    localStorage.removeItem('sb-admin'); sessionStorage.removeItem('sb-admin'); sessionStorage.removeItem('sb-auth'); // older plain storage
    renderGate();
  })();
})();
