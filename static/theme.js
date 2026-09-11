(() => {
  const STORAGE_KEY = 'iris-theme';
  const media = window.matchMedia('(prefers-color-scheme: dark)');

  function preference() {
    const value = localStorage.getItem(STORAGE_KEY);
    return ['light', 'dark', 'system'].includes(value) ? value : 'system';
  }

  function resolved(mode = preference()) {
    return mode === 'system' ? (media.matches ? 'dark' : 'light') : mode;
  }

  function apply(mode = preference()) {
    document.documentElement.dataset.themeMode = mode;
    document.documentElement.dataset.theme = resolved(mode);
    document.documentElement.style.colorScheme = resolved(mode);
  }

  function installControl() {
    const actions = document.querySelector('.top-actions');
    if (!actions || document.getElementById('irisThemeSelect')) return;
    const wrap = document.createElement('label');
    wrap.className = 'theme-control';
    wrap.innerHTML = '<span>Theme</span><select id="irisThemeSelect" aria-label="Theme"><option value="system">System</option><option value="dark">Dark</option><option value="light">Light</option></select>';
    actions.prepend(wrap);
    const select = document.getElementById('irisThemeSelect');
    select.value = preference();
    select.addEventListener('change', () => {
      const mode = select.value;
      localStorage.setItem(STORAGE_KEY, mode);
      apply(mode);
    });
  }

  apply();
  media.addEventListener?.('change', () => {
    if (preference() === 'system') apply('system');
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', installControl);
  else installControl();
})();
