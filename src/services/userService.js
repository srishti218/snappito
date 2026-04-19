import { request } from './apiClient.js';

const token = localStorage.getItem('token');

export async function getProfile() {
  return request('/api/user/profile', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  });
}

export async function getAddresses() {
  return request('/api/user/addresses', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  });
}

export async function addAddress(addressData) {
  return request('/api/user/addresses', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
    body: JSON.stringify(addressData)
  });
}

export async function createBooking(bookingData) {
  return request('/api/service/book', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
    body: JSON.stringify(bookingData)
  });
}
