import { getProfile, createBooking } from '../services/userService.js';

export async function initBooking() {
  const token = localStorage.getItem('token');
  const params = new URLSearchParams(window.location.search);
  
  const serviceId = params.get('service_id') || '';
  const serviceName = params.get('service') || 'Selected Service';
  const servicePrice = params.get('price') || '0';
  const serviceTier = params.get('tier') || 'Standard';

  // ─── Hydrate Summary ───────────────────────────────────────────
  const summaryService = document.getElementById('summary-service');
  const summaryTier = document.getElementById('summary-tier');
  const summaryTotal = document.getElementById('summary-total');

  if (summaryService) summaryService.textContent = serviceName;
  if (summaryTier) summaryTier.textContent = serviceTier;
  if (summaryTotal) summaryTotal.textContent = `₹${Number(servicePrice).toLocaleString('en-IN')}`;

  // ─── Time Slot Selection Logic ────────────────────────────────
  const slots = document.querySelectorAll('.slot-pill');
  const timeInput = document.getElementById('b-time');
  
  slots.forEach(slot => {
    slot.addEventListener('click', () => {
      slots.forEach(s => s.classList.remove('active'));
      slot.classList.add('active');
      if (timeInput) timeInput.value = slot.dataset.time;
    });
  });

  // ─── User Profile & Auth Check ────────────────────────────────
  if (!token) {
    const returnUrl = encodeURIComponent(window.location.href);
    window.location.href = `login.html?next=${returnUrl}`;
    return;
  }

  try {
    const user = await getProfile();
    if (user.full_name) document.getElementById('b-name').value = user.full_name;
    if (user.phone)     document.getElementById('b-phone').value = user.phone.replace(/^\+91\s?/, '');
  } catch (error) {
    console.error('Profile fetch failed:', error);
  }

  // ─── Form Submission ──────────────────────────────────────────
  const form = document.getElementById('booking-form');
  if (form) form.addEventListener('submit', handleBookingSubmit);
}

async function handleBookingSubmit(e) {
  e.preventDefault();
  const submitBtn = document.getElementById('submit-btn');
  const params = new URLSearchParams(window.location.search);
  const serviceId = params.get('service_id');

  const name = document.getElementById('b-name').value.trim();
  const phone = document.getElementById('b-phone').value.trim();
  const address = document.getElementById('b-address-text').value.trim();
  const date = document.getElementById('b-date').value;
  const time = document.getElementById('b-time').value;

  if (!name || !phone || !address || !date || !time) {
    if (window.showToast) window.showToast('Please fill all required fields.', 'error');
    return;
  }

  submitBtn.textContent = 'Processing Payment…';
  submitBtn.disabled = true;

  try {
    await createBooking({
      service_id: serviceId,
      scheduled_time: `${date}T${time.slice(0,5)}:00`, // Simple parse
      address: address,
      instructions: `Booked by ${name}. Phone: ${phone}`
    });

    if (window.showToast) window.showToast('🎉 Booking Confirmed!', 'success');
    
    setTimeout(() => {
      window.location.href = 'dashboard.html';
    }, 1800);

  } catch (error) {
    console.error('Booking Error:', error);
    if (window.showToast) window.showToast(error.message || 'Booking failed. Try again.', 'error');
    submitBtn.textContent = 'Confirm & Pay';
    submitBtn.disabled = false;
  }
}

// Auto-init
if (document.getElementById('booking-form')) {
  initBooking();
}
