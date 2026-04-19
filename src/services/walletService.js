import { request } from './apiClient.js';

export async function getWalletBalance() {
  return request('/api/wallet', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  });
}

export async function getTransactions() {
  return request('/api/wallet/transactions', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
  });
}

export async function createPaymentOrder(amount) {
  return request('/api/payment/razorpay/create-order', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
    body: JSON.stringify({ amount: parseFloat(amount) })
  });
}

export async function verifyPayment(paymentData) {
  return request('/api/payment/razorpay/verify', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
    body: JSON.stringify(paymentData)
  });
}
