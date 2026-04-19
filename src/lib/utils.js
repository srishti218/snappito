/**
 * Escapes HTML characters to prevent XSS.
 * @param {string} str 
 * @returns {string}
 */
export function escHtml(str) {
  if (!str) return '';
  const d = document.createElement('div');
  d.appendChild(document.createTextNode(str));
  return d.innerHTML;
}

/**
 * Converts a string to a URL-friendly slug.
 * @param {string} text 
 * @returns {string}
 */
export function toSlug(text) {
  return text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/[\s-]+/g, '-').replace(/^-+|-+$/g, '');
}

/**
 * Formats a number as Indian Rupee currency.
 * @param {number} amount 
 * @returns {string}
 */
export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(amount);
}
