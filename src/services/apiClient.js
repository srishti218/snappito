export const API_BASE_URL = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://127.0.0.1:5001'
  : '';

// Replace hardcoded key with environment value or placeholder
export const RAZORPAY_KEY_ID = "YOUR_RAZORPAY_KEY_ID"; // Set this in your environment or local config

/**
 * Standard fetch wrapper for Snappito services.
 */
export async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 403) {
        console.warn("Security Violation or Session Expired. Clearing session.");
        localStorage.clear();
        window.location.href = 'login.html';
    }
    const error = await response.json().catch(() => ({ error: 'Network response was not ok' }));
    throw new Error(error.error || 'Request failed');
  }

  return response.json();
}
