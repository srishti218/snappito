import { login, signup, forgotPassword } from '../services/authService.js';
// Assuming Toast is in globals now or using the toast.js module
// If toast is a global, we just use showToast

export function initAuth() {
  const loginForm = document.getElementById('loginForm');
  const signupForm = document.getElementById('signupForm');
  const forgotForm = document.getElementById('forgotForm');

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      btn.textContent = 'Logging in...';
      btn.disabled = true;

      try {
        const data = await login(
          document.getElementById('email').value,
          document.getElementById('password').value
        );
        localStorage.setItem('token', data.token);
        if (window.showToast) window.showToast('Login successful! Redirecting...', 'success');
        setTimeout(() => window.location.href = 'dashboard.html', 1500);
      } catch (error) {
        if (window.showToast) window.showToast(error.message || 'Login failed.', 'error');
        btn.textContent = 'Log In';
        btn.disabled = false;
      }
    });
  }

  if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      btn.textContent = 'Creating account...';
      btn.disabled = true;
      
      const payload = {
        full_name: document.getElementById('fullname')?.value || '',
        email:     document.getElementById('email')?.value || '',
        password:  document.getElementById('password')?.value || '',
        phone:     document.getElementById('phone')?.value || ''
      };

      try {
        await signup(payload);
        if (window.showToast) window.showToast('Account created! Please log in.', 'success');
        setTimeout(() => window.location.href = 'login.html', 1500);
      } catch (error) {
        if (window.showToast) window.showToast(error.message || 'Signup failed.', 'error');
        btn.textContent = 'Sign Up';
        btn.disabled = false;
      }
    });
  }

  if (forgotForm) {
    forgotForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btn = document.getElementById('forgotBtn');
        const input = document.getElementById('forgotInput').value;
        btn.textContent = 'Sending...';
        btn.disabled = true;

        try {
            const payload = input.includes('@') ? { email: input } : { phone_number: input };
            await forgotPassword(payload);
            if (window.showToast) window.showToast('Password reset instructions sent!', 'success');
            if (window.toggleForgotModal) window.toggleForgotModal(false);
        } catch (error) {
            if (window.showToast) window.showToast(error.message || 'Failed to send reset link.', 'error');
        }
        btn.textContent = 'Send Reset Link';
        btn.disabled = false;
    });
  }
}

// Auto-init
if (document.getElementById('loginForm') || document.getElementById('signupForm')) {
  initAuth();
}
