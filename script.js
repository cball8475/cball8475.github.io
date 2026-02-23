/* ================================================
   Florence Roll-Off Dumpster Rental Quotes
   script.js
   ================================================ */

/* ---------- CONFIG ---------- */
// Replace with your actual Formspree endpoint:
// 1. Go to https://formspree.io/ and create a free account
// 2. Create a new form and copy the endpoint URL
// 3. Paste it below (e.g. https://formspree.io/f/abcdefgh)
const FORMSPREE_ENDPOINT = ''; // <-- SET THIS TO ENABLE FORMSPREE
const MAILTO_ADDRESS = 'info@florencedumpsterquotes.com'; // <-- UPDATE TO YOUR EMAIL

/* ---------- MOBILE NAV ---------- */
(function initNav() {
  const toggle = document.getElementById('nav-toggle');
  const menu = document.getElementById('mobile-menu');
  if (!toggle || !menu) return;

  toggle.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('.icon-ham').style.display = open ? 'none' : 'block';
    toggle.querySelector('.icon-close').style.display = open ? 'block' : 'none';
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!menu.contains(e.target) && !toggle.contains(e.target)) {
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.querySelector('.icon-ham').style.display = 'block';
      toggle.querySelector('.icon-close').style.display = 'none';
    }
  });

  // Close on Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.querySelector('.icon-ham').style.display = 'block';
      toggle.querySelector('.icon-close').style.display = 'none';
    }
  });
})();

/* ---------- FAQ ACCORDION ---------- */
(function initFAQs() {
  const questions = document.querySelectorAll('.faq-question');
  questions.forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      // Close all
      questions.forEach(q => {
        q.setAttribute('aria-expanded', 'false');
        const ans = document.getElementById(q.getAttribute('aria-controls'));
        if (ans) ans.classList.remove('open');
      });
      // Open clicked if it was closed
      if (!expanded) {
        btn.setAttribute('aria-expanded', 'true');
        const ans = document.getElementById(btn.getAttribute('aria-controls'));
        if (ans) ans.classList.add('open');
      }
    });
  });
})();

/* ---------- LEAD FORM ---------- */
(function initForms() {
  const forms = document.querySelectorAll('.lead-form');
  forms.forEach(form => initForm(form));
})();

function initForm(form) {
  if (!form) return;
  const successEl = form.querySelector('.form-success');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!validateForm(form)) return;

    const submitBtn = form.querySelector('[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Submitting…';
    submitBtn.disabled = true;

    if (FORMSPREE_ENDPOINT) {
      // --- Formspree path ---
      try {
        const data = new FormData(form);
        const res = await fetch(FORMSPREE_ENDPOINT, {
          method: 'POST',
          body: data,
          headers: { Accept: 'application/json' }
        });
        if (res.ok) {
          form.reset();
          showSuccess(form, successEl);
        } else {
          const json = await res.json().catch(() => ({}));
          alert('There was a problem submitting your request. Please try again or call us directly.');
        }
      } catch (err) {
        alert('Network error. Please try again or call us directly.');
      } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      }
    } else {
      // --- mailto fallback ---
      const subject = encodeURIComponent('Dumpster Rental Quote Request');
      const body = buildMailtoBody(form);
      window.location.href = `mailto:${MAILTO_ADDRESS}?subject=${subject}&body=${body}`;
      showSuccess(form, successEl, true);
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    }
  });
}

function validateForm(form) {
  let valid = true;
  const required = form.querySelectorAll('[required]');
  required.forEach(field => {
    const group = field.closest('.form-group');
    const errorEl = group ? group.querySelector('.field-error') : null;
    let fieldValid = true;

    if (field.type === 'checkbox') {
      fieldValid = field.checked;
    } else {
      fieldValid = field.value.trim() !== '';
    }

    if (!fieldValid) {
      valid = false;
      field.classList.add('error');
      if (errorEl) errorEl.classList.add('visible');
    } else {
      field.classList.remove('error');
      if (errorEl) errorEl.classList.remove('visible');
    }
  });

  // Email format if provided
  const emailField = form.querySelector('[type="email"]');
  if (emailField && emailField.value.trim()) {
    const emailGroup = emailField.closest('.form-group');
    const emailError = emailGroup ? emailGroup.querySelector('.field-error') : null;
    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailField.value.trim());
    if (!emailValid) {
      valid = false;
      emailField.classList.add('error');
      if (emailError) { emailError.textContent = 'Please enter a valid email address.'; emailError.classList.add('visible'); }
    }
  }

  if (!valid) {
    const firstError = form.querySelector('.error');
    if (firstError) firstError.focus();
  }
  return valid;
}

function showSuccess(form, successEl, isMailto = false) {
  if (!successEl) return;
  if (isMailto) {
    successEl.querySelector('.success-main').textContent = 'Your mail client has been opened.';
    successEl.querySelector('.success-sub').textContent = 'Please send the pre-filled email to complete your request. If it didn\'t open, email us directly at ' + MAILTO_ADDRESS;
  }
  successEl.classList.add('visible');
  successEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function buildMailtoBody(form) {
  const data = new FormData(form);
  let lines = [];
  data.forEach((val, key) => {
    if (key !== '_subject') lines.push(`${key}: ${val}`);
  });
  return encodeURIComponent(lines.join('\n'));
}

/* ---------- ACTIVE NAV LINK ---------- */
(function setActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(link => {
    const href = link.getAttribute('href');
    if (!href) return;
    const linkPath = href.replace(/^\.\.\//, '/pages/').replace(/^\.\//, '/');
    if (path.endsWith(href) || (href !== '/' && path.includes(href.replace('../', '')))) {
      link.setAttribute('aria-current', 'page');
    }
  });
})();
