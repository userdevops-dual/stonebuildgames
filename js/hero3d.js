/* StoneBuild Games — hero scene. Loads Three.js lazily and only on capable devices;
   phones and low-power devices get a lightweight CSS fallback. */
const mount = document.getElementById('hero-canvas');
if (mount) {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small = window.matchMedia('(max-width: 900px)').matches;
  const saveData = navigator.connection && navigator.connection.saveData;
  const lowPower = (navigator.hardwareConcurrency || 8) <= 4 || (navigator.deviceMemory && navigator.deviceMemory <= 4);
  if (reduceMotion || small || saveData || lowPower) {
    mount.classList.add('is-fallback');
  } else {
    const start = () => import('/vendor/three.module.min.js').then((THREE) => init(THREE)).catch(() => mount.classList.add('is-fallback'));
    const idle = () => setTimeout(() => ('requestIdleCallback' in window ? requestIdleCallback(start, { timeout: 1500 }) : start()), 900); // after the intro animation
    if (document.readyState === 'complete') idle(); else window.addEventListener('load', idle, { once: true });
  }
}

function init(THREE) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
  renderer.setClearColor(0x000000, 0);
  mount.appendChild(renderer.domElement);
  renderer.domElement.style.opacity = '0';
  renderer.domElement.style.transition = 'opacity 1.2s ease';

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0xffffff, 0.022);
  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
  camera.position.set(0, 0, 14);

  scene.add(new THREE.AmbientLight(0xffffff, 2.1));
  const ember = new THREE.PointLight(0xff6a2b, 14, 40, 1.6); ember.position.set(8, 5, 6); scene.add(ember);
  const steel = new THREE.PointLight(0xffffff, 8, 40, 1.6); steel.position.set(-9, -4, 4); scene.add(steel);
  const key = new THREE.DirectionalLight(0xffffff, 0.6); key.position.set(-3, 6, 8); scene.add(key);

  const group = new THREE.Group(); scene.add(group);
  const geos = [new THREE.IcosahedronGeometry(1, 0), new THREE.DodecahedronGeometry(1, 0), new THREE.OctahedronGeometry(1, 0), new THREE.TetrahedronGeometry(1, 0)];
  const solid = new THREE.MeshStandardMaterial({ color: 0xe2e2e6, roughness: 0.8, metalness: 0.05, flatShading: true });
  const solidLight = new THREE.MeshStandardMaterial({ color: 0xeeeef0, roughness: 0.85, metalness: 0.02, flatShading: true });
  const wire = new THREE.MeshBasicMaterial({ color: 0xff6a2b, wireframe: true, transparent: true, opacity: 0.6 });
  const wireSteel = new THREE.MeshBasicMaterial({ color: 0x52525b, wireframe: true, transparent: true, opacity: 0.3 });
  const rand = (a, b) => a + Math.random() * (b - a);
  const stones = [];
  for (let i = 0; i < 12; i++) {
    const isWire = i % 4 === 3;
    const mesh = new THREE.Mesh(geos[i % geos.length], isWire ? (i % 8 === 3 ? wire : wireSteel) : (i % 2 ? solid : solidLight));
    mesh.scale.setScalar(rand(0.28, 0.85) * (isWire ? 1.3 : 1));
    // Keep clear of the headline: most stones sit on the right, the rest in the top and bottom bands
    const right = i % 4 !== 0;
    mesh.position.set(right ? rand(9.5, 13) : rand(-10, 8), right ? rand(-5, 5) : -rand(5.8, 6.8), rand(-8, 0)); // edges only, clear of text and rings
    mesh.rotation.set(rand(0, Math.PI), rand(0, Math.PI), rand(0, Math.PI));
    mesh.userData = { rx: rand(-0.25, 0.25), ry: rand(-0.3, 0.3), fy: rand(0.2, 0.6), fa: rand(0.15, 0.45), ph: rand(0, Math.PI * 2), y0: mesh.position.y };
    group.add(mesh); stones.push(mesh);
  }
  const pCount = 420, pos = new Float32Array(pCount * 3);
  for (let i = 0; i < pCount; i++) { pos[i * 3] = rand(-16, 16); pos[i * 3 + 1] = rand(-9, 9); pos[i * 3 + 2] = rand(-12, 4); }
  const pGeo = new THREE.BufferGeometry(); pGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const dust = new THREE.Points(pGeo, new THREE.PointsMaterial({ color: 0xff6a2b, size: 0.04, transparent: true, opacity: 0.45 }));
  scene.add(dust);

  const target = { x: 0, y: 0 }, cur = { x: 0, y: 0 };
  window.addEventListener('pointermove', (e) => { target.x = (e.clientX / window.innerWidth - 0.5) * 2; target.y = (e.clientY / window.innerHeight - 0.5) * 2; }, { passive: true });
  function resize() { const w = mount.clientWidth || window.innerWidth, h = mount.clientHeight || window.innerHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
  resize(); window.addEventListener('resize', resize);

  const clock = new THREE.Clock();
  let running = true, visible = true;
  if ('IntersectionObserver' in window) new IntersectionObserver((en) => { visible = en[0].isIntersecting; }).observe(mount);
  document.addEventListener('visibilitychange', () => { running = !document.hidden; });

  function frame() {
    requestAnimationFrame(frame);
    if (!running || !visible) return;
    const t = clock.getElapsedTime();
    cur.x += (target.x - cur.x) * 0.04; cur.y += (target.y - cur.y) * 0.04;
    camera.position.x = cur.x * 0.9; camera.position.y = -cur.y * 0.6; camera.lookAt(0, 0, 0);
    for (const m of stones) { const u = m.userData; m.rotation.x += u.rx * 0.016; m.rotation.y += u.ry * 0.016; m.position.y = u.y0 + Math.sin(t * u.fy + u.ph) * u.fa; }
    group.rotation.y = Math.sin(t * 0.05) * 0.08;
    dust.rotation.y = t * 0.012; dust.position.y = Math.sin(t * 0.1) * 0.3;
    ember.intensity = 13 + Math.sin(t * 1.7) * 2;
    renderer.render(scene, camera);
  }
  frame();
  requestAnimationFrame(() => { renderer.domElement.style.opacity = '1'; });
}
