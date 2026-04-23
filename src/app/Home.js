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

  document.querySelectorAll('.scroll-anim, .step-card').forEach((el) => {
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
  
  // Robust Shield: Listen for dynamic catalog loads to hide buttons
  document.addEventListener('catalog-rendered', applyAdminShield);
}

async function checkAuthState() {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('user_role');
  const loginLink = document.getElementById('nav-login');
  const actionBtn  = document.getElementById('nav-action-btn');
  
  if (token) {
    if (loginLink) loginLink.style.display = 'none';
    if (actionBtn) {
      const is_admin = (role === 'admin');
      actionBtn.textContent = is_admin ? 'Admin Center' : 'Go to Dashboard';
      actionBtn.href = is_admin ? 'admin.html' : 'dashboard.html';
      actionBtn.classList.add('nav-dashboard-btn');
    }

    // Apply shield immediately for static elements
    applyAdminShield();
    
    // Add a notice for admins on the homepage
    if (role === 'admin') {
        const hero = document.querySelector('.hero-content');
        if (hero && !document.getElementById('admin-notice')) {
            const notice = document.createElement('div');
            notice.id = 'admin-notice';
            notice.style.background = 'rgba(16, 185, 129, 0.1)';
            notice.style.border = '1px solid var(--brand-green)';
            notice.style.color = 'var(--brand-green)';
            notice.style.padding = '10px 20px';
            notice.style.borderRadius = '30px';
            notice.style.fontSize = '12px';
            notice.style.marginTop = '20px';
            notice.style.fontWeight = '700';
            notice.innerHTML = '<i class="fas fa-user-shield"></i> ADMINISTRATIVE VIEW ACTIVE';
            hero.appendChild(notice);
        }
    }
  }
}

// Admin Shield Logic
function applyAdminShield() {
    const role = localStorage.getItem('user_role');
    if (role === 'admin') {
        const ctas = document.querySelectorAll('.hero-btn, .service-card-action, #services-section h2 button, .ps-view-all, .catalog-service-link, .card');
        ctas.forEach(btn => btn.classList.add('admin-restricted'));
    }
}

// Auto-init if this script is loaded as a entry
if (document.getElementById('services-grid')) {
  initHome();
}
