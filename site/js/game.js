/* Stone Stack — isometric stacking game. Tap, click or press Space to drop the block. */
(function () {
  'use strict';
  const root = document.getElementById('stack-game');
  if (!root) return;

  const canvas = root.querySelector('canvas');
  const ctx = canvas.getContext('2d');
  const $ = (s) => root.querySelector(s);
  const startPanel = $('.game-start'), overPanel = $('.game-over'), cta = $('.game-cta');
  const scoreEl = $('.game-score'), bestEl = $('[data-best]'), finalEl = $('[data-final]'), subEl = $('[data-sub]');
  const soundBtn = $('.game-sound');

  const SIZE = 100, H = 17, COS = Math.cos(Math.PI / 6), SIN = 0.5;
  const PERFECT = 4.5, SWING = 150;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let W = 0, HT = 0, u = 1;
  let state = 'idle', blocks = [], mover = null, debris = [], rings = [], sparks = [], floats = [];
  let score = 0, best = 0, streak = 0, camY = 0, camTarget = 0, inView = !('IntersectionObserver' in window), lastT = 0, overAt = 0, muted = false, audio = null, ignoreClick = false;

  try { best = parseInt(localStorage.getItem('sb-stack-best'), 10) || 0; muted = localStorage.getItem('sb-stack-muted') === '1'; } catch (e) { /* storage blocked */ }

  /* ---------- Sound ---------- */
  function tone(freq, dur, type, vol) {
    if (muted) return;
    try {
      audio = audio || new (window.AudioContext || window.webkitAudioContext)();
      if (audio.state === 'suspended') audio.resume();
      const o = audio.createOscillator(), g = audio.createGain(), t = audio.currentTime;
      o.type = type || 'triangle'; o.frequency.value = freq;
      g.gain.setValueAtTime(vol || 0.05, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g).connect(audio.destination); o.start(t); o.stop(t + dur);
    } catch (e) { /* audio unavailable */ }
  }

  /* ---------- Isometric helpers ---------- */
  const px = (x, z, y) => [W / 2 + (x - z) * COS * u, HT * 0.68 + (x + z) * SIN * u - (y - camY) * u];
  function face(pts, fill, line) {
    ctx.beginPath();
    pts.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])));
    ctx.closePath(); ctx.fillStyle = fill; ctx.fill();
    ctx.strokeStyle = line || '#ffffff'; ctx.lineWidth = Math.max(1, u * 1.1); ctx.lineJoin = 'round'; ctx.stroke();
  }
  function topColor(i) { const h = 18 + Math.sin(i * 0.42) * 4; return `hsl(${h} 100% ${58 + Math.sin(i * 0.9) * 2}%)`; }
  function drawBox(b, y0, y1, top) {
    const { x0, x1, z0, z1 } = b;
    const shade = b.shade || 0;
    face([px(x0, z1, y1), px(x1, z1, y1), px(x1, z1, y0), px(x0, z1, y0)], `hsl(240 5% ${9 + shade}%)`);
    face([px(x1, z0, y1), px(x1, z1, y1), px(x1, z1, y0), px(x1, z0, y0)], `hsl(240 5% ${31 + shade}%)`);
    face([px(x0, z0, y1), px(x1, z0, y1), px(x1, z1, y1), px(x0, z1, y1)], top);
  }

  /* ---------- Layout ---------- */
  function resize() {
    const r = root.getBoundingClientRect(); const dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(1, Math.round(r.width)); HT = Math.max(1, Math.round(r.height));
    canvas.width = W * dpr; canvas.height = HT * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    u = Math.min((W * 0.37) / (SIZE * 2 * COS), (HT * 0.28) / (SIZE * 2 * SIN));
    draw();
  }

  /* ---------- Game flow ---------- */
  function reset() {
    blocks = [{ x0: -SIZE / 2, x1: SIZE / 2, z0: -SIZE / 2, z1: SIZE / 2, i: 0, shade: 0 }];
    debris = []; rings = []; sparks = []; floats = []; score = 0; streak = 0; camY = 0; camTarget = 0;
    spawn();
  }
  function spawn() {
    const top = blocks[blocks.length - 1], i = blocks.length, axis = i % 2 ? 'x' : 'z';
    const dir = (i >> 1) % 2 ? 1 : -1;
    mover = { x0: top.x0, x1: top.x1, z0: top.z0, z1: top.z1, i, axis, dir: -dir, off: dir * SWING, shade: i % 2 ? 2 : 0, flash: 0 };
    place(mover);
  }
  function place(m) {
    const top = blocks[blocks.length - 1];
    m.x0 = top.x0; m.x1 = top.x1; m.z0 = top.z0; m.z1 = top.z1;
    m[m.axis + '0'] += m.off; m[m.axis + '1'] += m.off;
  }
  const speed = () => (state === 'idle' ? 70 : Math.min(120 + score * 5.5, 300));

  function start() {
    reset(); state = 'playing';
    root.classList.add('is-playing'); root.classList.remove('is-over');
    startPanel.classList.remove('is-open'); overPanel.classList.remove('is-open'); cta.classList.remove('is-open');
    setScore(0); root.focus({ preventScroll: true }); tone(440, 0.09);
  }
  function setScore(v) {
    score = v; scoreEl.textContent = String(v);
    scoreEl.classList.remove('bump'); void scoreEl.offsetWidth; if (v) scoreEl.classList.add('bump');
  }
  function drop() {
    if (state !== 'playing' || !mover) return;
    const top = blocks[blocks.length - 1], a = mover.axis;
    const lo = Math.max(mover[a + '0'], top[a + '0']), hi = Math.min(mover[a + '1'], top[a + '1']);
    const y = blocks.length * H;
    if (hi - lo <= 1) {                       // Missed the stack completely
      debris.push({ ...mover, y, vy: 20, rot: 0, front: mover.off > 0, a: 1 });
      mover = null; return gameOver();
    }
    const size = top[a + '1'] - top[a + '0'];
    const placed = { x0: mover.x0, x1: mover.x1, z0: mover.z0, z1: mover.z1, i: mover.i, shade: mover.shade };
    if (Math.abs(mover.off) <= PERFECT) {     // Perfect drop: snap, bonus, regrow on a streak
      placed[a + '0'] = top[a + '0']; placed[a + '1'] = top[a + '1'];
      streak += 1;
      if (streak >= 3) { const g = Math.min(4, SIZE - size); placed[a + '0'] -= g / 2; placed[a + '1'] += g / 2; }
      setScore(score + 2);
      burst(placed, y);
      floats.push({ text: streak > 1 ? `PERFECT ×${streak}` : 'PERFECT', life: 1 });
      tone(520 + Math.min(streak, 12) * 62, 0.16, 'triangle', 0.07);
    } else {                                  // Trim the overhang into a falling piece
      streak = 0;
      const cut = { x0: mover.x0, x1: mover.x1, z0: mover.z0, z1: mover.z1, i: mover.i, shade: mover.shade, y, vy: 0, rot: 0, a: 1, front: mover.off > 0 };
      if (mover.off > 0) { cut[a + '0'] = hi; placed[a + '1'] = hi; } else { cut[a + '1'] = lo; placed[a + '0'] = lo; }
      placed[a + '0'] = Math.max(placed[a + '0'], lo); placed[a + '1'] = Math.min(placed[a + '1'], hi);
      debris.push(cut);
      setScore(score + 1);
      tone(240 + Math.min(score, 30) * 6, 0.08, 'square', 0.025);
    }
    blocks.push(placed);
    camTarget = Math.max(0, (blocks.length - 3) * H);
    spawn();
  }
  function burst(b, y) {
    rings.push({ b: { ...b }, y, t: 0 });
    if (reduceMotion) return;
    for (let i = 0; i < 12; i++) {
      const edge = Math.random();
      sparks.push({ x: b.x0 + (b.x1 - b.x0) * edge, z: i % 2 ? b.z1 : b.z0, y, vx: (Math.random() - 0.5) * 60, vz: (Math.random() - 0.5) * 60, vy: 40 + Math.random() * 70, life: 1 });
    }
  }
  function gameOver() {
    state = 'over'; overAt = performance.now();
    const record = score > best && score > 0;
    if (record) { best = score; try { localStorage.setItem('sb-stack-best', String(best)); } catch (e) { /* storage blocked */ } }
    bestEl.textContent = String(best);
    finalEl.textContent = String(score);
    subEl.textContent = record ? 'Your new record on this device.' : (best ? `Your best is ${best}. One more?` : 'Line them up. Perfect drops score double.');
    overPanel.classList.toggle('is-record', record);
    root.classList.remove('is-playing'); root.classList.add('is-over');
    overPanel.classList.add('is-open');
    tone(150, 0.3, 'sawtooth', 0.04);
  }
  function restartAllowed() { return performance.now() - overAt > 450; }

  /* ---------- Input ---------- */
  root.addEventListener('pointerdown', (e) => {
    if (e.button !== 0 || e.target.closest('.game-sound')) return;
    ignoreClick = state === 'playing';   // the click that follows a drop must not restart the game
    if (state === 'playing') { e.preventDefault(); drop(); }
  });
  root.addEventListener('click', (e) => {
    if (e.target.closest('.game-sound')) return;
    if (ignoreClick) { ignoreClick = false; return; }
    if (state === 'idle' || state === 'over') start();
  });
  window.addEventListener('keydown', (e) => {
    if (e.code !== 'Space' && e.code !== 'Enter') return;
    const a = document.activeElement, focused = a === root || root.contains(a);
    if (a && a.closest && a.closest('.game-sound')) return;
    if (!focused && !(state === 'playing' && inView)) return;
    if (!focused && a && /^(INPUT|TEXTAREA|SELECT|BUTTON|A)$/.test(a.tagName)) return;
    e.preventDefault();
    if (e.repeat) return;
    if (state === 'playing') drop(); else if (state === 'idle' || restartAllowed()) start();
  });
  function syncSound() { soundBtn.setAttribute('aria-pressed', String(muted)); soundBtn.setAttribute('aria-label', muted ? 'Turn sound on' : 'Turn sound off'); }
  soundBtn.addEventListener('click', () => { muted = !muted; syncSound(); try { localStorage.setItem('sb-stack-muted', muted ? '1' : '0'); } catch (e) { /* storage blocked */ } if (!muted) tone(660, 0.08); });

  /* ---------- Render ---------- */
  function draw() {
    if (!W) return;
    ctx.clearRect(0, 0, W, HT);
    const glow = ctx.createRadialGradient(W / 2, HT * 0.55, 10, W / 2, HT * 0.55, Math.max(W, HT) * 0.62);
    glow.addColorStop(0, '#fff3ec'); glow.addColorStop(1, '#ffffff');
    ctx.fillStyle = glow; ctx.fillRect(0, 0, W, HT);

    debris.filter((d) => !d.front).forEach(drawDebris);

    // Pillar under the first block runs off the bottom of the frame
    const base = blocks[0];
    drawBox(base, -900, 0, topColor(0));

    const firstVisible = Math.max(0, blocks.length - 40);
    for (let i = Math.max(1, firstVisible); i < blocks.length; i++) drawBox(blocks[i], (i - 1) * H, i * H, topColor(i));
    if (mover) drawMover();

    rings.forEach((r) => {
      const g = r.t * 26, b = r.b;
      ctx.globalAlpha = Math.max(0, 1 - r.t);
      ctx.beginPath();
      [[b.x0 - g, b.z0 - g], [b.x1 + g, b.z0 - g], [b.x1 + g, b.z1 + g], [b.x0 - g, b.z1 + g]].forEach((c, i) => { const p = px(c[0], c[1], r.y); i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); });
      ctx.closePath(); ctx.strokeStyle = '#ff6a2b'; ctx.lineWidth = 3; ctx.stroke(); ctx.globalAlpha = 1;
    });
    sparks.forEach((s) => { const p = px(s.x, s.z, s.y); ctx.globalAlpha = Math.max(0, s.life); ctx.fillStyle = '#ff6a2b'; ctx.fillRect(p[0] - 2.5, p[1] - 2.5, 5, 5); ctx.globalAlpha = 1; });

    debris.filter((d) => d.front).forEach(drawDebris);

    floats.forEach((f) => {
      ctx.globalAlpha = Math.min(1, f.life * 1.6);
      ctx.font = `700 ${Math.max(15, W * 0.03)}px "Chakra Petch", system-ui, sans-serif`;
      ctx.textAlign = 'center'; ctx.fillStyle = '#c7430f';
      ctx.fillText(f.text, W / 2, HT * 0.27 - (1 - f.life) * 22);
      ctx.globalAlpha = 1;
    });
  }
  function drawMover() { const y = blocks.length * H; drawBox(mover, y - H, y, topColor(mover.i)); }
  function drawDebris(d) { ctx.globalAlpha = d.a; drawBox(d, d.y - H, d.y, topColor(d.i)); ctx.globalAlpha = 1; }

  function tick(dt) {
    if (mover) {
      mover.off += mover.dir * speed() * dt;
      if (mover.off > SWING) { mover.off = SWING; mover.dir = -1; } else if (mover.off < -SWING) { mover.off = -SWING; mover.dir = 1; }
      place(mover);
    }
    camY += (camTarget - camY) * Math.min(1, dt * 7);
    debris.forEach((d) => { d.vy -= 520 * dt; d.y += d.vy * dt; d.a = Math.max(0, d.a - dt * 0.9); });
    debris = debris.filter((d) => d.a > 0.02);
    rings.forEach((r) => { r.t += dt * 2.2; }); rings = rings.filter((r) => r.t < 1);
    sparks.forEach((s) => { s.vy -= 200 * dt; s.x += s.vx * dt; s.z += s.vz * dt; s.y += s.vy * dt; s.life -= dt * 1.5; }); sparks = sparks.filter((s) => s.life > 0);
    floats.forEach((f) => { f.life -= dt * 1.1; }); floats = floats.filter((f) => f.life > 0);
  }
  function loop(t) {
    requestAnimationFrame(loop);
    const dt = Math.min((t - lastT) / 1000, 0.05); lastT = t;
    if (!inView || document.hidden) return;
    tick(reduceMotion && state === 'idle' ? 0 : dt);
    draw();
  }

  if ('IntersectionObserver' in window) new IntersectionObserver((en) => { inView = en[0].isIntersecting; }, { threshold: 0.1 }).observe(root);
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(root); else window.addEventListener('resize', resize);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);

  bestEl.textContent = String(best); syncSound();
  // Idle screen: a short tower with a block drifting across
  reset();
  for (let i = 0; i < 3; i++) { const t = blocks[blocks.length - 1]; blocks.push({ x0: t.x0, x1: t.x1, z0: t.z0, z1: t.z1, i: blocks.length, shade: blocks.length % 2 ? 2 : 0 }); }
  spawn();
  startPanel.classList.add('is-open'); cta.classList.add('is-open');
  resize();
  requestAnimationFrame((t) => { lastT = t; loop(t); });

  // Small hook for automated checks; has no effect on play
  root.gameState = () => ({ state, score, best, blocks: blocks.length, off: mover ? mover.off : null });
})();
