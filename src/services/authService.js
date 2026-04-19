import { request } from './apiClient.js';

export async function login(email, password) {
  return request('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  });
}

export async function signup(userData) {
  return request('/api/auth/signup', {
    method: 'POST',
    body: JSON.stringify(userData)
  });
}

export async function forgotPassword(payload) {
  return request('/api/auth/forgot-password', {
    method: 'POST',
    body: JSON.stringify(payload)
  });
}
