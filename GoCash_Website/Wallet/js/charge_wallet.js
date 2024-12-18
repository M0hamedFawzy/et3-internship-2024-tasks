// charge_wallet.js

document.addEventListener('DOMContentLoaded', () => {
    const chargeForm = document.getElementById('charge-wallet-form');
    const messageContainer = document.getElementById('message-container');
    const chargeButton = document.querySelector('button[type="submit"]');

    const token = getAuthToken();

    if (!token) {
        displayMessage('User not authenticated. Please log in.', 'error');
        // Optionally, redirect to login page
        window.location.href = 'login.html';
        return;
    }

    // Function to fetch wallet data and check if it's active
    async function checkWalletStatus() {
        try {
            const response = await fetch('http://127.0.0.1:8000/wallets/', {
                method: 'GET',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (response.ok) {
                if (!data.is_active) {
                    displayMessage('Your wallet is inactive and cannot perform any actions.', 'error');
                    disableForm();
                }
                // If active, no action needed
            } else {
                if (response.status === 404) {
                    displayMessage('No wallet found. Please create a wallet first.', 'error');
                    disableForm();
                } else {
                    const errorMsg = data.detail || Object.values(data).join(' ');
                    displayMessage(`Error: ${errorMsg}`, 'error');
                    disableForm();
                }
            }
        } catch (error) {
            console.error('Error fetching wallet status:', error);
            displayMessage('An error occurred while checking wallet status.', 'error');
            disableForm();
        }
    }

    // Function to disable the charge form
    function disableForm() {
        chargeForm.querySelectorAll('input, select, button').forEach(element => {
            element.disabled = true;
        });
    }

    // Function to display messages
    function displayMessage(message, type) {
        // Clear previous messages
        messageContainer.innerHTML = '';

        const div = document.createElement('div');
        div.classList.add('message');
        div.classList.add(type === 'success' ? 'success' : 'error');
        div.textContent = message;
        messageContainer.appendChild(div);
    }

    // Utility function to get Auth Token (Assuming token is stored in localStorage)
    function getAuthToken() {
        return localStorage.getItem('authToken') || '';
    }

    // Initial check on page load
    checkWalletStatus();

    // Handle Charge Wallet Form Submission
    chargeForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Clear previous messages
        messageContainer.innerHTML = '';

        // Retrieve form data
        const amount = document.getElementById('amount').value;
        const paymentMethod = document.getElementById('payment_method').value;

        // Basic client-side validation
        if (amount <= 0) {
            displayMessage('Amount must be greater than zero.', 'error');
            return;
        }

        if (!paymentMethod) {
            displayMessage('Please select a payment method.', 'error');
            return;
        }

        // Prepare payload
        const payload = {
            amount: parseFloat(amount),
            payment_method: paymentMethod
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/wallets/charge_wallet/', { // Adjust the URL if needed
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                displayMessage(data.success, 'success');
                // Optionally, reset the form
                chargeForm.reset();
            } else {
                // Handle specific error messages
                const errorMsg = data.detail || Object.values(data).join(' ');
                displayMessage(`Error: ${errorMsg}`, 'error');
            }
        } catch (error) {
            console.error('Error charging wallet:', error);
            displayMessage('An error occurred while charging the wallet.', 'error');
        }
    });
});
