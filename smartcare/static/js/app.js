/* SmartCare X — minimal shared JavaScript.
   Business logic never lives here; this only handles small UX niceties
   (loading state, tooltips, auto-dismiss). Page-specific interactivity
   (AJAX slot lookups, dynamic form rows) lives in each template's
   {% block extra_js %}. */

document.addEventListener('DOMContentLoaded', function () {
  injectSpinnerOverlay();
  wireLoadingSpinner();
  autoDismissAlerts();
  initTooltips();
});

function injectSpinnerOverlay() {
  if (document.querySelector('.sc-spinner-overlay')) return;
  const overlay = document.createElement('div');
  overlay.className = 'sc-spinner-overlay';
  overlay.innerHTML = '<div class="spinner-border" style="color: var(--sc-primary); width: 3rem; height: 3rem;" role="status"><span class="visually-hidden">Loading...</span></div>';
  document.body.appendChild(overlay);
}

function wireLoadingSpinner() {
  const overlay = document.querySelector('.sc-spinner-overlay');
  document.querySelectorAll('form:not([data-no-spinner])').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      // If the form has a confirm() dialog and the user cancels, this still
      // fires — but the browser blocks navigation until confirm resolves,
      // so the spinner briefly showing on a cancelled action is harmless.
      if (event.defaultPrevented) return;
      // Delay showing the overlay by 300ms — most page transitions on a
      // local/fast connection finish before this timer fires, so the
      // spinner never flashes on screen for quick operations. It only
      // becomes visible for genuinely slow ones (large PDF generation,
      // bill creation, etc.), which is when a loading indicator actually
      // helps rather than just adding visual noise.
      setTimeout(function () {
        overlay.classList.add('active');
      }, 300);
    });
  });
}

function autoDismissAlerts() {
  document.querySelectorAll('.alert.alert-dismissible').forEach(function (alertEl) {
    setTimeout(function () {
      const instance = bootstrap.Alert.getOrCreateInstance(alertEl);
      instance.close();
    }, 6000);
  });
}

function initTooltips() {
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
    new bootstrap.Tooltip(el);
  });
}
