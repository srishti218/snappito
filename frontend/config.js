// Use localhost for development, otherwise provide the production URL
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:5000'
  : ''; // Use empty string for production reverse proxy (routes already start with /api)

