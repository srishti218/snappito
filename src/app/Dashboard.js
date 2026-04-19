import { getProfile, getAddresses, addAddress } from '../services/userService.js';
import { getWalletBalance, createPaymentOrder } from '../services/walletService.js';
import { request } from '../services/apiClient.js';

export async function initDashboard() {
  const token = localStorage.getItem('token');
  if (!token) { window.location.href = 'login.html'; return; }

  const role = localStorage.getItem('user_role');
  
  // URL Param Check
  const urlParams = new URLSearchParams(window.location.search);
  const viewParam = urlParams.get('view');
  
  // Security Enforcement: Cross-role deep link protection
  if (role === 'admin') {
      window.location.href = 'admin.html';
      return;
  }
  
  if (viewParam === 'pro' && role !== 'professional') {
      console.warn("Unauthorized view access. Stripping parameters.");
      window.location.href = 'dashboard.html';
      return;
  }

  // Trigger UI Toggle immediately to prevent flicker
  toggleRoleUI(role);

  try {
    const profile = await getProfile();
    renderProfile(profile);
    await loadDashboardData();
  } catch (err) {
    console.error('Session expired or error:', err);
    localStorage.clear();
    window.location.href = 'login.html';
  }
}

function toggleRoleUI(role) {
    if (role === 'professional') {
        // Hide Customer Sections
        document.querySelectorAll('.customer-only').forEach(el => el.classList.add('hidden'));
        const walletSection = document.getElementById('wallet-section');
        const newBookingBtn = document.getElementById('new-booking-btn');
        if (walletSection) walletSection.classList.add('hidden');
        if (newBookingBtn) newBookingBtn.classList.add('hidden');

        // Sidebar Injection: Ensure Pro Schedule link is present
        const sidebarNav = document.getElementById('sidebar-nav');
        if (sidebarNav && !document.querySelector('.pro-only-nav')) {
            const proNavItem = document.createElement('div');
            proNavItem.className = 'nav-item pro-only pro-only-nav';
            proNavItem.innerHTML = '<i class="fas fa-clipboard-check"></i> Pro Schedule';
            proNavItem.onclick = () => window.switchSection('pro-schedule', proNavItem);
            
            // Insert before Wallet or at end
            const walletNav = document.querySelector('.nav-item[onclick*="wallet"]');
            if (walletNav) sidebarNav.insertBefore(proNavItem, walletNav);
            else sidebarNav.appendChild(proNavItem);
        }

        const proNavElement = document.querySelector('.pro-only-nav');
        if (proNavElement) proNavElement.style.display = 'flex';
        
        const proStats = document.getElementById('pro-stats-grid');
        if (proStats) proStats.classList.remove('hidden');

        // Force switch to schedule view if reached via ?view=pro
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('view') === 'pro' && window.switchSection) {
            // Delay slightly to ensure switchSection is ready
            setTimeout(() => {
                const proNav = document.querySelector('.pro-only-nav');
                if (proNav) window.switchSection('pro-schedule', proNav);
            }, 100);
        }
    } else {
        // Customer View
        document.querySelectorAll('.pro-only').forEach(el => el.classList.add('hidden'));
        document.querySelectorAll('.customer-only').forEach(el => el.classList.remove('hidden'));
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
    document.getElementById('welcome-text').innerText = (data.user_type === 'professional') 
        ? `Pro Dashboard, ${firstName}` 
        : `Hi, ${firstName}!`;
        
    document.getElementById('header-email').innerText = data.email;
    
    const avatar = data.profile_image || 'src/assets/images/premium/hero_bg.png';
    document.getElementById('header-avatar').src = avatar;
    
    // RBAC Final Check & Pro Logic
    if (data.user_type === 'professional') {
        if (window.loadProSchedule) window.loadProSchedule();
    }
    
    document.getElementById('loader').style.display = 'none';
    document.getElementById('content').style.display = 'grid';
}
async function loadBookings() {
    const bookings = await request('/api/bookings', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    });
    
    const listSmall = document.getElementById('booking-list-small');
    const listFull  = document.getElementById('booking-list-full');
    const activeCount = document.getElementById('active-bookings-count-cust');
    
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
    localStorage.clear();
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

// switchSection is handled inline in dashboard.html to avoid race conditions with module loading

window.openAddressModal = () => {
    document.getElementById('address-modal').style.display = 'flex';
};

window.submitAddress = async () => {
    const label = document.getElementById('addr-label').value;
    const hno = document.getElementById('addr-hno').value;
    const landmark = document.getElementById('addr-landmark').value;
    const area = document.getElementById('addr-area').value;
    const city = document.getElementById('addr-city').value;
    const state = document.getElementById('addr-state').value;
    const zipcode = document.getElementById('addr-zip').value;
    const isDefault = document.getElementById('addr-default').checked;

    if (!hno || !area || !city) {
        if (window.showToast) window.showToast('House No, Area, and City are required.', 'error');
        return;
    }

    // Combine detailed fields into line1 for the database
    // Structure: "House No, Area, Landmark"
    const line1 = `${hno}${landmark ? ', ' + landmark : ''}, ${area}`;

    try {
        await addAddress({ label, line1, city, state, zipcode, is_default: isDefault });
        if (window.showToast) window.showToast('Address added successfully!', 'success');
        closeModal('address-modal');
        loadAddresses();
    } catch (e) {
        if (window.showToast) window.showToast('Failed to save address.', 'error');
    }
};

