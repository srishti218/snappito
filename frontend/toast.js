document.addEventListener("DOMContentLoaded", () => {
    // Create container if it doesn't exist
    if(!document.getElementById('toast-container')) {
        const container = document.createElement('div');
        container.id = 'toast-container';
        document.body.appendChild(container);
    }
});

window.showToast = function(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if(!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'ℹ️';
    if(type === 'success') icon = '✅';
    if(type === 'error') icon = '❌';

    toast.innerHTML = `<span class="toast-icon">${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);
    
    // Trigger sliding animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove after 4 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400); // Wait for transition
    }, 4000);
};
