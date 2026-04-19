import { getProfile, getAddresses, createBooking } from '../services/userService.js';
import { createPaymentOrder } from '../services/walletService.js';
import { request } from '../services/apiClient.js';

let allAddresses = [];
let ACTIVE_RAZORPAY_KEY = null;

export async function initBooking() {
  const token = localStorage.getItem('token');
  const params = new URLSearchParams(window.location.search);
  
  // 1. Fetch System Configuration & Key
  try {
    const config = await request('/api/public/config');
    if (config.razorpay_key_id && config.razorpay_key_id !== "NOT_CONFIGURED") {
        ACTIVE_RAZORPAY_KEY = config.razorpay_key_id;
    } else {
        throw new Error("Missing Key");
    }
  } catch (e) {
    console.error("Payment system config failed:", e);
    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Payment System Unavailable";
        submitBtn.style.background = "#94a3b8";
        submitBtn.style.cursor = "not-allowed";
    }
    if (window.showToast) window.showToast('Payment system is undergoing maintenance. Please try again later.', 'error');
  }
  
  // 1. Hydrate Summary immediately from URL
  const serviceName = params.get('service') || 'Selected Service';
  const servicePrice = params.get('price') || '0';
  const serviceTier = params.get('tier') || 'Standard';

  if (document.getElementById('summary-service')) document.getElementById('summary-service').textContent = serviceName;
  if (document.getElementById('summary-tier')) document.getElementById('summary-tier').textContent = serviceTier;
  if (document.getElementById('summary-total')) document.getElementById('summary-total').textContent = `₹${Number(servicePrice).toLocaleString('en-IN')}`;

  // 2. Auth Check
  if (!token) {
    window.location.href = `login.html?next=${encodeURIComponent(window.location.href)}`;
    return;
  }

  // 3. Define Slot Management logic BEFORE calling UI generators
  const slots = document.querySelectorAll('.slot-pill');
  const updateAvailableSlots = () => {
    const today = new Date();
    const todayStr = today.toLocaleDateString('en-CA'); // YYYY-MM-DD local
    const selectedDate = document.getElementById('b-date').value;
    const isToday = selectedDate === todayStr;
    const currentHour = today.getHours();

    slots.forEach(slot => {
      const slotTimeText = slot.dataset.time; // e.g. "09:00 AM"
      let slotHour = parseInt(slotTimeText.split(':')[0]);
      
      // Convert to 24h format for comparison
      if (slotTimeText.includes('PM') && slotHour !== 12) slotHour += 12;
      if (slotTimeText.includes('AM') && slotHour === 12) slotHour = 0;

      if (isToday && slotHour <= currentHour) {
          slot.classList.add('disabled');
          slot.style.opacity = '0.3';
          slot.style.filter = 'grayscale(1)';
          slot.style.pointerEvents = 'none';
          slot.classList.remove('active');
      } else {
          slot.classList.remove('disabled');
          slot.style.opacity = '1';
          slot.style.filter = 'none';
          slot.style.pointerEvents = 'auto';
      }
    });

    const activeSlot = Array.from(slots).find(s => s.classList.contains('active') && !s.classList.contains('disabled'));
    if (!activeSlot) {
        const firstAvailable = Array.from(slots).find(s => !s.classList.contains('disabled'));
        if (firstAvailable) firstAvailable.click();
    }
  };
  window.updateAvailableSlots = updateAvailableSlots;

  // 4. Load User Data & Addresses
  try {
    const user = await getProfile();
    allAddresses = await getAddresses();
    if (user.full_name) document.getElementById('b-name').value = user.full_name;
    if (user.phone)     document.getElementById('b-phone').value = user.phone.replace(/^\+91\s?/, '');

    const selector = document.getElementById('address-selector');
    if (selector) {
        while (selector.options.length > 1) selector.remove(1);
        allAddresses.forEach(addr => {
            const opt = document.createElement('option');
            opt.value = addr.id;
            opt.textContent = `${addr.label || 'Home'} - ${addr.line1}`;
            selector.appendChild(opt);
        });

        selector.addEventListener('change', (e) => {
            if (e.target.value === 'new') {
                clearAddressFields();
            } else {
                const found = allAddresses.find(a => a.id === e.target.value);
                if (found) fillAddressFields(found);
            }
        });

        const def = allAddresses.find(a => a.is_default) || allAddresses[0];
        if (def) {
            fillAddressFields(def);
            selector.value = def.id;
        }
    }
  } catch (error) { console.error('Data init error:', error); }

  // 5. Initialize UI Components
  generateDatePills();
  
  slots.forEach(slot => {
    slot.addEventListener('click', () => {
      if (slot.classList.contains('disabled')) return;
      slots.forEach(s => s.classList.remove('active'));
      slot.classList.add('active');
      const timeInp = document.getElementById('b-time');
      if (timeInp) timeInp.value = slot.dataset.time;
    });
  });

  const pinInput = document.getElementById('addr-zip');
  if (pinInput) pinInput.addEventListener('input', handlePincode);

  const giftToggle = document.getElementById('b-different-person');
  if (giftToggle) {
    giftToggle.addEventListener('change', (e) => {
      if (e.target.checked) {
        document.getElementById('b-name').value = "";
        document.getElementById('b-phone').value = "";
      } else {
        getProfile().then(u => {
          document.getElementById('b-name').value = u.full_name || "";
          document.getElementById('b-phone').value = (u.phone || "").replace(/^\+91\s?/, "");
        });
      }
    });
  }

  const form = document.getElementById('booking-form');
  if (form) form.addEventListener('submit', handleBookingSubmit);
}

