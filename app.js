'use strict';
(() => {
  const c = window.CABINET || {};
  const ar = document.documentElement.lang === 'ar';
  const name = ar ? c.doctorNameAr : c.doctorName;
  const biography = ar ? c.biographyAr : c.biography;
  const address = ar ? c.addressAr : c.address;
  const hours = ar ? c.hoursAr : c.hours;
  const isolate = text => `\u2066${text}\u2069`;
  const messages = ar ? {
    title: `${name} · طبيب عيون بالدار البيضاء`,
    description: `${name}، طبيب عيون بالدار البيضاء. تعرّفوا على الطبيب والعيادة واطّلعوا على المعلومات العملية للتحضير لزيارتكم.`,
    home: `${name}، الصفحة الرئيسية`,
    location: `توجد العيادة في ${address}. تجدون رابط البحث عن العنوان في قسم التواصل والعنوان.`,
    appointment: `لحجز موعد، اتصلوا بالعيادة على الرقم ${isolate(c.phone)}${c.secondPhone ? ` أو ${isolate(c.secondPhone)}` : ''}. يمكن لسكرتارية العيادة إطلاعكم على المواعيد المتاحة وتفاصيل زيارتكم.`,
    call: phone => `الاتصال على الرقم ${phone}`,
    preview: 'نسخة للمعاينة · أوقات العمل ومعلومات النشر قيد التأكيد',
    openMenu: 'فتح القائمة', closeMenu: 'إغلاق القائمة',
  } : {
    title: `${name} · Ophtalmologue à Casablanca`,
    description: `${name}, ophtalmologue à Casablanca. Découvrez le médecin, le cabinet et les informations pratiques pour votre consultation.`,
    home: `${name}, accueil`,
    location: `Le cabinet se trouve ${address}. Retrouvez le lien de recherche de l’adresse dans la rubrique Contact & accès.`,
    appointment: `Pour convenir d’un rendez-vous, contactez le cabinet au ${c.phone}${c.secondPhone ? ` ou au ${c.secondPhone}` : ''}. Le secrétariat pourra vous préciser les disponibilités et les modalités de votre visite.`,
    call: phone => `Appeler le ${phone}`,
    preview: 'Version de présentation · Horaires et informations de publication à confirmer',
    openMenu: 'Ouvrir le menu', closeMenu: 'Fermer le menu',
  };
  const $ = s => document.querySelector(s);
  const set = (s, value) => { if (value) $(s).textContent = value; };
  const safeLink = value => { try { const u = new URL(value); return ['https:', 'http:'].includes(u.protocol) ? u.href : ''; } catch { return ''; } };
  const phoneHref = value => { const n = String(value || '').replace(/[\s().-]/g, ''); return /^\+?\d{6,16}$/.test(n) ? `tel:${n.startsWith('0') ? '+212' + n.slice(1) : n}` : ''; };
  set('#year', new Date().getFullYear().toString());
  if (name) {
    document.querySelectorAll('[data-brand], [data-doctor]').forEach(el => el.textContent = name);
    document.title = messages.title;
    $('meta[name="description"]').content = messages.description;
    $('meta[property="og:title"]').content = document.title;
    $('meta[property="og:description"]').content = messages.description;
    $('.brand').setAttribute('aria-label', messages.home);
  }
  set('[data-biography]', biography);
  if (address) {
    set('#address-text', address); $('#address-pending').hidden = true;
    set('#faq-address', messages.location);
  }
  if (safeLink(c.mapsUrl)) { $('#maps-link').href = safeLink(c.mapsUrl); $('#maps-link').hidden = false; }
  const primaryPhone = phoneHref(c.phone);
  if (primaryPhone) {
    set('#phone-text', c.phone); $('#phone-link').href = primaryPhone; $('#phone-link').hidden = false; $('#phone-pending').hidden = true;
    set('#faq-appointment', messages.appointment);
  }
  if (phoneHref(c.secondPhone)) {
    const p = document.createElement('p'); const a = document.createElement('a');
    a.href = phoneHref(c.secondPhone); a.textContent = c.secondPhone; a.dir = 'ltr'; a.setAttribute('aria-label', messages.call(c.secondPhone)); p.append(a); $('#phone-text').after(p);
  }
  if (c.email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c.email)) {
    const p = document.createElement('p'); const a = document.createElement('a');
    a.href = `mailto:${c.email}`; a.textContent = c.email; a.dir = 'ltr'; p.className = 'email-contact'; p.append(a); $('#phone-link').before(p);
  }
  if (safeLink(c.appointmentUrl)) { $('#appointment-link').href = safeLink(c.appointmentUrl); $('#appointment-link').hidden = false; }
  if (Array.isArray(hours) && hours.length) {
    $('#hours').replaceChildren();
    hours.forEach(({day, time}) => {
      const p = document.createElement('p'); p.className = 'hour-row';
      for (const t of [day, time]) { const span = document.createElement('span'); span.textContent = t; p.append(span); }
      $('#hours').append(p);
    });
  }
  set('#legal-editor', ar ? c.legalEditorAr : c.legalEditor);
  const previewNote = $('#preview-note');
  if (previewNote) {
    previewNote.hidden = c.presentation === false;
    if (name && address && primaryPhone) previewNote.textContent = messages.preview;
  }
  const toggle = $('.menu-toggle'); const nav = $('#navigation');
  function closeMenu() { toggle.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); $('.menu-toggle .sr-only').textContent = messages.openMenu; }
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open);
    $('.menu-toggle .sr-only').textContent = open ? messages.closeMenu : messages.openMenu;
  });
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  document.addEventListener('click', e => { if (!e.target.closest('.site-header')) closeMenu(); });
  document.querySelectorAll('.language-switch a').forEach(link => link.addEventListener('click', () => {
    link.hash = window.location.hash;
  }));
  const openDialog = dialog => { dialog.showModal(); document.body.style.overflow = 'hidden'; };
  document.querySelectorAll('[data-open]').forEach(btn => btn.addEventListener('click', () => openDialog(document.getElementById(btn.dataset.open))));
  document.querySelectorAll('dialog').forEach(dialog => {
    dialog.querySelectorAll('[data-close]').forEach(btn => btn.addEventListener('click', () => dialog.close()));
    dialog.addEventListener('click', e => {
      const r = dialog.getBoundingClientRect();
      if (e.target === dialog && (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom)) dialog.close();
    });
    dialog.addEventListener('close', () => { document.body.style.overflow = ''; });
  });
  document.querySelectorAll('[data-photo]').forEach(btn => btn.addEventListener('click', () => {
    $('#enlarged-photo').src = btn.dataset.photo; $('#enlarged-photo').alt = btn.querySelector('img').alt;
    set('#enlarged-caption', btn.dataset.caption); openDialog($('#photo-dialog'));
  }));
})();
