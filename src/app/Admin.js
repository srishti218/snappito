import { request } from '../services/apiClient.js';

let serviceChart, timeChart;

export async function initAdmin() {
  const token = localStorage.getItem('token');
  if (!token) { window.location.href = 'login.html'; return; }

  // Restrict professional/customer from admin page
  const role = localStorage.getItem('user_role');
  if (role !== 'admin') {
      window.location.href = 'dashboard.html';
      return;
  }

  try {
      initCharts();
      await loadDashboardData();
  } catch(e) {
      console.error("Admin Load Error:", e);
      // Backend Role Enforcement: Handle 403 Forbidden
      if (e.message?.includes('403') || String(e).includes('403') || e.status === 403) {
          if (window.showToast) window.showToast("Unauthorized: Admin Access Required.", "error");
          localStorage.clear(); // Security Trap Door
          setTimeout(() => window.location.href = 'login.html', 2000);
      } else {
          if (window.showToast) window.showToast("Critical Error loading records.", "error");
      }
  }

  // Setup Navigation
  document.querySelectorAll('.nav-item[data-target]').forEach(item => {
      item.addEventListener('click', (e) => {
          document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
          e.currentTarget.classList.add('active');
          
          document.querySelectorAll('.section-view').forEach(s => s.classList.remove('active'));
          const target = e.currentTarget.dataset.target;
          document.getElementById('section-' + target).classList.add('active');

          // Trigger specific loaders
          if (target === 'pros') loadFleetData();
          if (target === 'services') loadCatalogueData();
      });
  });
}

function initCharts() {
    const ctxS = document.getElementById('serviceChart').getContext('2d');
    serviceChart = new Chart(ctxS, {
        type: 'doughnut',
        data: { labels: [], datasets: [{ data: [], backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6'] }] },
        options: { 
            responsive: true, 
            maintainAspectRatio: true, 
            aspectRatio: 2,
            plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } } } 
        }
    });

    const ctxT = document.getElementById('timeChart').getContext('2d');
    timeChart = new Chart(ctxT, {
        type: 'line',
        data: { labels: [], datasets: [{ label: 'Booking Density', data: [], borderColor: '#3b82f6', tension: 0.4, fill: true, backgroundColor: 'rgba(59, 130, 246, 0.1)' }] },
        options: { 
            responsive: true, 
            maintainAspectRatio: true, 
            aspectRatio: 2,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        }
    });
}

async function loadDashboardData() {
    await loadRevenueAndAnalytics();
    await loadJobs();
    await loadMetics();
}

