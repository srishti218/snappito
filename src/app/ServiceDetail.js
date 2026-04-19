import { SERVICES } from '../features/catalog/data/serviceData.js';
import { renderService } from '../features/catalog/components/ServiceDetail.js';

export function runDetail() {
    const params = new URLSearchParams(window.location.search);
    const slug = (params.get('service') || '').trim();
    const dbId = (params.get('service_id') || '').trim();
    
    if (!slug) {
        window.location.href = 'index.html';
        return;
    }

    const found = SERVICES.find(s => s.id === slug);
    if (!found) {
        window.location.href = 'index.html';
        return;
    }

    // Attach the real database UUID so it propagates to booking
    if (dbId) found.db_id = dbId;

    renderService(found);
}

// Module entry point
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runDetail);
} else {
    runDetail();
}
