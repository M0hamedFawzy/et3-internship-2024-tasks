// js/signin.js

document.addEventListener('DOMContentLoaded', () => {
    const signinForm = document.getElementById('signin-form');
    const messageBox = document.getElementById('message-box');

    signinForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        const phone = document.getElementById('phone').value;

        // Simple validation (optional)
        if (!phone) {
            displayMessage('Please enter your phone number.', 'error');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/sign_in/', { // Update the API endpoint as needed
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Include CSRF token if your backend requires it
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ phone_number: phone }),
            });

            console.log(response);
            if (response.ok) {
                const data = await response.json();
                console.log('Success:', data);

                 // Check for token in response
                 let token = data.user.token;
                 console.log('Extracted Token:', token);
 
                 if (token) {
                     localStorage.setItem('authToken', token);  // Store token with the key 'authToken'
                     console.log('Token stored in localStorage under key "authToken".');
                 } else {
                     console.error('Token not found in the response.');
                     displayMessage('Sign in failed. Token not found.', 'error');
                     return;
                 }

                displayMessage('Sign in successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = 'Dashboard/dashboard.html';
                }, 500);
            } else {
                const errorData = await response.json();
                console.log('Error:', errorData); // Log error
                displayMessage(errorData.error || 'Sign in failed.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            displayMessage('An error occurred. Please try again.', 'error');
        }
    });

    function displayMessage(message, type) {
        messageBox.textContent = message;
        messageBox.className = type; // You can style messages based on type
    }

    // Optional: Function to get CSRF token from cookies if needed
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
});