// ─── Auto-fill Pincode Logic ─────────────────────────────────────────
document.addEventListener('input', async (e) => {
    if (e.target && e.target.id === 'addr-zip') {
        const pin = e.target.value.trim();
        if (pin.length === 6 && /^\d+$/.test(pin)) {
            const cityInput = document.getElementById('addr-city');
            const stateInput = document.getElementById('addr-state');
            
            cityInput.placeholder = "Searching...";
            stateInput.placeholder = "Searching...";

            try {
                const response = await fetch(`https://api.postalpincode.in/pincode/${pin}`);
                const data = await response.json();
                
                if (data[0] && data[0].Status === "Success") {
                    const info = data[0].PostOffice[0];
                    cityInput.value = info.District;
                    stateInput.value = info.State;
                    if (window.showToast) window.showToast(`Found: ${info.District}, ${info.State}`, 'success');
                } else {
                    cityInput.placeholder = "City";
                    stateInput.placeholder = "State";
                }
            } catch (err) {
                console.error("Pincode fetch error:", err);
                cityInput.placeholder = "City";
                stateInput.placeholder = "State";
            }
        }
    }
});

window.loadProSchedule = async () => {
    try {
        const schedule = await request('/api/pro/schedule', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        
        const list = document.getElementById('pro-schedule-list');
        const activeCount = document.getElementById('active-bookings-count-pro');
        const activeTasks = schedule.filter(b => !['completed', 'canceled'].includes(b.status));
        
        if (activeCount) activeCount.textContent = activeTasks.length;
        
        if (!schedule || schedule.length === 0) {
            list.innerHTML = `<div style="text-align: center; padding: 40px; color: var(--text-muted);"><i class="fas fa-bed" style="font-size: 30px; margin-bottom: 10px;"></i><p>No jobs assigned to you right now. Relax!</p></div>`;
            return;
        }

        const nextStatus = {
            'assigned': 'en-route',
            'en-route': 'started',
            'started': 'completed'
        };

        const statusLabels = {
            'assigned': 'Start Journey (En-Route)',
            'en-route': 'Arrived & Start Job',
            'started': 'Mark as Completed'
        };

        list.innerHTML = schedule.map(b => `
            <div class="booking-item" style="flex-direction: column; align-items: flex-start; gap: 15px;">
                <div style="display: flex; justify-content: space-between; width: 100%;">
                    <div>
                        <h4 style="color: var(--primary); font-size: 16px;">${b.service_name}</h4>
                        <p style="font-size: 13px; color: var(--text-muted);"><i class="fas fa-clock"></i> ${new Date(b.scheduled_time).toLocaleString()}</p>
                    </div>
                    <span class="status-badge status-${b.status === 'completed' ? 'confirmed' : 'pending'}">${b.status}</span>
                </div>
                
                <div style="background: var(--bg-slate); width: 100%; padding: 15px; border-radius: 8px;">
                    <p style="font-weight: 600; font-size: 14px; margin-bottom: 5px;"><i class="fas fa-user"></i> ${b.customer_name}</p>
                    <p style="font-size: 13px; color: var(--text-muted);"><i class="fas fa-phone"></i> ${b.customer_phone || 'N/A'}</p>
                    <p style="font-size: 13px; color: var(--text-muted); margin-top: 5px;"><i class="fas fa-map-marker-alt"></i> ${b.address}</p>
                    ${b.instructions ? `<p style="font-size: 13px; color: #d97706; margin-top: 5px;"><i class="fas fa-info-circle"></i> ${b.instructions}</p>` : ''}
                </div>
                
                ${nextStatus[b.status] ? `
                <div style="width: 100%; text-align: right;">
                    <button class="btn-sm btn-assign" onclick="window.updateJobStatus('${b.booking_id}', '${nextStatus[b.status]}')" style="padding: 10px 20px; font-size: 13px; cursor: pointer; border:none; border-radius:8px; font-weight:700;">
                        ${statusLabels[b.status]} <i class="fas fa-arrow-right"></i>
                    </button>
                </div>
                ` : ''}
            </div>
        `).join('');
    } catch(err) {
        console.error(err);
    }
};

window.updateJobStatus = async (bookingId, status) => {
    if (!confirm('Confirm status update?')) return;
    try {
        await request(`/api/pro/bookings/${bookingId}/status`, {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
            body: JSON.stringify({ status })
        });
        if (window.showToast) window.showToast('Job status updated!', 'success');
        window.loadProSchedule();
    } catch(err) {
        if (window.showToast) window.showToast('Failed to update status', 'error');
    }
};

// ─── Auto-init ──────────────────────────────────────────────────
if (document.getElementById('welcome-text')) {
    initDashboard();
}
