// Appearance is a browser preference, deliberately separate from portable studies.
(() => {
  const key = 'biblical-bot-color-scheme';
  const themes = ['parchment', 'rose', 'coast', 'vespers', 'aurora'];
  let theme = 'vespers';
  try {
    const stored = localStorage.getItem(key);
    if (themes.includes(stored)) theme = stored;
  } catch { /* Reading and palette selection also work without storage. */ }
  document.documentElement.dataset.theme = theme;
  document.addEventListener('DOMContentLoaded', () => {
    const picker = document.getElementById('color-scheme');
    if (!picker) return;
    picker.value = theme;
    picker.addEventListener('change', () => {
      if (!themes.includes(picker.value)) return;
      document.documentElement.dataset.theme = picker.value;
      try { localStorage.setItem(key, picker.value); } catch { /* Session-only choice. */ }
    });
  });
})();
