// Menu mobile, agrandissement des captures, apparition au défilement.
const burger = document.querySelector('.burger');
const menu = document.getElementById('menu');
burger.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  burger.setAttribute('aria-expanded', String(open));
});
menu.addEventListener('click', e => { if (e.target.tagName === 'A') { menu.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); } });

const box = document.querySelector('.lightbox');
document.querySelectorAll('.gallery button').forEach(b => b.addEventListener('click', () => {
  const img = b.querySelector('img');
  box.querySelector('img').src = b.dataset.full; box.querySelector('img').alt = img.alt;
  box.showModal();
}));
box.addEventListener('click', e => { if (e.target === box || e.target.tagName === 'BUTTON') box.close(); });

const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

// En-tête : ombre légère dès qu'on fait défiler.
const nav = document.querySelector('.nav');
const onScroll = () => nav.classList.toggle('scrolled', scrollY > 8);
addEventListener('scroll', onScroll, { passive: true }); onScroll();

if ('IntersectionObserver' in window) {
  // Apparition au défilement, en cascade entre éléments voisins.
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .12 });
  document.querySelectorAll('.card, .feature, .steps li, .checks li, .timeline li, .doc, .gallery figure, .engines li, .roles .grid4 div, .studio-why li, .studio-shot').forEach(el => {
    const sibs = [...el.parentElement.children].filter(x => x.tagName === el.tagName);
    el.style.setProperty('--d', (Math.max(0, sibs.indexOf(el)) % 6) * 0.09 + 's');
    el.classList.add('reveal'); io.observe(el);
  });
  // Animations déclenchées une fois visibles : schéma avant / après, étapes, frise.
  const once = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    e.target.classList.add(e.target.matches('.arch-panel') ? 'in' : 'play');
    if (e.target.matches('.arch-after') && !calm) packets(e.target.querySelector('svg'));
    once.unobserve(e.target);
  }), { threshold: .35 });
  document.querySelectorAll('.arch-panel, .steps, .timeline').forEach(el => once.observe(el));
}

// Requêtes qui circulent : des postes vers SQLVault Gateway, puis vers les bases (vertes : validées) ;
// l'une d'elles, rouge, est arrêtée par la passerelle (requête dangereuse bloquée).
function packets(svg) {
  const NS = 'http://www.w3.org/2000/svg', t0 = svg.getCurrentTime();
  const dot = (d, color, begin, dur, blocked) => {
    const c = document.createElementNS(NS, 'circle');
    c.setAttribute('r', blocked ? 4.5 : 3.6); c.setAttribute('fill', color); c.setAttribute('opacity', 0);
    const m = document.createElementNS(NS, 'animateMotion');
    Object.entries({ path: d, dur: dur + 's', begin: (t0 + begin) + 's', repeatCount: 'indefinite', calcMode: 'spline', keyTimes: '0;1', keySplines: '.45 0 .55 1' }).forEach(([k, v]) => m.setAttribute(k, v));
    const o = document.createElementNS(NS, 'animate');
    Object.entries({ attributeName: 'opacity', values: blocked ? '0;1;1;0' : '0;1;1;0', keyTimes: blocked ? '0;.1;.8;1' : '0;.08;.9;1', dur: dur + 's', begin: (t0 + begin) + 's', repeatCount: 'indefinite' }).forEach(([k, v]) => o.setAttribute(k, v));
    c.append(m, o); svg.append(c);
  };
  const ins = [...svg.querySelectorAll('.lines-in path')].map(p => p.getAttribute('d'));
  const outs = [...svg.querySelectorAll('.lines-out path')].map(p => p.getAttribute('d'));
  ins.forEach((d, i) => dot(d, i === 2 ? '#e8542f' : '#2f7dfa', 1.8 + i * 0.55, 2.4, i === 2));
  outs.forEach((d, i) => dot(d, '#1a8a4f', 3.4 + i * 0.6, 2.1));
}

// Copier une commande d'installation.
document.querySelectorAll('.cmd .copy').forEach(b => b.addEventListener('click', async () => {
  const code = b.parentElement.querySelector('code').textContent, label = b.textContent;
  try { await navigator.clipboard.writeText(code); b.textContent = document.documentElement.lang === 'en' ? 'Copied ✓' : 'Copié ✓'; }
  catch { const r = document.createRange(); r.selectNodeContents(b.parentElement.querySelector('code')); getSelection().removeAllRanges(); getSelection().addRange(r); }
  setTimeout(() => { b.textContent = label; }, 1800);
}));
