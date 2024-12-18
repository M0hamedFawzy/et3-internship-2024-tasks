// wallet.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('authToken'); // Ensure the token is stored under 'authToken'
    console.log('token here -->', token)
    if (!token) {
        // If no token is found, redirect to the login page
        window.location.href = '/signin.html';
    }

    const walletContent = document.getElementById('wallet-content');

    // Modals
    const createWalletModal = document.getElementById('create-wallet-modal');
    const activationModal = document.getElementById('activation-modal');
    const deleteWalletModal = document.getElementById('delete-wallet-modal');
    const restoreWalletModal = document.getElementById('restore-wallet-modal');
    const resetPasswordModal = document.getElementById('reset-password-modal');

    // Close buttons
    const closeCreateWallet = document.getElementById('close-create-wallet');
    const closeActivationModal = document.getElementById('close-activation-modal');
    const closeDeleteWallet = document.getElementById('close-delete-wallet');
    const closeRestoreWallet = document.getElementById('close-restore-wallet');
    const closeResetPassword = document.getElementById('close-reset-password');

    // Forms
    const createWalletForm = document.getElementById('create-wallet-form');
    const activationForm = document.getElementById('activation-form');
    const deleteWalletForm = document.getElementById('delete-wallet-form');
    const restoreWalletForm = document.getElementById('restore-wallet-form');
    const resetPasswordForm = document.getElementById('reset-password-form');

    // Buttons (to be dynamically created)
    let chargeButton, deactivateButton, deleteButton, restoreButton, createButton;

    // Fetch wallet data on page load
    fetchWalletData();

    // Event Listeners for closing modals
    closeCreateWallet.addEventListener('click', () => {
        createWalletModal.style.display = 'none';
    });

    closeActivationModal.addEventListener('click', () => {
        activationModal.style.display = 'none';
    });

    closeDeleteWallet.addEventListener('click', () => {
        deleteWalletModal.style.display = 'none';
    });

    closeRestoreWallet.addEventListener('click', () => {
        restoreWalletModal.style.display = 'none';
    });

    // Close Reset Password Modal
    closeResetPassword.addEventListener('click', () => {
        resetPasswordModal.style.display = 'none';
    });

    // Close modals when clicking outside the modal content
    window.onclick = function(event) {
        if (event.target == createWalletModal) {
            createWalletModal.style.display = 'none';
        }
        if (event.target == activationModal) {
            activationModal.style.display = 'none';
        }
        if (event.target == deleteWalletModal) {
            deleteWalletModal.style.display = 'none';
        }
        if (event.target == restoreWalletModal) {
            restoreWalletModal.style.display = 'none';
        }
        if (event.target == resetPasswordModal) {
            resetPasswordModal.style.display = 'none';
        }
    }

    // Handle Create Wallet Form Submission
    createWalletForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const termsAccepted = document.getElementById('terms-checkbox').checked;
        const password = document.getElementById('wallet-password').value;
        const repass = document.getElementById('wallet-repass').value;

        const messageContainer = createWalletModal.querySelector('.message-container');

        if (!termsAccepted) {
            displayMessage(messageContainer, 'You must accept the terms to create a wallet.', 'error');
            return;
        }

        if (password !== repass) {
            displayMessage(messageContainer, 'Passwords do not match.', 'error');
            return;
        }

        // Make API call to create wallet
        try {
            const response = await fetch('http://127.0.0.1:8000/wallets/creating_wallet/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify({ password, repass })
            });

            const data = await response.json();

            if (response.ok) {
                displayMessage(messageContainer, 'Wallet created successfully!', 'success');
                createWalletForm.reset();
                // Optionally, close the modal after a delay
                setTimeout(() => {
                    createWalletModal.style.display = 'none';
                }, 2000);
                fetchWalletData();
            } else {
                const errorMsg = data.detail || Object.values(data).join(' ');
                displayMessage(messageContainer, `Error: ${errorMsg}`, 'error');
            }
        } catch (error) {
            console.error('Error creating wallet:', error);
            displayMessage(messageContainer, 'An error occurred while creating the wallet.', 'error');
        }
    });

    // Handle Reset Password Form Submission
    resetPasswordForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const oldPassword = document.getElementById('old-password').value;
        const newPassword = document.getElementById('new-password').value;

        const messageContainer = resetPasswordModal.querySelector('.message-container');

        try {
            const response = await fetch('http://127.0.0.1:8000/wallets/reset_password/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}` // Assuming getAuthToken() fetches the token
                },
                body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
            });

            const data = await response.json();

            if (response.ok) {
                displayMessage(messageContainer, data.success, 'success');
                resetPasswordForm.reset();
                // Optionally, close the modal after a delay
                setTimeout(() => {
                    resetPasswordModal.style.display = 'none';
                }, 2000);
            } else {
                const errorMsg = data.detail || Object.values(data).join(' ');
                displayMessage(messageContainer, `Error: ${errorMsg}`, 'error');
            }
        } catch (error) {
            console.error('Error resetting password:', error);
            displayMessage(messageContainer, 'An error occurred while resetting the password.', 'error');
        }
    });

    // Handle Activation Form Submission
    activationForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const password = document.getElementById('activation-password').value;
        const state = document.getElementById('activation-modal-title').innerText.includes('Activate');

        const messageContainer = activationModal.querySelector('.message-container');

        // Make API call to activate/deactivate wallet
        try {
            const response = await fetch('http://127.0.0.1:8000/wallets/wallet_activation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify({ password, state })
            });

            const data = await response.json();

            if (response.ok) {
                displayMessage(messageContainer, 'Wallet status updated successfully!', 'success');
                activationForm.reset();
                // Optionally, close the modal after a delay
                setTimeout(() => {
                    activationModal.style.display = 'none';
                }, 2000);
                
                fetchWalletData();
            } else {
                const errorMsg = data.detail || Object.values(data).join(' ');
                displayMessage(messageContainer, `Error: ${errorMsg}`, 'error');
            }
        } catch (error) {
            console.error('Error updating wallet status:', error);
            displayMessage(messageContainer, 'An error occurred while updating wallet status.', 'error');
        }
    });

    // Handle Delete Wallet Form Submission
    deleteWalletForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const password = document.getElementById('delete-password').value;
        const confirmTxt = document.getElementById('confirm-delete').value;

        const messageContainer = deleteWalletModal.querySelector('.message-container');

        if (confirmTxt !== 'I Confirm' && confirmTxt !== 'i confirm') {
            displayMessage(messageContainer, 'You must type "I Confirm" to proceed with deletion.', 'error');
            return;
        }

        // Make API call to delete wallet
        try {
            const response = await fetch('http://127.0.0.1:8000/wallets/initial_delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify({ password, confirm_txt: confirmTxt })
            });

            const data = await response.json();

            if (response.ok) {
                displayMessage(messageContainer, 'Wallet deletion initiated. You can restore your wallet within 3 days.', 'success');
                
                // Optionally, close the modal after a delay
                setTimeout(() => {
                    deleteWalletModal.style.display = 'none';
                }, 2000);
                deleteWalletForm.reset();
                fetchWalletData();
            } else {
                const errorMsg = data.detail || Object.values(data).join(' ');
                displayMessage(messageContainer, `Error: ${errorMsg}`, 'error');
            }
        } catch (error) {
            console.error('Error deleting wallet:', error);
            displayMessage(messageContainer, 'An error occurred while deleting the wallet.', 'error');
        }
    });

    // Handle Restore Wallet Form Submission
    restoreWalletForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const password = document.getElementById('restore-password').value;

        const messageContainer = restoreWalletModal.querySelector('.message-container');

        // Make API call to restore wallet
        try {
            const response = await fetch('http://127.0.0.1:8000/wallets/restore_wallet/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify({ password })
            });

            const data = await response.json();

            if (response.ok) {
                displayMessage(messageContainer, 'Wallet restored successfully!', 'success');
                restoreWalletForm.reset();
                // Optionally, close the modal after a delay
                setTimeout(() => {
                    restoreWalletModal.style.display = 'none';
                }, 2000);
                fetchWalletData();
            } else {
                const errorMsg = data.detail || Object.values(data).join(' ');
                displayMessage(messageContainer, `Error: ${errorMsg}`, 'error');
            }
        } catch (error) {
            console.error('Error restoring wallet:', error);
            displayMessage(messageContainer, 'An error occurred while restoring the wallet.', 'error');
        }
    });

    // Function to fetch wallet data
    async function fetchWalletData() {
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
                renderWallet(data);
            } else {
                if (response.status === 404) {
                    // No wallet exists
                    renderNoWallet();
                } else if (data.deleted) {
                    // Wallet is deleted or in the process of deletion
                    renderDeletedWallet();
                } else {
                    const messageContainer = walletContent.querySelector('.message-container');
                    displayMessage(messageContainer, `Error: ${data.detail || JSON.stringify(data)}`, 'error');
                }
            }
        } catch (error) {
            console.error('Error fetching wallet data:', error);
            const messageContainer = walletContent.querySelector('.message-container');
            displayMessage(messageContainer, 'An error occurred while fetching wallet data.', 'error');
        }
    }

    // Function to render wallet when it exists
    function renderWallet(wallet) {
        walletContent.innerHTML = `
            <div class="balance-container">
                <p class="user-info">Wallet Balance: ${wallet.balance} EGP</p>
                <div class="button-container">
                    <button class="button" id="charge-wallet">Charge</button>
                    <button class="button" id="toggle-activation">${wallet.is_active ? 'Deactivate' : 'Activate'}</button>
                    <button class="button" id="delete-wallet">Delete Wallet</button>
                    <button class="button" id="reset-password-btn">Reset Password</button>
                </div>
            </div>
            <div class="message-container"></div> <!-- Added message container for wallet content -->
        `;

        // Attach event listeners to buttons
        document.getElementById('charge-wallet').addEventListener('click', () => {
            // Redirect to charge page or implement charge functionality
            window.location.href = '/Wallet/charge_wallet.html'; // Assuming you have a charge_wallet.html
        });

        document.getElementById('toggle-activation').addEventListener('click', () => {
            const action = wallet.is_active ? 'Deactivate' : 'Activate';
            activationModal.querySelector('#activation-modal-title').innerText = `${action} Wallet`;
            activationModal.querySelector('#activation-submit-button').innerText = `${action}`;
            activationModal.style.display = 'block';
        });

        document.getElementById('delete-wallet').addEventListener('click', () => {
            deleteWalletModal.style.display = 'block';
        });

        document.getElementById('reset-password-btn').addEventListener('click', () => {
            resetPasswordModal.style.display = 'block';
        });
    }

    // Function to render no wallet scenario
    function renderNoWallet() {
        walletContent.innerHTML = `
            <div class="noWallet-container">
                <p class="no-text">You don't have a wallet. Create one now.</p>
                <div class="cta">
                    <button id="create-wallet-button">Create Wallet</button>
                </div>
                <div class="message-container"></div> <!-- Added message container for wallet content -->
            </div>
        `;

        // Attach event listener to Create Wallet button
        document.getElementById('create-wallet-button').addEventListener('click', () => {
            createWalletModal.style.display = 'block';
        });
    }

    // Function to render deleted wallet scenario
    function renderDeletedWallet() {
        walletContent.innerHTML = `
            <div class="deletedWallet-container">
                <p class="no-text"><strong>Recover your Wallet before the three-day period expires</strong></p>
                <div class="cta">
                    <button id="restore-wallet-button">Restore Wallet</button>
                </div>
                <div class="message-container"></div> <!-- Added message container for wallet content -->
            </div>
        `;

        // Attach event listener to Restore Wallet button
        document.getElementById('restore-wallet-button').addEventListener('click', () => {
            restoreWalletModal.style.display = 'block';
        });
    }

    // Function to display messages within a specific container
    function displayMessage(container, message, type) {
        // console.log(`Displaying message: ${message} of type: ${type}`);
        // container.innerHTML = '';
        const div = document.createElement('div');
        div.classList.add('message');
        div.classList.add(type === 'success' ? 'success' : 'error');
        div.textContent = message;
        container.appendChild(div);
        console.log(container);
    }

    // Utility function to get Auth Token (Assuming token is stored in localStorage)
    function getAuthToken() {
        return localStorage.getItem('authToken') || '';
    }

    // Optionally, implement token management, logout functionality, etc.
});
