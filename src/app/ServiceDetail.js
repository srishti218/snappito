import { SERVICES } from '../features/catalog/data/serviceData.js';
import { renderService } from '../features/catalog/components/ServiceDetail.js';

export function runDetail() {
    const params = new URLSearchParams(window.location.search);
    const serviceId = (params.get('service') || '').trim();
    
    if (!serviceId) {
        window.location.href = 'index.html';
        return;
    }

    const found = SERVICES.find(s => s.id === serviceId);
    if (!found) {
        window.location.href = 'index.html';
        return;
    }

    renderService(found);
}

// Module entry point
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runDetail);
} else {
    runDetail();
}
