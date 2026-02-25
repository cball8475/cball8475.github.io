/* Florence SC Services — script.js */

const FORMSPREE = 'https://formspree.io/f/meelnjaj';
const MAILTO   = 'dumpsters@florencescservices.com';

/* NAV TOGGLE */
(function(){
  const btn = document.getElementById('nav-toggle');
  const menu = document.getElementById('mobile-menu');
  if (!btn || !menu) return;
  btn.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    btn.setAttribute('aria-expanded', String(open));
    btn.querySelector('.i-ham').style.display  = open ? 'none' : 'block';
    btn.querySelector('.i-close').style.display = open ? 'block' : 'none';
  });
  document.addEventListener('click', e => {
    if (!menu.contains(e.target) && !btn.contains(e.target)) {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded','false');
      btn.querySelector('.i-ham').style.display  = 'block';
      btn.querySelector('.i-close').style.display = 'none';
    }
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') menu.classList.remove('open');
  });
})();

/* FAQ ACCORDION */
document.querySelectorAll('.faq-q').forEach(btn => {
  btn.addEventListener('click', () => {
    const expanded = btn.getAttribute('aria-expanded') === 'true';
    document.querySelectorAll('.faq-q').forEach(b => {
      b.setAttribute('aria-expanded','false');
      const a = document.getElementById(b.getAttribute('aria-controls'));
      if (a) a.classList.remove('open');
    });
    if (!expanded) {
      btn.setAttribute('aria-expanded','true');
      const a = document.getElementById(btn.getAttribute('aria-controls'));
      if (a) a.classList.add('open');
    }
  });
});

/* FORMS */
document.querySelectorAll('.lead-form').forEach(initForm);

function initForm(form) {
  const success = form.querySelector('.form-success');
  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (!validate(form)) return;
    const btn = form.querySelector('[type=submit]');
    const orig = btn.innerHTML;
    btn.innerHTML = 'Submitting…'; btn.disabled = true;
    if (FORMSPREE) {
      try {
        const r = await fetch(FORMSPREE, { method:'POST', body: new FormData(form), headers:{Accept:'application/json'} });
        if (r.ok) { form.reset(); showSuccess(success); }
        else alert('Something went wrong. Please call us directly.');
      } catch { alert('Network error. Please call us.'); }
      finally { btn.innerHTML = orig; btn.disabled = false; }
    } else {
      window.location.href = `mailto:${MAILTO}?subject=${encodeURIComponent('Dumpster Quote Request')}&body=${buildBody(form)}`;
      showSuccess(success, true);
      btn.innerHTML = orig; btn.disabled = false;
    }
  });
}

function validate(form) {
  let ok = true;
  form.querySelectorAll('[required]').forEach(f => {
    const g = f.closest('.field');
    const e = g && g.querySelector('.field-err');
    const valid = f.type === 'checkbox' ? f.checked : f.value.trim() !== '';
    if (!valid) { ok = false; f.classList.add('err'); if(e) e.classList.add('show'); }
    else { f.classList.remove('err'); if(e) e.classList.remove('show'); }
  });
  const email = form.querySelector('[type=email]');
  if (email && email.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    ok = false; email.classList.add('err');
    const e = email.closest('.field') && email.closest('.field').querySelector('.field-err');
    if(e){ e.textContent='Enter a valid email.'; e.classList.add('show'); }
  }
  if (!ok) { const first = form.querySelector('.err'); if(first) first.focus(); }
  return ok;
}

function showSuccess(el, mailto=false) {
  if (!el) return;
  if (mailto) { el.querySelector('.s-sub').textContent = 'Your mail client opened with a pre-filled email. Send it to complete your request.'; }
  el.classList.add('show');
  el.scrollIntoView({ behavior:'smooth', block:'nearest' });
}

function buildBody(form) {
  const lines = [];
  new FormData(form).forEach((v,k) => { if(k !== '_subject') lines.push(`${k}: ${v}`); });
  return encodeURIComponent(lines.join('\n'));
}

/* ACTIVE NAV */
const path = window.location.pathname;
document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(a => {
  const href = a.getAttribute('href') || '';
  if (href && (path.endsWith(href) || (href !== 'index.html' && path.includes(href.replace('.html',''))))) {
    a.setAttribute('aria-current','page');
  }
});
