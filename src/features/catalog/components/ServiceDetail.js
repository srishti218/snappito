import { escHtml } from '../../../lib/utils.js';

export let currentService = null;
export let currentTier = null;

const ASSET_ROOT = 'src/assets/images/premium/';
const FALLBACK_HERO = ASSET_ROOT + 'hero_bg.png';

export function selectTier(tierKey) {
    if (!currentService) return;
    
    // Find tier by ID or Name
    const tier = currentService.tiers.find(t => 
        (t.id && t.id.toLowerCase() === tierKey.toLowerCase()) || 
        (t.name && t.name.toLowerCase() === tierKey.toLowerCase())
    ) || currentService.tiers[0];
    
    currentTier = tier;

    const displayPrice = document.getElementById('display-price');
    if (displayPrice) {
        displayPrice.textContent = tier.price.toLocaleString('en-IN');
    }

    // Toggle active classes
    document.querySelectorAll('.tier-option').forEach(opt => {
        const optKey = opt.getAttribute('data-tier') || '';
        opt.classList.toggle('active', optKey.toLowerCase() === tierKey.toLowerCase());
    });
}

export function renderService(service) {
    if (!service) return;
    currentService = service;
    
    const elements = {
        title: document.getElementById('service-title'),
        desc: document.getElementById('service-desc'),
        hero: document.getElementById('hero-img'),
        includes: document.getElementById('included-list'),
        excludes: document.getElementById('excluded-list')
    };

    if (elements.title) elements.title.textContent = service.title;
    if (elements.desc) elements.desc.textContent = service.description || "Professional cleaning service delivered with precision.";
    
    if (elements.hero) {
        const imgMap = {
            "bathroom-cleaning": "bathroom.png",
            "kitchen-cleaning": "kitchen.png",
            "fan-cleaning": "fan.png",
            "windows-cleaning": "window.png",
            "laundry": "laundry.png",
            "utensils": "dishwashing.png",
            "sweeping-and-mopping": "sweeping-mopping.png"
        };
        const fname = imgMap[service.id] || "hero_bg.png";
        elements.hero.style.backgroundImage = `url('${ASSET_ROOT + fname}')`;
    }

    if (elements.includes) {
        elements.includes.innerHTML = (service.includes || []).map(item => `
            <div class="list-item">
                <span class="check-icon">✔</span>
                <span>${escHtml(item)}</span>
            </div>
        `).join('');
    }

    if (elements.excludes) {
        elements.excludes.innerHTML = (service.excludes || []).map(item => `
            <div class="list-item">
                <span class="cross-icon">✘</span>
                <span>${escHtml(item)}</span>
            </div>
        `).join('');
    }

    // Dynamic Tier Selector
    const tierContainer = document.querySelector('.tier-selector');
    if (tierContainer && service.tiers) {
        tierContainer.innerHTML = service.tiers.map(t => `
            <div class="tier-option" data-tier="${t.name}" onclick="selectTier('${t.name}')">
              <h4>${t.name}</h4>
              <span>${t.duration}</span>
            </div>
        `).join('');
    }

    // Default to the first tier
    if (service.tiers && service.tiers.length > 0) {
        selectTier(service.tiers[0].name);
    }
}

export function handleBook() {
    if (!currentService || !currentTier) return;
    const params = new URLSearchParams({
        service_id: currentService.db_id || currentService.id,
        service: currentService.title,
        tier: currentTier.name,
        price: currentTier.price
    });
    window.location.href = `booking.html?${params.toString()}`;
}

// Global exposure for simple HTML bridge
window.selectTier = selectTier;
window.proceedToBooking = handleBook;
