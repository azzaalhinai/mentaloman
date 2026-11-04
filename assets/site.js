(() => {
const root = document.documentElement, $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
const save = (k, v) => { try { localStorage.setItem(k, v); } catch {} };

$('#langBtn').onclick = () => {
  const lang = root.lang === 'ar' ? 'en' : 'ar';
  root.lang = lang; root.dir = lang === 'ar' ? 'rtl' : 'ltr'; save('lang', lang);
  document.dispatchEvent(new Event('langchange'));
};
$('#themeBtn').onclick = () => { const t = root.dataset.theme === 'dark' ? 'light' : 'dark'; root.dataset.theme = t; save('theme', t); };
const burger = $('#burger'), nav = $('.nav');
burger.onclick = () => burger.setAttribute('aria-expanded', nav.classList.toggle('open'));
nav.addEventListener('click', e => { if (e.target.closest('a')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', false); } });
const top = $('.top'), stick = () => top.classList.toggle('stuck', scrollY > 20);
addEventListener('scroll', stick, { passive: true }); stick();

const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8%' });
$$('.rv').forEach(el => io.observe(el));

$$('.chips').forEach(group => group.addEventListener('click', e => {
  const b = e.target.closest('.chip'); if (!b) return;
  $$('.chip', group).forEach(c => c.setAttribute('aria-pressed', c === b));
  $$(group.dataset.for).forEach(el => { el.style.display = b.dataset.f === 'all' || el.dataset.c === b.dataset.f ? '' : 'none'; });
}));

const dlg = $('dialog');
if (dlg) {
  $$('.chart').forEach(b => b.onclick = () => { const i = $('img', b); $('img', dlg).src = i.src; $('img', dlg).alt = i.alt; dlg.showModal(); });
  $('button', dlg).onclick = () => dlg.close();
  dlg.onclick = e => { if (e.target === dlg) dlg.close(); };
}

const form = $('#contactForm');
if (form) form.onsubmit = e => {
  e.preventDefault();
  const f = new FormData(form);
  location.href = `mailto:${form.dataset.to}?subject=${encodeURIComponent(f.get('subject'))}&body=${encodeURIComponent(`${f.get('message')}\n\n${f.get('name')} <${f.get('email')}>`)}`;
};

const stage = $('.stage');
if (!stage) return;
const cards = $$('.rc', stage), PITCH = 196, LOOP = PITCH * cards.length;
let offset = 0, vel = 0, dragging = false, moved = 0, lastX = 0, lastMove = 0;
const wrap = t => ((t + LOOP / 2) % LOOP + LOOP) % LOOP - LOOP / 2;

// rounded polygon: each corner is cut back by r along its two edges
function quad(p, r) {
  let d = '';
  p.forEach((c, i) => {
    const to = n => { const l = Math.hypot(n[0] - c[0], n[1] - c[1]); return [c[0] + (n[0] - c[0]) * r / l, c[1] + (n[1] - c[1]) * r / l]; };
    const s = to(p[(i + 3) % 4]), e = to(p[(i + 1) % 4]);
    d += `${i ? 'L' : 'M'}${s[0].toFixed(1)} ${s[1].toFixed(1)}Q${c[0].toFixed(1)} ${c[1].toFixed(1)} ${e[0].toFixed(1)} ${e[1].toFixed(1)}`;
  });
  return `path("${d}Z")`;
}

function layout() {
  const phone = innerWidth <= 820, W = stage.clientWidth, H = stage.clientHeight;
  const s = phone ? W / 640 : W / 1440, R = phone ? 380 : 706, cy = phone ? H / 2 : 687 * s;
  stage.style.setProperty('--cu', s + 'px');
  cards.forEach((el, i) => {
    const t = wrap(i * PITCH - offset), x = t * (1 + 0.083 * (t / R) ** 2);
    const d = Math.min(Math.abs(x) / R, 1.25), w = 170 + 48 * d * d;
    const edge = e => 280 + 92 * Math.min(Math.abs(e) / R, 1.25) ** 2.6;
    const hl = edge(x - w / 2), hr = edge(x + w / 2), hm = Math.max(hl, hr);
    const bw = w * s, bh = hm * s, ol = (hm - hl) / 2 * s, or = (hm - hr) / 2 * s;
    el.style.width = bw + 'px'; el.style.height = bh + 'px';
    el.style.transform = `translate(${W / 2 + (x - w / 2) * s}px,${cy + (-12 * d * d - hm / 2) * s}px)`;
    el.style.clipPath = quad([[0, ol], [bw, or], [bw, bh - or], [0, bh - ol]], 15 * s);
  });
}

const clock = root.animate([], { duration: 1e9 });
let prev = clock.currentTime || 0;
(function frame() {
  const now = clock.currentTime || 0, dt = Math.min((now - prev) / 1000, .1); prev = now;
  if (!dragging) {
    offset += ((calm ? 0 : root.dir === 'rtl' ? -50 : 50) + vel) * dt;
    vel *= Math.pow(.05, dt);
  }
  layout();
  requestAnimationFrame(frame);
})();

stage.addEventListener('pointerdown', e => { dragging = true; moved = 0; vel = 0; lastX = e.clientX; lastMove = performance.now(); });
addEventListener('pointermove', e => {
  if (!dragging) return;
  const s = stage.clientWidth / (innerWidth <= 820 ? 640 : 1440), dx = (e.clientX - lastX) / s, t = performance.now();
  moved += Math.abs(e.clientX - lastX); if (moved > 6) stage.classList.add('drag');
  offset -= dx; vel = -dx / Math.max((t - lastMove) / 1000, .008); lastX = e.clientX; lastMove = t;
});
const end = () => { if (performance.now() - lastMove > 90) vel = 0; dragging = false; stage.classList.remove('drag'); };
addEventListener('pointerup', end); addEventListener('pointercancel', end);
stage.addEventListener('click', e => { if (moved > 6) e.preventDefault(); }, true);
stage.addEventListener('dragstart', e => e.preventDefault());
cards.forEach((el, i) => el.addEventListener('focus', () => { offset = i * PITCH; vel = 0; }));

if (!calm) {
  const seq = (sel, from, delay, dur = 800) => $$(sel).forEach((el, i) => el.animate([from, { opacity: 1, filter: 'blur(0)', transform: getComputedStyle(el).transform }], { duration: dur, delay: delay + i * 140, easing: 'cubic-bezier(.2,.8,.2,1)', fill: 'backwards' }));
  seq('.top', { opacity: 0, transform: 'translateY(-20px)' }, 0);
  seq('.badge', { opacity: 0 }, 150);
  seq('.hero h1 .l', { opacity: 0, transform: 'translateY(30px)', filter: 'blur(10px)' }, 280);
  seq('.sub', { opacity: 0, transform: 'translateY(16px)' }, 640);
  seq('.stage', { opacity: 0, transform: 'translateY(60px)' }, 760, 1100);
  seq('.ring', { opacity: 0, transform: 'scale(.8)' }, 1100);
  seq('.hand', { opacity: 0 }, 1400);
  $$('.doodle path').forEach((p, i) => { const l = p.getTotalLength(); p.style.strokeDasharray = l; p.animate([{ strokeDashoffset: l }, { strokeDashoffset: 0 }], { duration: 900, delay: 1300 + i * 240, easing: 'ease-out', fill: 'backwards' }); });
  // the hero must never stay hidden if the animation timeline is stalled
  setTimeout(() => document.getAnimations().forEach(x => { if (x !== clock && x.effect.getTiming().fill === 'backwards') x.finish(); }), 3500);
}
})();
