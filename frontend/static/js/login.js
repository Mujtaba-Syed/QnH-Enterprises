// Login form functionality
function togglePassword() {
  const passwordField = document.getElementById('password');
  const passwordIcon = document.getElementById('passwordIcon');
  
  if (passwordField.type === 'password') {
    passwordField.type = 'text';
    passwordIcon.classList.remove('bi-eye');
    passwordIcon.classList.add('bi-eye-slash');
  } else {
    passwordField.type = 'password';
    passwordIcon.classList.remove('bi-eye-slash');
    passwordIcon.classList.add('bi-eye');
  }
}

// Initialize login functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('loginForm');
  const googleLoginBtn = document.getElementById('googleLoginBtn');
  
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = form.username.value;
      const password = form.password.value;

      const res = await fetch('/accounts/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();
      console.log('Login response:', data);
      console.log('Response status:', res.status);
      
      if (res.ok) {
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);
        if (window.notificationManager) {
          window.notificationManager.success('Login successful!');
        } else {
          alert('Login successful!');
        }
        window.location.href = '/';  
      } else {
        // Handle different types of error responses
        let errorMessage = 'Login failed';
        
        if (data.detail) {
          errorMessage = data.detail;
        } else if (data.non_field_errors && data.non_field_errors.length > 0) {
          errorMessage = data.non_field_errors[0];
        } else if (data.username && data.username.length > 0) {
          errorMessage = data.username[0];
        } else if (data.password && data.password.length > 0) {
          errorMessage = data.password[0];
        } else if (typeof data === 'string') {
          errorMessage = data;
        }
        
        console.log('Error message:', errorMessage);
        console.log('Notification manager available:', !!window.notificationManager);
        
        if (window.notificationManager) {
          window.notificationManager.error(errorMessage);
          // Add delay before redirect so notification can be shown
          setTimeout(() => {
            window.location.href = '/login/';
          }, 3000);
        } else {
          alert(errorMessage);
          window.location.href = '/login/';
        }
      }
    });
  }

  // Google OAuth Login
  if (googleLoginBtn) {
    googleLoginBtn.addEventListener('click', async () => {
      try {
        // Get the Google OAuth URL
        const response = await fetch('/accounts/google-oauth-initiate/');
        const data = await response.json();
        
        if (response.ok) {
          // Redirect to Google OAuth
          window.location.href = data.auth_url;
        } else {
          alert('Failed to initiate Google login');
        }
      } catch (error) {
        console.error('Google login error:', error);
        alert('Failed to initiate Google login');
      }
    });
  }
}); 