// js/register.js

document.addEventListener('DOMContentLoaded', () => {
    const registrationForm = document.getElementById('registration-form');
    const messageBox = document.getElementById('message-box');

    registrationForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        const username = document.getElementById('username').value;
        const phone = document.getElementById('phone').value;

        // Simple validation (optional)
        if (!username || !phone) {
            displayMessage('Please fill in all fields.', 'error');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/register/', { // Update the API endpoint as needed
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // Include CSRF token if your backend requires it
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ username, phone_number: phone }),
            });

            console.log(response);
            if (response.ok) {
                const data = await response.json();
                console.log('Success:', data);
                displayMessage('Registration successful! Redirecting...', 'success');
                // Redirect to sign-in page after a short delay
                setTimeout(() => {
                    window.location.href = 'signin.html';
                }, 500);
            } else {
                const errorData = await response.json();
                console.log('Error:', errorData); // Log error
                displayMessage(errorData.error || 'Registration failed.', 'error');
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
