function logout() {
  fetch('/logout', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(response => {
      if (response.ok) {
          console.log('Logout successful');
          window.location.href = 'welcome.html'; // Redirect to welcome page after logout
      } else {
          console.error('Logout failed');
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}
