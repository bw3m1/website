(function () {
  // Get DOM elements
  const tocContainer = document.getElementById('tocContainer');
  const tocToggle = document.getElementById('tocToggle');
  const tocLinks = document.querySelectorAll('.toc a');
  const sections = document.querySelectorAll('section');

    // Apply system theme
    function applySystemTheme() {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      document.body.classList.toggle('dark', prefersDark);
    }

  // Toggle TOC visibility
  function toggleTOC() {
    tocContainer.classList.toggle('visible');
    // Adjust main content width when TOC is visible
    const mainContent = document.querySelector('main');
    if (mainContent) {
      if (tocContainer.classList.contains('visible')) {
        mainContent.style.width = 'calc(100% - var(--toc-width))';
      } else {
        mainContent.style.width = '';
      }
    }
  }

  function getIcon(name) {
    const isDark = document.body.classList.contains('dark');
    if (name === "home") {
      return isDark ? "../icons/home_dark.svg" : "../icons/home_light.svg";
    } else if (name === "toggle-toc") {
      return isDark ? "../icons/toggle_toc_dark.svg" : "../icons/toggle_toc_light.svg";
    } else if (name === "close-toc") {
      return isDark ? "../icons/close_toc_dark.svg" : "../icons/close_toc_light.svg";
    }
    return '';
  }

  function setIcon(name) {
    if (name === "home") {
      const home = document.getElementById("home");
      home.setAttribute('src', getIcon("home"));
    } else if (name === "toggle-toc") {
      const toggleToc = document.getElementById("toggle-toc");
      toggleToc.setAttribute('src', getIcon("toggle-toc"));
    }  else if (name === "close-toc") {
      const toggleToc = document.getElementById("close-toc");
      toggleToc.setAttribute('src', getIcon("close-toc"));
    } else {
      console.error("icon name invalid");
    }
  }

  // Initialize
  function init() {
    // Set up theme
    applySystemTheme();
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      applySystemTheme();
      setIcon("home");
      setIcon("toggle-toc");
      setIcon("close-toc");
    });

    // Set initial icons
    setIcon("home");
    setIcon("toggle-toc");
    setIcon("close-toc");

    // Set up TOC toggle button
    if (tocToggle) {
      tocToggle.addEventListener('click', toggleTOC);
    }

    // Set up elements with data-action="toggle-toc"
    const tocTogglers = document.querySelectorAll('[data-action="toggle-toc"]');
    tocTogglers.forEach(toggler => {
      toggler.addEventListener('click', function (e) {
        e.preventDefault();
        toggleTOC();
      });
    });

    // Toggle with 'c' key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'c' || e.key === 'C') {
        e.preventDefault();
        toggleTOC();
      }
    });

    // Close TOC when clicking outside on mobile (ignore toggle elements)
    document.addEventListener('click', function (e) {
      if (window.innerWidth <= 1200) {
        const isClickOnToggler = (
          (tocToggle && tocToggle.contains(e.target)) ||
          e.target.closest('[data-action="toggle-toc"]')
        );

        if (!tocContainer.contains(e.target) && !isClickOnToggler) {
          tocContainer.classList.remove('visible');
        }
      }
    });

    // Smooth scrolling with highlighting
    tocLinks.forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
          targetElement.scrollIntoView({ behavior: 'smooth' });
          targetElement.classList.add('highlight');
          setTimeout(() => targetElement.classList.remove('highlight'), 1500);

          if (window.innerWidth <= 1200) {
            tocContainer.classList.remove('visible');
          }
        }
      });
    });

    // Highlight current section in TOC
    function updateActiveTocLink() {
      let currentSection = '';
      sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (window.scrollY >= sectionTop - 100) {
          currentSection = '#' + section.getAttribute('id');
        }
      });

      tocLinks.forEach(link => {
        link.style.fontWeight = link.getAttribute('href') === currentSection ? 'bold' : 'normal';
      });
    }

    window.addEventListener('scroll', updateActiveTocLink);
    updateActiveTocLink();
  }

  // Start the application
  init();
})();
