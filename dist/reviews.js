import reviewsData from './reviews-data.js';

const COPY = {
  fr: {
    empty: 'Découvrez les avis des patients sur la fiche Google Maps du cabinet.',
    selected: date => `Sélection relevée le ${date} · Mise à jour manuelle`, stars: n => `${n} étoiles sur 5`,
    read: 'Lire la suite', less: 'Réduire', source: 'Voir cet avis sur Google Maps',
    original: 'Voir le texte original', translated: 'Afficher la traduction', translation: 'Traduction du site — extrait original disponible',
    position: (i, n) => `Avis ${i} sur ${n}`, demo: 'Prévisualisation : avis fictifs, non publiés',
  },
  ar: {
    empty: 'اطّلعوا على آراء المرضى على صفحة العيادة في Google Maps.',
    selected: date => `اختيار جُمِع بتاريخ ${date} · يُحدّث يدوياً`, stars: n => `${n} نجوم من 5`,
    read: 'قراءة المزيد', less: 'عرض أقل', source: 'عرض هذا الرأي على Google Maps',
    original: 'عرض النص الأصلي', translated: 'عرض الترجمة', translation: 'ترجمة الموقع — المقتطف الأصلي متاح',
    position: (i, n) => `الرأي ${i} من ${n}`, demo: 'معاينة: آراء افتراضية غير منشورة',
  },
};

function safeURL(value) {
  try {
    const url = new URL(value);
    const hosts = ['google.com', 'g.co', 'maps.app.goo.gl'];
    return url.protocol === 'https:' && hosts.some(h => url.hostname === h || url.hostname.endsWith(`.${h}`)) ? url.href : '';
  } catch { return ''; }
}

