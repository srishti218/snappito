import { loadServices } from '../features/catalog/components/Catalog.js';

/**
 * Initializes Home page specific logic.
 */
export function initHome() {
  // Intersection Observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  document.querySelectorAll('.scroll-anim').forEach((el) => {
    observer.observe(el);
  });

  // Search debounce
  let searchTimeout;
  const searchInput = document.getElementById('service-search');
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => loadServices(e.target.value.trim()), 300);
    });
  }

  // Initial load
  loadServices();
  checkAuthState();
  initTheme();
}

async function checkAuthState() {
  const token = localStorage.getItem('token');
  const loginLink = document.getElementById('nav-login');
  const actionBtn  = document.getElementById('nav-action-btn');
  if (token) {
    if (loginLink) loginLink.style.display = 'none';
    if (actionBtn) {
      actionBtn.textContent = 'Go to Dashboard';
      actionBtn.href = 'dashboard.html';
      actionBtn.classList.add('nav-dashboard-btn');
    }
  }
}

function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  if (!themeToggle) return;

  const currentTheme = localStorage.getItem('theme') || 'light';
  applyTheme(currentTheme);

  themeToggle.addEventListener('click', () => {
    const newTheme = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
    applyTheme(newTheme);
    localStorage.setItem('theme', newTheme);
  });
}

function applyTheme(theme) {
  const themeToggle = document.getElementById('theme-toggle');
  if (theme === 'dark') {
    document.body.classList.add('dark-mode');
    if (themeToggle) themeToggle.textContent = '☀️';
  } else {
    document.body.classList.remove('dark-mode');
    if (themeToggle) themeToggle.textContent = '🌙';
  }
}

// Auto-init if this script is loaded as a entry
if (document.getElementById('services-grid')) {
  initHome();
}