async function loadMetics() {
    try {
        const pros = await request('/api/admin/professionals/search', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        document.getElementById('total-pros').textContent = pros.length;
    } catch(e) {}
}

async function loadRevenueAndAnalytics() {
    try {
        const data = await request('/api/admin/revenue', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        
        document.getElementById('total-net').textContent = `₹${data.total_snappito_revenue.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
        
        const tbody = document.getElementById('txn-tbody');
        if (data.transactions.length === 0) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No logs available.</td></tr>`;
            return;
        }

        tbody.innerHTML = data.transactions.map(t => `
            <tr>
                <td style="font-family: monospace; color: var(--text-muted); font-size: 11px;">#${t.transaction_id.substring(0,10)}</td>
                <td style="font-size: 13px;">${new Date(t.created_at).toLocaleString([], {dateStyle: 'medium', timeStyle: 'short'})}</td>
                <td style="font-weight: 600;">₹${t.amount}</td>
                <td style="color: var(--primary); font-weight: 800;">₹${t.snappito_revenue}</td>
                <td style="color: #6366f1;">₹${t.pro_payout}</td>
            </tr>
        `).join('');

        // Update Charts
        updateAnalyticsCharts(data.transactions);

    } catch(err) {
        console.error("Load Revenue fail:", err);
    }
}

function updateAnalyticsCharts(txns) {
    // 1. Service Popularity (assuming we have description or similar, or mock for demo if text unavailable)
    // Actually our backend doesn't return service details in txn yet, let's derive from descriptions
    const serviceCounts = {};
    txns.forEach(t => {
        const match = t.description.match(/Booking /); // Simple filter
        if(match) {
            const label = "Standard Service"; // Real implementation would use service_name
            serviceCounts[label] = (serviceCounts[label] || 0) + 1;
        }
    });

    serviceChart.data.labels = Object.keys(serviceCounts).length ? Object.keys(serviceCounts) : ['Cleaning', 'Plumbing', 'Electrical'];
    serviceChart.data.datasets[0].data = Object.keys(serviceCounts).length ? Object.values(serviceCounts) : [12, 19, 7];
    serviceChart.update();

    // 2. Peak Hours
    const hours = new Array(24).fill(0);
    txns.forEach(t => {
        const h = new Date(t.created_at).getHours();
        hours[h]++;
    });
    
    timeChart.data.labels = hours.map((_, i) => `${i}:00`);
    timeChart.data.datasets[0].data = hours;
    timeChart.update();
}

async function loadJobs() {
    try {
        const bookings = await request('/api/admin/bookings', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });

        const tbody = document.getElementById('jobs-tbody');
        const todayStr = new Date().toLocaleDateString();

        // 1. Update Real-Time Metrics
        const activeCount = bookings.filter(b => !['completed', 'canceled'].includes(b.status)).length;
        const enRouteCount = bookings.filter(b => b.status === 'en-route').length;
        const completedToday = bookings.filter(b => b.status === 'completed' && new Date(b.scheduled_time).toLocaleDateString() === todayStr).length;

        document.getElementById('total-active').textContent = activeCount;
        document.getElementById('total-enroute').textContent = enRouteCount;
        document.getElementById('total-completed').textContent = completedToday;

        // 2. Render Live Job Board (ALL JOBS)
        tbody.innerHTML = bookings.map(b => {
            const isToday = new Date(b.scheduled_time).toLocaleDateString() === todayStr;
            
            // Status Pill Logic
            let pillColor = '#64748b'; // Default Grey
            let pillBg = '#f1f5f9';
            if (b.status === 'unassigned') { pillColor = '#ef4444'; pillBg = 'rgba(239, 68, 68, 0.1)'; }
            if (b.status === 'assigned') { pillColor = '#3b82f6'; pillBg = 'rgba(59, 130, 246, 0.1)'; }
            if (b.status === 'en-route') { pillColor = '#8b5cf6'; pillBg = 'rgba(139, 92, 246, 0.1)'; }
            if (b.status === 'started') { pillColor = '#f59e0b'; pillBg = 'rgba(245, 158, 11, 0.1)'; }
            if (b.status === 'completed') { pillColor = '#10b981'; pillBg = 'rgba(16, 185, 129, 0.1)'; }

            const statusLabel = b.status.toUpperCase().replace('-', ' ');
            const staffName = b.professional_name || (b.status === 'unassigned' ? '<span style="color:#ef4444; opacity:0.6;">MISSING</span>' : 'System');

            return `
                <tr style="${b.status === 'completed' ? 'opacity: 0.6;' : ''}">
                    <td style="font-family: monospace; font-weight: 700;">#${b.booking_id.substring(0,6).toUpperCase()}</td>
                    <td>
                        <div style="font-weight: 800;">${b.customer_name || 'Anonymous Meta'}</div>
                        <div style="font-size: 11px; color: var(--text-muted); opacity: 0.7;">Pincode: ${b.address?.split('-').pop().trim() || 'N/A'}</div>
                    </td>
                    <td style="font-size: 13px; font-weight: 600;">${b.service_name}</td>
                    <td style="font-size: 13px; font-weight: 700; color: var(--primary-dark);">${staffName}</td>
                    <td><span class="status-pill" style="font-size: 10px; background: ${pillBg}; color: ${pillColor}; border: 1px solid ${pillColor}44;">${statusLabel}</span></td>
                    <td>
                        <div style="font-weight: 700; color: ${isToday?'#ef4444':'var(--text-main)'}">${isToday?'TODAY':new Date(b.scheduled_time).toLocaleDateString([], {month:'short', day:'numeric'})}</div>
                        <div style="font-size: 11px; color: var(--text-muted);">${new Date(b.scheduled_time).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</div>
                    </td>
                    <td>
                        ${b.status === 'unassigned' ? 
                            `<button class="btn-sm btn-assign" onclick="window.initAssignFlow('${b.booking_id}', '${b.service_id}')">APPROVE & ASSIGN</button>` : 
                            `<span style="font-size: 11px; color: var(--text-muted);">LOCKED</span>`
                        }
                    </td>
                </tr>
            `;
        }).join('');
    } catch(err) {
        console.error("Load Jobs fail:", err);
    }
}

window.initAssignFlow = async (bookingId, serviceId) => {
    if (window.showToast) window.showToast('Opening Fleet Selector...', 'info');
    
    try {
       const pros = await request('/api/admin/professionals/search', {
           headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
       });
       
       if(pros.length === 0) {
           alert("No active professionals found in system.");
           return;
       }
       
       const proStr = pros.map((p, i) => `${i+1}. ${p.full_name} [${p.experience}yrs]`).join('\n');
       const selection = prompt(`SELECT COMMAND STAFF (MANUAL SELECTION):\n${proStr}`);
       
       if (selection && !isNaN(selection) && parseInt(selection) > 0 && parseInt(selection) <= pros.length) {
           const selectedPro = pros[parseInt(selection)-1];
           
           await request(`/api/admin/bookings/${bookingId}/assign`, {
               method: 'PUT',
               headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
               body: JSON.stringify({ professional_id: selectedPro.user_id })
           });
           
           if(window.showToast) window.showToast(`Command Issued: ${selectedPro.full_name} assigned.`, 'success');
           loadDashboardData();
       }

    } catch(e) {
       console.error(e);
       if(window.showToast) window.showToast('Deployment assignment failed.', 'error');
    }
};

