/* StoneBuild Games — site behaviour v2 (GSAP enhances when present) */
(function () {
  'use strict';
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isDesktop = window.matchMedia('(min-width: 1024px)').matches;

  /* ---- Header: pill on scroll ---- */
  const header = $('.site-header');
  let lastState = null;
  const onScroll = () => {
    const s = window.scrollY > 24;
    if (s !== lastState && header) { header.classList.toggle('is-scrolled', s); lastState = s; }
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- Mobile nav ---- */
  const toggle = $('.nav-toggle');
  const nav = $('#nav');
  const closeNav = () => { if (!nav) return; nav.classList.remove('is-open'); toggle?.setAttribute('aria-expanded', 'false'); };
  if (toggle && nav) {
    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', (e) => { if (!nav.contains(e.target) && !toggle.contains(e.target)) closeNav(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeNav(); });
  }

  /* ---- Current page ---- */
  const path = location.pathname.replace(/index\.html$/, '');
  $$('.nav a').forEach((a) => { if (a.getAttribute('href') === path) a.setAttribute('aria-current', 'page'); });

  /* ---- Page transition fallback (browsers without cross-document view transitions) ---- */
  if (!('startViewTransition' in document) && !reduceMotion) {
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href]');
      if (!a || a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.defaultPrevented) return;
      const url = new URL(a.href, location.href);
      if (url.origin !== location.origin || url.pathname === location.pathname || a.hasAttribute('download') || a.protocol === 'mailto:') return;
      e.preventDefault();
      document.documentElement.classList.add('is-leaving');
      setTimeout(() => { location.href = url.href; }, 200);
    });
    window.addEventListener('pageshow', () => document.documentElement.classList.remove('is-leaving'));
  }

  /* ---- Section dots ---- */
  const dots = $$('.dots a');
  const sections = $$('main > section.screen');
  if (dots.length && sections.length && 'IntersectionObserver' in window) {
    const byId = new Map(dots.map((d) => [d.getAttribute('href').slice(1), d]));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        dots.forEach((d) => d.classList.remove('is-active'));
        (byId.get(en.target.id || 'top') || dots[0]).classList.add('is-active');
      });
    }, { threshold: 0.55 });
    sections.forEach((s) => io.observe(s));
  }

  /* ---- Card glow + tilt ---- */
  $$('.card').forEach((card) => {
    const tilt = card.classList.contains('tilt') && isDesktop && !reduceMotion;
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
      card.style.setProperty('--mx', (px * 100) + '%');
      card.style.setProperty('--my', (py * 100) + '%');
      if (tilt) { card.style.setProperty('--ry', ((px - 0.5) * 6).toFixed(2) + 'deg'); card.style.setProperty('--rx', ((0.5 - py) * 6).toFixed(2) + 'deg'); }
    });
    card.addEventListener('pointerleave', () => { card.style.setProperty('--rx', '0deg'); card.style.setProperty('--ry', '0deg'); });
  });


  /* ---- Hero visual: pointer parallax ---- */
  const hv = $('.hero-visual');
  if (hv && isDesktop && !reduceMotion) {
    window.addEventListener('pointermove', (e) => {
      hv.style.setProperty('--px', ((e.clientX / window.innerWidth) - 0.5).toFixed(3));
      hv.style.setProperty('--py', ((e.clientY / window.innerHeight) - 0.5).toFixed(3));
    }, { passive: true });
  }

  /* ---- Split hero headline into words ---- */
  const h1 = $('.hero h1');
  if (h1) {
    $$('.line', h1).forEach((line) => {
      const words = line.textContent.trim().split(/\s+/);
      line.innerHTML = words.map((w) => `<span class="word">${w}</span>`).join(' ');
    });
  }

  /* ---- Reveal animations ---- */
  const reveals = $$('.reveal');
  const heroText = $$('.hero-text');
  const showAll = () => { reveals.forEach((el) => el.classList.add('is-in')); heroText.forEach((el) => el.classList.add('is-in')); };
  const lateStart = document.documentElement.classList.contains('reveal-ready');

  function revealWithGsap() {
    gsap.registerPlugin(ScrollTrigger);
    const blur = isDesktop ? { filter: 'blur(8px)' } : {};
    const blurOff = isDesktop ? { filter: 'blur(0px)' } : {};
    const done = (items) => () => { items.forEach((i) => i.classList.add('is-in')); gsap.set(items, { clearProps: 'transform,opacity,filter,translate,rotate,scale' }); };

    // Hero: words then the rest
    const hero = $('.hero');
    if (hero) {
      const words = $$('.word', hero);
      const rest = $$('.reveal', hero);
      const h1 = $('.hero h1'), lead = $('.hero .lead');
      gsap.set(rest, { opacity: 0, y: 26 });
      if (words.length) {
        // Text is never fully transparent, so it still counts as the LCP element
        gsap.set(h1, { opacity: 1, y: 0 });
        gsap.set(words, { opacity: 0.15, y: 46, rotateX: -40, transformOrigin: '50% 100%' });
        gsap.to(words, { opacity: 1, y: 0, rotateX: 0, duration: 0.8, stagger: 0.05, ease: 'power4.out', delay: 0.05,
          onComplete: () => { h1.classList.add('is-in'); h1.style.cssText = ''; } });
      }
      if (lead) gsap.fromTo(lead, { opacity: 0.35, y: 18 }, { opacity: 1, y: 0, duration: 0.6, ease: 'power3.out', delay: 0.2,
        onComplete: () => { lead.classList.add('is-in'); lead.style.cssText = ''; } });
      gsap.to(rest, { opacity: 1, y: 0, duration: 0.6, stagger: 0.06, ease: 'power3.out', delay: 0.25, onComplete: done(rest) });
      // Parallax on scroll
      if (isDesktop) {
        gsap.to('.hero .container', { y: 140, opacity: 0.15, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
        gsap.to('.hero-canvas', { scale: 1.12, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
      }
    }
    // Full-screen sections: stagger when entering
    sections.filter((s) => !s.classList.contains('hero')).forEach((section) => {
      const items = $$('.reveal', section);
      if (!items.length) return;
      gsap.set(items, { opacity: 0, y: 28, ...blur });
      ScrollTrigger.create({ trigger: section, start: 'top 72%', once: true,
        onEnter: () => gsap.to(items, { opacity: 1, y: 0, ...blurOff, duration: 0.85, stagger: 0.07, ease: 'power3.out', onComplete: done(items) }) });
    });
    // Inner pages: group by nearest section
    const loose = reveals.filter((el) => !el.closest('section.screen'));
    const groups = new Map();
    loose.forEach((el) => { const key = el.closest('section') || document.body; if (!groups.has(key)) groups.set(key, []); groups.get(key).push(el); });
    groups.forEach((items, key) => {
      gsap.set(items, { opacity: 0, y: 24, ...blur });
      ScrollTrigger.create({ trigger: key, start: 'top 85%', once: true,
        onEnter: () => gsap.to(items, { opacity: 1, y: 0, ...blurOff, duration: 0.8, stagger: 0.06, ease: 'power3.out', onComplete: done(items) }) });
    });
    // Magnetic primary buttons
    if (isDesktop) $$('.btn-primary').forEach((btn) => {
      btn.addEventListener('pointermove', (e) => { const r = btn.getBoundingClientRect(); gsap.to(btn, { x: (e.clientX - r.left - r.width / 2) * 0.16, y: (e.clientY - r.top - r.height / 2) * 0.26, duration: 0.3 }); });
      btn.addEventListener('pointerleave', () => gsap.to(btn, { x: 0, y: 0, duration: 0.5, ease: 'elastic.out(1, 0.4)' }));
    });
  }
  function revealWithObserver() {
    if (!('IntersectionObserver' in window)) return showAll();
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en, i) => { if (en.isIntersecting) { en.target.style.transitionDelay = (i % 8) * 60 + 'ms'; en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { threshold: 0.15 });
    reveals.forEach((el) => io.observe(el));
  }
  if (reduceMotion || lateStart) showAll();
  else if (window.gsap && window.ScrollTrigger) revealWithGsap();
  else revealWithObserver();

  /* ---- Contact form -> mailto ---- */
  const form = $('#contact-form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const data = new FormData(form);
      const get = (k) => (data.get(k) || '').toString().trim();
      const name = get('name'), email = get('email'), type = get('type'), budget = get('budget'), message = get('message');
      const note = $('#form-note');
      if (!name || !email || !message) { if (note) note.textContent = 'Please fill in your name, email and a short description of the game.'; form.querySelector(':invalid')?.focus(); return; }
      const subject = `Project inquiry: ${type} — ${name}`;
      const body = `Name: ${name}\nEmail: ${email}\nProject type: ${type}\nBudget: ${budget}\n\n${message}`;
      location.href = `mailto:support@stonebuildgames.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      if (note) note.textContent = 'Your email app should open now. If it did not, write to support@stonebuildgames.com.';
    });
  }

  /* ---- Legal TOC ---- */
  const tocLinks = $$('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const targets = tocLinks.map((a) => $(a.getAttribute('href'))).filter(Boolean);
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) tocLinks.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id)); });
    }, { rootMargin: '-20% 0px -70% 0px' });
    targets.forEach((t) => io.observe(t));
  }

  const y = $('#year');
  if (y) y.textContent = String(new Date().getFullYear());
})();