function generateDatePills() {
    const container = document.getElementById('date-scroll-container');
    const dateInput = document.getElementById('b-date');
    if (!container) return;

    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    for (let i = 0; i < 7; i++) {
        const d = new Date();
        d.setDate(d.getDate() + i);
        const dateStr = d.toLocaleDateString('en-CA');
        const dayName = i === 0 ? 'Today' : i === 1 ? 'Tomorrow' : days[d.getDay()];
        const dayDate = d.getDate();
        const monthName = months[d.getMonth()];

        const pill = document.createElement('div');
        pill.className = 'date-pill' + (i === 0 ? ' active' : '');
        pill.innerHTML = `<span class="day">${dayName}</span><span class="num">${dayDate} ${monthName}</span>`;
        
        pill.addEventListener('click', () => {
            document.querySelectorAll('.date-pill').forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            dateInput.value = dateStr;
            if (window.updateAvailableSlots) window.updateAvailableSlots();
        });

        container.appendChild(pill);
        if (i === 0) dateInput.value = dateStr;
    }
    if (window.updateAvailableSlots) window.updateAvailableSlots();
}

function fillAddressFields(addr) {
    if (!addr) return;
    const line = addr.line1 || "";
    const parts = line.split(', ');
    document.getElementById('addr-line1').value = parts[0] || "";
    if (parts.length === 3) {
        document.getElementById('addr-landmark').value = parts[1] || "";
        document.getElementById('addr-area').value = parts[2] || "";
    } else {
        document.getElementById('addr-landmark').value = "";
        document.getElementById('addr-area').value = parts.slice(1).join(', ') || "";
    }
    document.getElementById('addr-city').value = addr.city || "";
    document.getElementById('addr-zip').value = addr.zipcode || "";
    if (window.updateAvailableSlots) window.updateAvailableSlots();
}

function clearAddressFields() {
    ['addr-line1', 'addr-landmark', 'addr-area', 'addr-zip', 'addr-city'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = "";
    });
}

async function handlePincode(e) {
    const pin = e.target.value.trim();
    if (pin.length === 6 && /^\d+$/.test(pin)) {
        const cityInp = document.getElementById('addr-city');
        if (cityInp) {
            cityInp.placeholder = "Searching...";
            try {
                const res = await fetch(`https://api.postalpincode.in/pincode/${pin}`);
                const data = await res.json();
                if (data[0] && data[0].Status === "Success") {
                    const info = data[0].PostOffice[0];
                    cityInp.value = info.State === "Karnataka" && info.District === "Bangalore" ? "Bengaluru" : info.District;
                }
            } catch(err) { console.error(err); }
        }
    }
}

async function handleBookingSubmit(e) {
  e.preventDefault();
  
  const hno = document.getElementById('addr-line1').value.trim();
  const area = document.getElementById('addr-area').value.trim();
  const city = document.getElementById('addr-city').value.trim();
  const zip = document.getElementById('addr-zip').value.trim();
  const date = document.getElementById('b-date').value;
  const time = document.getElementById('b-time').value;

  if (!hno || !area || !date || !time) {
      if (window.showToast) window.showToast('Please select a valid date/time and address.', 'error');
      return;
  }

  const submitBtn = document.getElementById('submit-btn');
  const params = new URLSearchParams(window.location.search);
  const price = parseFloat(params.get('price') || '0');
  const serviceName = params.get('service') || 'Service';

  submitBtn.textContent = 'Preparing Payment...';
  submitBtn.disabled = true;

  try {
    // 2. Create Razorpay Order via Backend
    const orderData = await createPaymentOrder(price);
    
    // 3. Configure Razorpay Options
    const options = {
      key: ACTIVE_RAZORPAY_KEY,
      amount: orderData.amount, // in paise
      currency: "INR",
      name: "Snappito",
      description: `Payment for ${serviceName}`,
      order_id: orderData.id,
      handler: async function (response) {
        if (window.showToast) window.showToast('Payment Successful! Finalizing booking...', 'info');
        
        try {
          const fullAddress = `${hno}, ${area}, ${city} - ${zip}`;
          const payload = {
            service_id: params.get('service_id'),
            scheduled_time: `${date}T${time.slice(0,5)}:00`,
            address: fullAddress,
            instructions: `Contact: ${document.getElementById('b-name').value} (+91 ${document.getElementById('b-phone').value})`,
            payment_info: {
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_order_id: response.razorpay_order_id,
              razorpay_signature: response.razorpay_signature
            }
          };

          await createBooking(payload);
          if (window.showToast) window.showToast('🎉 Booking Confirmed!', 'success');
          setTimeout(() => { window.location.href = 'dashboard.html'; }, 1500);
        } catch (err) {
          if (window.showToast) window.showToast('Booking failed after payment. Support alerted.', 'error');
          console.error(err);
        }
      },
      prefill: {
        name: document.getElementById('b-name').value,
        contact: document.getElementById('b-phone').value
      },
      theme: { color: "#10b981" },
      modal: {
        ondismiss: function() {
          submitBtn.textContent = 'Confirm & Pay';
          submitBtn.disabled = false;
        }
      }
    };

    const rzp = new window.Razorpay(options);
    rzp.open();

  } catch (error) {
    if (window.showToast) window.showToast(error.message || 'Error initiating payment', 'error');
    submitBtn.textContent = 'Confirm & Pay';
    submitBtn.disabled = false;
  }
}

initBooking();
