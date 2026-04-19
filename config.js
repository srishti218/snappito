const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:5001'
  : ''; 

const RAZORPAY_KEY_ID = "YOUR_RAZORPAY_KEY_ID"; // Replace with your test key from Razorpay Dashboard

export { API_BASE_URL, RAZORPAY_KEY_ID };
