// send_money.js

// Replace with your actual token retrieval method
const token = localStorage.getItem('authToken'); // Ensure you securely obtain and store the token

// Function to display messages
function displayMessage(message, type) {
    const messageContainer = document.getElementById('message-container');
    // Clear previous messages
    messageContainer.innerHTML = '';

    const div = document.createElement('div');
    div.classList.add('message');
    div.classList.add(type === 'success' ? 'success' : 'error');
    div.textContent = message;
    messageContainer.appendChild(div);
}

// Function to disable the form
function disableForm() {
    const form = document.getElementById('send-money-form');
    form.querySelectorAll('input, button').forEach(element => {
        element.disabled = true;
    });
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

// Handle form submission
document.getElementById('send-money-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const receiverNumber = document.getElementById('receiver_number').value;
    const amount = document.getElementById('amount').value;

    try {
        const response = await fetch('http://127.0.0.1:8000/transactions/send_money/', {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                reciever_number: receiverNumber,
                amount: amount
            })
        });

        const data = await response.json();

        if (response.ok) {
            displayMessage(data.detail, 'success');
            // Optionally, reset the form
            document.getElementById('send-money-form').reset();
        } else {
            const errorMsg = data.detail || Object.values(data).join(' ');
            displayMessage(`Error: ${errorMsg}`, 'error');
        }
    } catch (error) {
        console.error('Error sending money:', error);
        displayMessage('An error occurred while sending money.', 'error');
    }
});

// Initial check on page load
document.addEventListener('DOMContentLoaded', checkWalletStatus);
