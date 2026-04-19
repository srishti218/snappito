import { getProfile, getAddresses, addAddress } from '../services/userService.js';
import { getWalletBalance, createPaymentOrder } from '../services/walletService.js';
import { request } from '../services/apiClient.js';

export async function initDashboard() {
  const token = localStorage.getItem('token');
  if (!token) { window.location.href = 'login.html'; return; }

  try {
    const profile = await getProfile();
    renderProfile(profile);
    await loadDashboardData();
  } catch (err) {
    console.error('Session expired or error:', err);
    localStorage.removeItem('token');
    window.location.href = 'login.html';
  }
}

async function loadDashboardData() {
  try {
    const balance = await getWalletBalance();
    document.getElementById('wallet-balance').textContent = Number(balance.balance || 0).toLocaleString('en-IN', {minimumFractionDigits: 2});
    
    await loadBookings();
    await loadAddresses();
  } catch (e) {
    console.warn('Silent data load fail:', e);
  }
}

function renderProfile(data) {
    const firstName = data.full_name.split(' ')[0];
    document.getElementById('welcome-text').innerText = `Hi, ${firstName}!`;
    document.getElementById('header-email').innerText = data.email;
    
    const avatar = data.profile_image || 'src/assets/images/premium/hero_bg.png'; // Placeholder avatar
    document.getElementById('header-avatar').src = avatar;
    
    document.getElementById('loader').style.display = 'none';
    document.getElementById('content').style.display = 'grid'; // Layout uses grid
}

async function loadBookings() {
    const bookings = await request('/api/bookings', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    });
    
    const listSmall = document.getElementById('booking-list-small');
    const listFull  = document.getElementById('booking-list-full');
    const activeCount = document.getElementById('active-bookings-count');
    
    if (activeCount) activeCount.textContent = bookings.filter(b => b.status === 'confirmed').length;

    const bookingHtml = bookings.length === 0 
        ? `<div style="text-align: center; padding: 40px; color: var(--text-muted);"><i class="fas fa-calendar-times" style="font-size: 40px; margin-bottom: 10px;"></i><p>No bookings found.</p></div>`
        : bookings.map(b => `
            <div class="booking-item">
                <div>
                   <h4 style="color: var(--primary-dark);">#${b.booking_id.substring(0,8).toUpperCase()}</h4>
                   <p style="font-size: 14px; color: var(--text-muted);">${new Date(b.scheduled_time).toLocaleDateString()} at ${new Date(b.scheduled_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
                </div>
                <div style="text-align: right;">
                   <span class="status-badge ${b.status === 'confirmed' ? 'status-confirmed' : 'status-pending'}">${b.status}</span>
                   <p style="font-size: 12px; margin-top: 4px; color: var(--text-muted); cursor: pointer;" onclick="cancelBooking('${b.booking_id}')">Cancel</p>
                </div>
            </div>`).join('');

    if (listSmall) listSmall.innerHTML = bookingHtml;
    if (listFull)  listFull.innerHTML  = bookingHtml;
}

async function loadAddresses() {
  try {
    const addresses = await getAddresses();
    const listFull = document.getElementById('address-list-full');
    if (!addresses || addresses.length === 0) {
        if (listFull) listFull.innerHTML = `<p style="grid-column: 1/-1; color: var(--text-muted);">No addresses saved yet.</p>`;
        return;
    }
    const addrHtml = addresses.map(a => `
        <div class="booking-item" style="padding: 15px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: var(--bg-slate); width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <i class="fas fa-home" style="color: var(--primary);"></i>
                </div>
                <div>
                   <h4 style="font-size: 15px;">${a.label || 'Home'}</h4>
                   <p style="font-size: 12px; color: var(--text-muted);">${a.line1}, ${a.city}</p>
                </div>
            </div>
        </div>`).join('');
    
    if (listFull) listFull.innerHTML = addrHtml;
  } catch(e) {}
}

// window.switchSection is now handled inline in dashboard.html to prevent caching issues
/*
window.switchSection = (section, el) => {
    ...
};
*/// ─── Event Handlers ──────────────────────────────────────────────

window.logout = () => {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
};

window.openWalletModal = () => {
    document.getElementById('wallet-modal').style.display = 'flex';
};

window.closeModal = (id) => {
    document.getElementById(id).style.display = 'none';
};

window.handleTopup = async () => {
    const amt = document.getElementById('topup-amount').value;
    if (!amt || amt < 100) {
        if (window.showToast) window.showToast('Minimum top-up is ₹100', 'error');
        return;
    }
    try {
        const order = await createPaymentOrder(amt);
        if (window.showToast) window.showToast('Redirecting to Payment...', 'success');
        // Razorpay logic integration would go here
    } catch (e) {
        if (window.showToast) window.showToast('Payment failed to initialize', 'error');
    }
};

window.switchSection = (section, el) => {
    // Update active class
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    el.classList.add('active');

    // For now, we'll just show toasts for WIP sections
    if (section === 'wallet' || section === 'settings') {
        if (window.showToast) window.showToast('Section coming soon!', 'info');
        return;
    }
    
    // In a real SPA we would hide/show containers
    if (window.showToast) window.showToast(`Switched to ${section}`, 'success');
};

window.openAddressModal = () => {
    document.getElementById('address-modal').style.display = 'flex';
};

window.submitAddress = async () => {
    const label = document.getElementById('addr-label').value;
    const line1 = document.getElementById('addr-line').value;
    const city = document.getElementById('addr-city').value;
    const zipcode = document.getElementById('addr-zip').value;
    const isDefault = document.getElementById('addr-default').checked;

    if (!line1 || !city) {
        if (window.showToast) window.showToast('Address and City are required.', 'error');
        return;
    }

    try {
        await addAddress({ label, line1, city, zipcode, is_default: isDefault });
        if (window.showToast) window.showToast('Address added successfully!', 'success');
        closeModal('address-modal');
        loadAddresses();
    } catch (e) {
        if (window.showToast) window.showToast('Failed to save address.', 'error');
    }
};

// ─── Auto-init ──────────────────────────────────────────────────
if (document.getElementById('welcome-text')) {
    initDashboard();
}