export function mountReviews(root, {data = reviewsData} = {}) {
  const doc = root.ownerDocument;
  const ar = doc.documentElement.lang === 'ar';
  const t = COPY[ar ? 'ar' : 'fr'];
  const locale = ar ? 'ar-MA' : 'fr-MA';
  const find = selector => root.querySelector(selector);
  const status = find('[data-reviews-status]');
  const track = find('[data-reviews-track]');
  const controls = find('[data-reviews-controls]');
  const previous = find('[data-review-prev]');
  const next = find('[data-review-next]');
  let index = 0;

  function element(tag, className, text) {
    const el = doc.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  }
  function link(label, href, className = '') {
    const el = element('a', className, label);
    el.href = href;
    el.target = '_blank';
    el.rel = 'noopener noreferrer';
    return el;
  }
  function lastStart() {
    const width = track.children[0]?.getBoundingClientRect?.().width || 0;
    const gap = parseFloat(doc.defaultView?.getComputedStyle?.(track)?.columnGap) || 22;
    const visible = width && track.clientWidth ? Math.max(1, Math.round((track.clientWidth + gap) / (width + gap))) : 1;
    return Math.max(0, track.children.length - visible);
  }
  function updatePosition() {
    const n = track.children.length;
    previous.disabled = index === 0;
    next.disabled = index >= lastStart();
    find('[data-review-position]').textContent = n ? t.position(index + 1, n) : '';
  }
  function move(delta) {
    index = Math.max(0, Math.min(lastStart(), index + delta));
    const card = track.children[index];
    const reduced = doc.defaultView?.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    card?.scrollIntoView?.({behavior: reduced ? 'instant' : 'smooth', block: 'nearest', inline: 'start'});
    updatePosition();
  }
  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  track.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      e.preventDefault(); move((e.key === 'ArrowRight' ? 1 : -1) * (ar ? -1 : 1));
    }
  });
  track.addEventListener('scroll', () => {
    const viewport = track.getBoundingClientRect();
    let distance = Infinity;
    Array.from(track.children).forEach((card, i) => {
      const rect = card.getBoundingClientRect();
      const d = Math.abs(ar ? rect.right - viewport.right : rect.left - viewport.left);
      if (d < distance) { distance = d; index = i; }
    });
    index = Math.min(index, lastStart());
    updatePosition();
  }, {passive: true});
  doc.defaultView?.addEventListener?.('resize', () => { index = Math.min(index, lastStart()); updatePosition(); });

  function renderCard(review) {
    const card = element('article', 'review-card');
    const header = element('div', 'review-author');
    const avatar = element('span', 'review-avatar review-initial', (review.author?.name || '').slice(0, 1));
    avatar.setAttribute('aria-hidden', 'true'); header.append(avatar);
    const info = element('div');
    info.append(safeURL(review.author?.profileUrl)
      ? link(review.author.name, safeURL(review.author.profileUrl), 'review-author-name')
      : element('span', 'review-author-name', review.author?.name || ''));
    const date = element('time', 'review-date');
    if (review.publishTime && Number.isFinite(Date.parse(review.publishTime))) {
      date.dateTime = review.publishTime;
      date.textContent = new Intl.DateTimeFormat(locale, {day: 'numeric', month: 'long', year: 'numeric'}).format(new Date(review.publishTime));
    } else date.textContent = (ar ? review.publishedLabelAr : review.publishedLabel) || review.publishedLabel || '';
    info.append(date); header.append(info); card.append(header);
    const stars = element('div', 'review-stars', '★'.repeat(Math.round(review.rating)));
    stars.setAttribute('role', 'img');
    stars.setAttribute('aria-label', t.stars(review.rating)); card.append(stars);
    const body = element('p', 'review-text', review.text);
    body.dir = 'auto'; card.append(body);
    if (Math.max(review.text.length, review.originalText?.length || 0) > 220 || review.text.includes('\n')) {
      body.classList.add('is-collapsible');
      const expand = element('button', 'review-expand', t.read); expand.type = 'button'; expand.setAttribute('aria-expanded', 'false');
      expand.addEventListener('click', () => {
        const open = expand.getAttribute('aria-expanded') !== 'true';
        expand.setAttribute('aria-expanded', String(open)); body.classList.toggle('is-expanded', open); expand.textContent = open ? t.less : t.read;
      });
      card.append(expand);
    }
    if (review.originalText && review.originalText !== review.text) {
      const note = element('p', 'review-translation', t.translation);
      const toggle = element('button', 'review-original', t.original); toggle.type = 'button';
      let original = false;
      toggle.addEventListener('click', () => {
        original = !original; body.textContent = original ? review.originalText : review.text;
        toggle.textContent = original ? t.translated : t.original; note.hidden = original;
      });
      card.append(note, toggle);
    }
    card.append(link(t.source, safeURL(review.sourceUrl), 'review-source'));
    return card;
  }

  // These excerpts are edited locally; no Google API, cookies or remote avatar requests.
  const reviews = (Array.isArray(data.reviews) ? data.reviews : []).filter(r =>
    Number.isFinite(r.rating) && r.rating >= 4 && r.rating <= 5 && typeof r.text === 'string' && r.text.trim() && r.author?.name && safeURL(r.sourceUrl))
    .map(r => ({...r, text: ar && r.textAr ? r.textAr : r.text, originalText: r.text}));
  track.replaceChildren(...reviews.map(renderCard));
  status.textContent = reviews.length ? '' : t.empty;
  status.hidden = Boolean(reviews.length);
  track.hidden = !reviews.length;
  controls.hidden = reviews.length < 2;
  if (/^\d{4}-\d{2}-\d{2}$/.test(data.selectedOn || '')) {
    const date = new Date(`${data.selectedOn}T12:00:00Z`);
    if (Number.isFinite(date.getTime())) find('[data-reviews-selected]').textContent = t.selected(new Intl.DateTimeFormat(locale, {day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC'}).format(date));
  }
  if (data.demo === true) { const demo = find('[data-review-demo]'); demo.hidden = false; demo.textContent = t.demo; }
  updatePosition();
  return {count: reviews.length};
}

if (typeof document !== 'undefined') {
  const root = document.querySelector('[data-reviews]');
  if (root) mountReviews(root);
}
