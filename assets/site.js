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

if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .12 });
  document.querySelectorAll('.card, .feature, .steps li, .checks li, .timeline li, .doc, .gallery figure').forEach(el => { el.classList.add('reveal'); io.observe(el); });
}

// Copier une commande d'installation.
document.querySelectorAll('.cmd .copy').forEach(b => b.addEventListener('click', async () => {
  const code = b.parentElement.querySelector('code').textContent, label = b.textContent;
  try { await navigator.clipboard.writeText(code); b.textContent = document.documentElement.lang === 'en' ? 'Copied ✓' : 'Copié ✓'; }
  catch { const r = document.createRange(); r.selectNodeContents(b.parentElement.querySelector('code')); getSelection().removeAllRanges(); getSelection().addRange(r); }
  setTimeout(() => { b.textContent = label; }, 1800);
}));
