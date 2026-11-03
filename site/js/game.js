/* Stone Stack — a 20-second mini-game. Tap / click / Space to drop the moving stone on the stack. */
(function () {
  'use strict';
  const frame = document.getElementById('stack-game');
  if (!frame) return;
  const canvas = frame.querySelector('canvas');
  const ctx = canvas.getContext('2d');
  const overlay = frame.querySelector('.game-overlay');
  const oTitle = overlay.querySelector('h3'), oText = overlay.querySelector('p'), oBtn = overlay.querySelector('button');
  const hudScore = frame.querySelector('[data-score]'), hudBest = frame.querySelector('[data-best]');
  const outScore = document.querySelector('[data-score-out]'), outBest = document.querySelector('[data-best-out]');
  const BLOCK_H = 26, BASE = 44;
  let W = 0, H = 0, state = 'idle', blocks = [], moving = null, debris = [], score = 0, best = 0;
  let cameraY = 0, targetCam = 0, dir = 1, speed = 0, lastT = 0, shake = 0, flash = 0, inView = true, perfectStreak = 0;
  try { best = parseInt(localStorage.getItem('sb-stack-best') || '0', 10) || 0; } catch (e) { best = 0; }

  function resize() {
    const r = frame.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.round(r.width); H = Math.round(r.height);
    canvas.width = W * dpr; canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (state !== 'playing') { reset(); }
    draw();
  }
  function reset() { blocks = [{ x: W * 0.25, w: W * 0.5, hue: 0 }]; cameraY = 0; targetCam = 0; score = 0; debris = []; perfectStreak = 0; spawn(); }
  function spawn() {
    const top = blocks[blocks.length - 1];
    dir = blocks.length % 2 ? 1 : -1;
    moving = { x: dir === 1 ? -top.w * 0.6 : W - top.w * 0.4, w: top.w, hue: blocks.length };
    speed = 170 + Math.min(score, 40) * 8.5;
  }
  const blockY = (i) => H - BASE - (i + 1) * BLOCK_H + cameraY;
  function drop() {
    if (state !== 'playing' || !moving) return;
    const top = blocks[blocks.length - 1];
    const left = Math.max(moving.x, top.x), right = Math.min(moving.x + moving.w, top.x + top.w);
    const overlap = right - left;
    const y = blockY(blocks.length);
    if (overlap <= 2) { debris.push({ x: moving.x, w: moving.w, y, vy: -60, vx: dir * 70, rot: 0, hue: moving.hue }); moving = null; gameOver(); return; }
    if (Math.abs(moving.x - top.x) <= 4) {
      blocks.push({ x: top.x, w: top.w, hue: moving.hue }); perfectStreak++; score += 2; flash = 1;
    } else {
      if (moving.x < top.x) debris.push({ x: moving.x, w: top.x - moving.x, y, vy: -40, vx: -90, rot: 0, hue: moving.hue });
      else debris.push({ x: top.x + top.w, w: (moving.x + moving.w) - (top.x + top.w), y, vy: -40, vx: 90, rot: 0, hue: moving.hue });
      blocks.push({ x: left, w: overlap, hue: moving.hue }); perfectStreak = 0; score += 1;
    }
    updateHud();
    const topY = blockY(blocks.length - 1);
    if (topY < H * 0.42) targetCam += (H * 0.42 - topY);
    spawn();
  }
  function gameOver() {
    state = 'over'; shake = 1;
    if (score > best) { best = score; try { localStorage.setItem('sb-stack-best', String(best)); } catch (e) {} }
    updateHud();
    oTitle.textContent = score >= 15 ? 'Solid build!' : 'Game over';
    oText.textContent = `You stacked ${score} ${score === 1 ? 'point' : 'points'}. Perfect drops score double.`;
    oBtn.textContent = 'Play again';
    overlay.classList.remove('is-hidden');
  }
  function start() { reset(); state = 'playing'; overlay.classList.add('is-hidden'); updateHud(); lastT = performance.now(); }
  function updateHud() {
    hudScore.textContent = String(score); hudBest.textContent = String(best);
    if (outScore) outScore.textContent = String(score);
    if (outBest) outBest.textContent = String(best);
  }
  function action(e) { if (e) e.preventDefault(); if (state === 'playing') drop(); else start(); }
  frame.addEventListener('pointerdown', (e) => { if (e.button === 0) action(e); });
  frame.addEventListener('keydown', (e) => { if (e.code === 'Space' || e.code === 'Enter') action(e); });
  window.addEventListener('keydown', (e) => {
    if (e.code !== 'Space' || !inView || state !== 'playing') return;
    const a = document.activeElement; if (a && /INPUT|TEXTAREA|SELECT|BUTTON/.test(a.tagName)) return;
    action(e);
  });

  function stoneColor(hue, l) { const h = 212 + (hue * 9) % 48; return `hsl(${h} 18% ${l}%)`; }
  function roundRect(x, y, w, h, r) { r = Math.min(r, h / 2, Math.max(w, 0.01) / 2); ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function drawBlock(x, y, w, isMoving, hue) {
    if (w <= 0) return;
    const g = ctx.createLinearGradient(0, y, 0, y + BLOCK_H);
    if (isMoving) { g.addColorStop(0, '#ffa072'); g.addColorStop(1, '#f25a18'); }
    else { g.addColorStop(0, stoneColor(hue, 32)); g.addColorStop(1, stoneColor(hue, 18)); }
    ctx.shadowColor = 'rgba(0,0,0,0.45)'; ctx.shadowBlur = 10; ctx.shadowOffsetY = 4;
    roundRect(x, y, w, BLOCK_H - 3, 7); ctx.fillStyle = g; ctx.fill();
    ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0;
    ctx.fillStyle = isMoving ? 'rgba(255,255,255,0.4)' : 'rgba(255,255,255,0.1)';
    roundRect(x + 5, y + 3, Math.max(0, w - 10), 3, 1.5); ctx.fill();
  }
  function draw() {
    ctx.clearRect(0, 0, W, H);
    ctx.save();
    if (shake > 0) ctx.translate((Math.random() - 0.5) * shake * 10, (Math.random() - 0.5) * shake * 10);
    // guide line of the top stone
    const top = blocks[blocks.length - 1];
    if (top && state === 'playing') { ctx.fillStyle = 'rgba(255,106,43,0.08)'; ctx.fillRect(top.x, 0, top.w, H); }
    // plinth
    ctx.fillStyle = 'rgba(255,255,255,0.05)'; roundRect(W * 0.12, H - BASE + cameraY, W * 0.76, BASE + 40, 12); ctx.fill();
    blocks.forEach((b, i) => drawBlock(b.x, blockY(i), b.w, false, b.hue));
    debris.forEach((d) => { ctx.save(); ctx.translate(d.x + d.w / 2, d.y + BLOCK_H / 2); ctx.rotate(d.rot); ctx.globalAlpha = 0.85; drawBlock(-d.w / 2, -BLOCK_H / 2, d.w, false, d.hue); ctx.restore(); });
    if (moving && state === 'playing') drawBlock(moving.x, blockY(blocks.length), moving.w, true, moving.hue);
    if (flash > 0) { ctx.fillStyle = `rgba(255,106,43,${flash * 0.22})`; ctx.fillRect(0, 0, W, H); }
    ctx.restore();
  }
  function loop(t) {
    requestAnimationFrame(loop);
    if (!inView || document.hidden) { lastT = t; return; }
    const dt = Math.min((t - lastT) / 1000, 0.05); lastT = t;
    if (state === 'playing' && moving) {
      moving.x += dir * speed * dt;
      const minX = -moving.w * 0.35, maxX = W - moving.w * 0.65;
      if (moving.x > maxX) { moving.x = maxX; dir = -1; } else if (moving.x < minX) { moving.x = minX; dir = 1; }
    }
    cameraY += (targetCam - cameraY) * Math.min(1, dt * 6);
    debris.forEach((d) => { d.vy += 1500 * dt; d.y += d.vy * dt; d.x += d.vx * dt; d.rot += (d.vx > 0 ? 1 : -1) * 2.2 * dt; });
    debris = debris.filter((d) => d.y < H + 120);
    shake = Math.max(0, shake - dt * 3); flash = Math.max(0, flash - dt * 2.5);
    if (state !== 'idle' || debris.length || shake > 0 || flash > 0) draw();
  }
  if ('IntersectionObserver' in window) new IntersectionObserver((en) => { inView = en[0].isIntersecting; }, { threshold: 0.2 }).observe(frame);
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(frame); else window.addEventListener('resize', resize);
  oBtn.addEventListener('click', (e) => { e.stopPropagation(); action(e); });
  resize(); updateHud(); requestAnimationFrame((t) => { lastT = t; loop(t); });
})();
