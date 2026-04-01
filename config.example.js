// Template for config.js
// Copy this file to config.js and update with your actual values

const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:5000'
  : 'https://api.yourdomain.com'; // TODO: Replace this with your actual AWS backend URL