window.loadFleetData = async () => {
    const wrap = document.getElementById('pros-table-wrap');
    wrap.innerHTML = '<div style="padding: 20px;">Fetching recruitment data...</div>';

    try {
        const pros = await request('/api/admin/professionals/search', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });

        if (pros.length === 0) {
            wrap.innerHTML = '<div style="padding: 40px;">No professionals onboarded yet.</div>';
            return;
        }

        wrap.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Staff Name</th>
                        <th>Expertise</th>
                        <th>Contact</th>
                        <th>Experience</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${pros.map(p => `
                        <tr>
                            <td><div style="font-weight: 700;">${p.full_name}</div><div style="font-size: 11px; color: var(--text-muted);">ID: ${p.user_id.substring(0,8)}</div></td>
                            <td><span class="status-pill" style="background: #eff6ff; color: #3b82f6;">${p.category_name || 'Generalist'}</span></td>
                            <td><div style="font-size: 13px;">${p.phone || '+91-8747858018'}</div><div style="font-size: 11px; color: var(--primary);">Verified</div></td>
                            <td>${p.experience} Years</td>
                            <td><button class="btn-sm" style="background: #f8fafc; color: var(--text-main); border: 1px solid var(--border-light);">Edit Profile</button></td>
                        </tr>`).join('')}
                </tbody>
            </table>`;
    } catch (e) {
        wrap.innerHTML = '<div style="color: #ef4444; padding: 20px;">Failed to load fleet data.</div>';
    }
};

window.loadCatalogueData = async () => {
    const wrap = document.getElementById('services-table-wrap');
    wrap.innerHTML = '<div style="padding: 20px;">Synchronizing inventory...</div>';

    try {
        const data = await request('/api/services');
        const categories = data.categories || [];

        if (categories.length === 0) {
            wrap.innerHTML = '<div style="padding: 40px;">Service catalog is empty.</div>';
            return;
        }

        wrap.innerHTML = categories.map(cat => `
            <div style="margin-bottom: 30px; text-align: left;">
                <h4 style="margin-bottom: 15px; color: var(--primary-dark); font-size: 15px;">${cat.name} <small style="font-weight: normal; color: var(--text-muted);">(${cat.services.length} items)</small></h4>
                <div class="data-table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>Service Name</th>
                                <th>Base Price</th>
                                <th>Commission</th>
                                <th>Status</th>
                                <th>Mgmt</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${cat.services.map(s => `
                                <tr>
                                    <td style="font-weight: 600;">${s.name}</td>
                                    <td>₹${s.base_price}</td>
                                    <td style="color: var(--primary); font-weight: 700;">${s.commission_rate || 20}%</td>
                                    <td><span class="status-pill" style="background: #ecfdf5; color: var(--primary);">Active</span></td>
                                    <td><button class="btn-sm" style="background: #f1f5f9; color: var(--text-muted); cursor: not-allowed;" title="Premium Admin required">Modify</button></td>
                                </tr>`).join('')}
                        </tbody>
                    </table>
                </div>
            </div>`).join('');
    } catch (e) {
        wrap.innerHTML = '<div style="color: #ef4444; padding: 20px;">Failed to sync with catalog.</div>';
    }
};

window.openProModal = async () => {
    const modal = document.getElementById('pro-modal');
    modal.style.display = 'flex';
    
    // Fetch categories for dropdown
    const select = document.getElementById('pro-category');
    if (select.options.length <= 1) {
        try {
            const data = await request('/api/services');
            const categories = data.categories || [];
            categories.forEach(cat => {
                const opt = document.createElement('option');
                opt.value = cat.id;
                opt.textContent = cat.name;
                select.appendChild(opt);
            });
        } catch (e) {
            console.error("Failed to load categories for modal");
        }
    }
};

window.closeModal = (id) => {
    document.getElementById(id).style.display = 'none';
};

window.submitOnboarding = async () => {
    const password = document.getElementById('pro-password').value;
    
    // UI Validation: 6 char minimum
    if (password.length < 6) {
        if (window.showToast) window.showToast("Password must be at least 6 characters.", "error");
        return;
    }

    const payload = {
        full_name: document.getElementById('pro-name').value,
        email: document.getElementById('pro-email').value,
        phone: document.getElementById('pro-phone').value,
        category_id: document.getElementById('pro-category').value,
        experience: parseInt(document.getElementById('pro-exp').value),
        password: password
    };

    try {
        if (window.showToast) window.showToast("Onboarding staff...", "info");
        
        await request('/api/admin/professionals', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
            body: JSON.stringify(payload)
        });

        if (window.showToast) window.showToast("Staff onboarded successfully!", "success");
        
        // Clean UI on success
        window.closeModal('pro-modal');
        document.getElementById('proForm').reset();
        
        window.loadFleetData(); // Success Loop refresh
        
    } catch (e) {
        if (window.showToast) window.showToast("Onboarding failed: " + e.message, "error");
    }
};

window.logout = () => {
    localStorage.clear();
    window.location.href = 'index.html';
};

document.addEventListener('DOMContentLoaded', () => {
    initAdmin();
});
