// js/withdrawal.js

document.addEventListener('DOMContentLoaded', () => {
    const withdrawalForm = document.getElementById('withdrawal-form');
    const token = localStorage.getItem('authToken');

    const form = document.getElementById('withdrawal-form');
    const messageContainer = document.getElementById('message-container');
    const amountInput = document.getElementById('amount');
    const paymentMethodSelect = document.getElementById('payment_method');
    const confirmButton = form.querySelector('button[type="submit"]');

    // Replace 'YOUR_AUTH_TOKEN' with the actual token
    const AUTH_TOKEN = token;

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
        withdrawalForm.querySelectorAll('input, select, button').forEach(element => {
            element.disabled = true;
        });
    }

    // Initial check on page load
    checkWalletStatus();


    // Function to handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the default form submission

        // Clear previous messages
        messageContainer.innerHTML = '';

        const paymentMethod = paymentMethodSelect.value;
        const amount = parseFloat(amountInput.value);

        // Validate input
        if (isNaN(amount) || amount <= 0) {
            displayMessage('Please enter a valid amount.', 'error');
            return;
        }

        // Prepare the data
        const data = {
            amount: amount,
            payment_method: paymentMethod
        };

        try {
            const response = await fetch('http://localhost:8000/transactions/withdrawal/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${AUTH_TOKEN}`
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                displayMessage(result.detail, 'success');
                // Optionally, reset the form
                form.reset();
            } else {
                if (result.detail.includes('activate your wallet')) {
                    displayMessage(result.detail, 'error');
                    // Disable the amount input and payment method select
                    amountInput.disabled = true;
                    paymentMethodSelect.disabled = true;
                    confirmButton.disabled = true;
                } else {
                    displayMessage(result.detail, 'error');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            displayMessage('An unexpected error occurred. Please try again later.', 'error');
        }
    });
});
