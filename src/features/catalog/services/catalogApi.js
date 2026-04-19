import { request } from '../../../services/apiClient.js';

/**
 * Fetches all service categories and their nested services.
 */
export async function getCategories() {
  return request('/api/services');
}

/**
 * Performs a search query against the service catalog.
 * @param {string} query 
 */
export async function searchServices(query) {
  return request(`/api/search?q=${encodeURIComponent(query)}`);
}
