// Main JS for theme toggle, mobile menu, and unauthenticated homepage modal
document.addEventListener('DOMContentLoaded', () => {
  const root = document.documentElement;
  const toggle = document.getElementById('theme-toggle');
  const sun = document.getElementById('theme-sun');
  const moon = document.getElementById('theme-moon');
  
  // ============================================
  // Theme Toggle Functionality
  // ============================================
  function applyTheme(theme) {
    if (theme === 'light') {
      root.classList.add('light-mode');
      if (sun) sun.classList.remove('hidden');
      if (moon) moon.classList.add('hidden');
      document.documentElement.style.colorScheme = 'light';
    } else {
      root.classList.remove('light-mode');
      if (sun) sun.classList.add('hidden');
      if (moon) moon.classList.remove('hidden');
      document.documentElement.style.colorScheme = 'dark';
    }
  }

  // Initialize from localStorage
  const saved = localStorage.getItem('sl_theme') || 'dark';
  applyTheme(saved === 'light' ? 'light' : 'dark');

  if (toggle) {
    toggle.addEventListener('click', () => {
      const current = document.documentElement.classList.contains('light-mode') ? 'light' : 'dark';
      const next = current === 'light' ? 'dark' : 'light';
      applyTheme(next);
      localStorage.setItem('sl_theme', next);
    });
  }

  // ============================================
  // Mobile Menu Toggle Functionality
  // ============================================
  const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
  const mobileNavDrawer = document.getElementById('mobile-nav-drawer');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

  if (mobileMenuToggle && mobileNavDrawer) {
    mobileMenuToggle.addEventListener('click', () => {
      mobileNavDrawer.classList.toggle('open');
      mobileMenuToggle.classList.toggle('active');
    });

    // Close drawer when a link is clicked
    mobileNavLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileNavDrawer.classList.remove('open');
        mobileMenuToggle.classList.remove('active');
      });
    });

    // Close drawer when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.nav-bar')) {
        if (mobileNavDrawer.classList.contains('open')) {
          mobileNavDrawer.classList.remove('open');
          mobileMenuToggle.classList.remove('active');
        }
      }
    });
  }

  // ============================================
  // Unauthenticated Homepage Modal
  // ============================================
  try {
    const unauth = document.body.dataset.unauth === '1';
    const onIndex = document.body.dataset.page === 'index';
    if (unauth && onIndex) {
      // Show modal after 2s
      setTimeout(() => {
        const modal = document.getElementById('home-auth-modal');
        if (modal) {
          modal.style.display = 'flex';

          // Close handler
          const closeBtn = modal.querySelector('.close-btn');
          if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
              e.preventDefault();
              modal.style.display = 'none';
            });
          }

          // Close modal when clicking outside (on backdrop)
          modal.addEventListener('click', (e) => {
            if (e.target === modal) {
              modal.style.display = 'none';
            }
          });
        }
      }, 2000);
    }
  } catch (e) {
    // Ignore errors in modal initialization
    console.debug('Modal initialization skipped:', e);
  }
});
