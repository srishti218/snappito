import { getCategories, searchServices } from '../services/catalogApi.js';
import { toSlug, escHtml } from '../../../lib/utils.js';

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&q=80&w=400';

/**
 * Toggles the visibility of a category accordion.
 * @param {string} id 
 */
export function toggleCategory(id) {
  const el = document.getElementById('cat-' + id);
  const btn = document.getElementById('cat-btn-' + id);
  const open = el.style.display !== 'none';
  el.style.display = open ? 'none' : 'block';
  if (btn) btn.textContent = open ? '▼ Expand' : '▲ Collapse';
}

/**
 * Loads services into the grid, partitioned by category or search results.
 * @param {string} query 
 */
export async function loadServices(query = '') {
  const grid = document.getElementById('services-grid');
  if (!grid) return;

  try {
    const data = query ? await searchServices(query) : await getCategories();
    grid.innerHTML = '';

    if (query) {
      renderSearchResults(data, grid);
    } else {
      renderCategoryList(data.categories || [], grid);
    }
  } catch (e) {
    console.error('loadServices error:', e);
    grid.innerHTML = '<p style="text-align:center;color:var(--text-muted);grid-column:1/-1;">We are performing maintenance. Please <a href="tel:8747858018" style="color:var(--secondary);">call us</a> to book.</p>';
  }
}

function renderSearchResults(services, grid) {
  const serviceList = Array.isArray(services) ? services : (services.services || []);
  if (serviceList.length === 0) {
    grid.innerHTML = '<p style="text-align:center;color:var(--text-muted);grid-column:1/-1">No services found. <a href="tel:8747858018" style="color:var(--secondary)">Call us</a> for custom requests.</p>';
    return;
  }
  
  serviceList.forEach(s => {
    const slug = toSlug(s.name);
    grid.innerHTML += `
      <a class="card" href="service-detail.html?service=${slug}" style="text-decoration:none;">
        <div class="card-img" style="background-image:url('${s.image_url || FALLBACK_IMG}')"></div>
        <div class="card-content">
          <h3>${s.name}</h3>
          <p>${s.description || 'Professional home service'}</p>
          <div class="price" style="display:flex;align-items:center;justify-content:space-between;">
            <span>From &#8377;${s.base_price}</span>
            <span style="font-size:13px;color:var(--secondary);font-weight:700;">View Details →</span>
          </div>
        </div>
      </a>`;
  });
}

function renderCategoryList(categories, grid) {
  if (categories.length === 0) {
    grid.innerHTML = '<p style="text-align:center;color:var(--text-muted);grid-column:1/-1">No services available right now.</p>';
    return;
  }

  categories.forEach((cat, index) => {
    const listItems = cat.services.map(s => {
      const slug = toSlug(s.name);
      return `
        <a class="catalog-service-link" href="service-detail.html?service=${slug}">
          <span class="csl-name" style="display:flex; align-items:center; gap:10px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" style="color: #064e3b;"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
            ${s.name}
          </span>
          <span class="csl-right">
            <span class="csl-price">Starts at &#8377;${s.base_price}</span>
            <span class="csl-arrow" style="font-weight: 800; font-size: 18px;">&rsaquo;</span>
          </span>
        </a>`;
    }).join('');

    grid.innerHTML += `
      <div class="catalog-category" style="grid-column:1/-1;">
        <button class="catalog-cat-header" data-cat-id="${index}" aria-expanded="false">
          <span class="cch-name">
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="color: #10b981"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" /></svg>
            ${cat.name}
          </span>
          <span class="cch-meta">
            <span class="cch-count">${cat.services.length} services</span>
            <span class="cch-chevron" id="cat-btn-${index}">▼ Expand</span>
          </span>
        </button>
        <div class="catalog-service-list" id="cat-${index}" style="display:none;">
          ${listItems}
        </div>
      </div>`;
  });

  // Attach event listeners for accordions (avoiding inline onclick)
  grid.querySelectorAll('.catalog-cat-header').forEach(btn => {
    btn.addEventListener('click', () => toggleCategory(btn.dataset.catId));
  });
}
