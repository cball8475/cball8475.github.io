/* Florence SC Services — shared site JS
   Covers: nav toggle, mobile dropdown, dropdown nav, FAQ accordion
   form submission is handled inline in each page
*/

(function () {

  /* ── NAV TOGGLE (hamburger) ─────────────────────────────────────── */
  var navBtn  = document.getElementById('nav-toggle');
  var mobileMenu = document.getElementById('mobile-menu');

  if (navBtn && mobileMenu) {
    var ham   = navBtn.querySelector('.i-ham');
    var close = navBtn.querySelector('.i-close');

    navBtn.addEventListener('click', function () {
      var open = mobileMenu.classList.toggle('open');
      navBtn.setAttribute('aria-expanded', open);
      navBtn.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      if (ham)   ham.style.display   = open ? 'none' : '';
      if (close) close.style.display = open ? ''     : 'none';
    });

    document.addEventListener('click', function (e) {
      if (!navBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
        mobileMenu.classList.remove('open');
        navBtn.setAttribute('aria-expanded', 'false');
        if (ham)   ham.style.display   = '';
        if (close) close.style.display = 'none';
      }
    });

    mobileMenu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        mobileMenu.classList.remove('open');
        navBtn.setAttribute('aria-expanded', 'false');
        if (ham)   ham.style.display   = '';
        if (close) close.style.display = 'none';
      });
    });
  }

  /* ── DROPDOWN NAV ───────────────────────────────────────────────── */
  document.querySelectorAll('.nav-dropdown-trigger').forEach(function (trigger) {
    var menu = trigger.nextElementSibling;
    trigger.addEventListener('click', function (e) {
      e.preventDefault();
      var open = menu.classList.toggle('open');
      trigger.setAttribute('aria-expanded', open);
    });
  });

  document.addEventListener('click', function (e) {
    document.querySelectorAll('.nav-dropdown').forEach(function (dd) {
      if (!dd.contains(e.target)) {
        var m = dd.querySelector('.nav-dropdown-menu');
        var t = dd.querySelector('.nav-dropdown-trigger');
        if (m) m.classList.remove('open');
        if (t) t.setAttribute('aria-expanded', 'false');
      }
    });
  });

  /* ── MOBILE DROPDOWN ────────────────────────────────────────────── */
  document.querySelectorAll('.mobile-dropdown-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var menu = btn.nextElementSibling;
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
      btn.classList.toggle('open', open);
    });
  });

  /* ── FAQ ACCORDION ──────────────────────────────────────────────── */
  document.querySelectorAll('.faq-q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var targetId = btn.getAttribute('aria-controls');
      var panel    = document.getElementById(targetId);
      if (!panel) return;
      var isOpen = panel.classList.toggle('open');
      btn.setAttribute('aria-expanded', isOpen);
    });
  });

})();
