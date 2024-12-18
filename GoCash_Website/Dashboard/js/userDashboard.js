// js/userDashboard.js

document.addEventListener('DOMContentLoaded', () => {
    // Retrieve the token from localStorage
    const token = localStorage.getItem('authToken'); // Ensure the token is stored under 'authToken'
    console.log('token here -->', token)
    if (!token) {
        // If no token is found, redirect to the login page
        window.location.href = '/signin.html';
    }

    // Elements
    const username_Elem = document.getElementById('username_0');
    const usernameElem = document.getElementById('username');
    const phoneNumberElem = document.getElementById('phone-number');
    const balanceElem = document.getElementById('balance');
    const statusElem = document.getElementById('status');
    const subscriptionPlanElem = document.getElementById('subscriptionPlan');
    // const upgradeButton2 = document.getElementById('upgrade-button-2');
    // const upgradeButton = document.getElementById('upgrade-button');

    const modal = document.getElementById('card-modal');
    const closeButton = document.querySelector('.close-button');
    const modalUsername = document.getElementById('modal-username');
    const modalPhoneNumber = document.getElementById('modal-phone-number');
    const modalBalance = document.getElementById('modal-balance');
    const modalStatus = document.getElementById('modal-status');
    const modalPlan = document.getElementById('modal-plan');

    const gocashCard = document.getElementById('gocash-card');

    const logoutLink = document.getElementById('logout-link');

    // Fetch User Dashboard Data
    fetch('http://127.0.0.1:8000/dashboard/', { // Update the URL if necessary
        method: 'GET',
        headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 200) {
            return response.json();
        } else if (response.status === 401) {
            alert('Unauthorized access. Please log in again.');
            window.location.href = '/signin.html';
        } else {
            throw new Error('Failed to fetch data');
        }
    })
    .then(data => {
        // Populate card information
        username_Elem.textContent = data.username;
        usernameElem.textContent = data.username;
        phoneNumberElem.textContent = data.PhoneNumber;
        balanceElem.textContent = data.Balance;
        statusElem.textContent = data.Status === "True" || data.Status === true ? "Active Wallet" : "Inactive Wallet";
        statusElem.style.color = data.Status === "True" || data.Status === true ? "#30BB9F" : "#E47740";
        subscriptionPlanElem.textContent = data.SubscriptionPlan;

        // if (data.SubscriptionPlan == 'premium'){
        //     upgradeButton.textContent = 'Change Plan';
        //     upgradeButton2.textContent = 'Change Plan';
        // }
        // else{
        //     upgradeButton.textContent = 'Upgrade';
        //     upgradeButton2.textContent = 'Upgrade';
        // }

        // Populate modal information
        modalUsername.textContent = data.username;
        modalPhoneNumber.textContent = data.PhoneNumber;
        modalBalance.textContent = data.Balance;
        modalStatus.textContent = data.Status === "True" || data.Status === true ? "Active Wallet" : "Inactive Wallet";
        modalStatus.style.color = data.Status === "True" || data.Status === true ? "#30BB9F" : "#E47740";
        modalPlan.textContent = data.SubscriptionPlan;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while fetching dashboard data.');
    });

    // Popup Modal Functionality
    gocashCard.addEventListener('click', () => {
        modal.style.display = 'flex';
    });

    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // Upgrade plan button
    document.getElementById('upgrade-plan').addEventListener('click', () => {
        window.location.href = '/subscriptionplan.html';
    });

    // Action Buttons Event Listeners
    document.getElementById('charge-wallet').addEventListener('click', () => {
        window.location.href = '/Wallet/wallet.html';
    });

    document.getElementById('send-money').addEventListener('click', () => {
        window.location.href = '/Transactions/send_money.html'; // Update the path as needed
    });

    document.getElementById('transfers').addEventListener('click', () => {
        window.location.href = '/Transactions/transactions.html';
    });

    // Become Green Button
    document.getElementById('become-green-button').addEventListener('click', () => {
        window.location.href = '/'; // Update the path as needed
    });

    // Upgrade Button in Modal
    document.getElementById('upgrade-button-2').addEventListener('click', () => {
        window.location.href = '/'; // Update the path as needed
    });

    // Logout Functionality
    logoutLink.addEventListener('click', (e) => {
        e.preventDefault();
        // Send logout request to the API
        fetch('http://127.0.0.1:8000/logout/', {
            method: 'POST',
            headers: {
                'Authorization': `Token ${token}`, // Include the token in the header
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (response.ok) {
                // Remove the token from localStorage
                localStorage.removeItem('authToken');
                // Redirect to the home page
                window.location.href = '/index.html';
            } else {
                alert('Logout failed. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during logout. Please try again.');
        });
    });
});
