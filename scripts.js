(function() {
  function applySystemTheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.body.classList.toggle('dark', prefersDark);
  }

  // Apply on load
  applySystemTheme();

  // Listen for changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applySystemTheme);
})();
