// document.addEventListener("DOMContentLoaded", () => {
//     // Retrieve the token from localStorage
//     const token = localStorage.getItem('authToken'); // Ensure the token is stored under 'authToken'
//     console.log('token here -->', token)
//     if (!token) {
//         // If no token is found, redirect to the login page
//         window.location.href = '/signin.html';
//     }

//     const methods = document.querySelectorAll(".method");
//     const modal = document.getElementById("payment-modal");
//     const closeModal = modal.querySelector(".close");
//     const confirmButton = document.getElementById("confirm-button");
//     const confirmCheckbox = document.getElementById("confirm-checkbox");
//     const discountLabel = document.getElementById("discount-label");

//     let userGreenStatus = null;

//     // Fetch green-user status
//     fetch('http://127.0.0.1:8000/payment/', { // Update the URL if necessary
//         method: 'GET',
//         headers: {
//             'Authorization': `Token ${token}`,
//             'Content-Type': 'application/json'
//         }
//     }).then(response => {
//         if (response.status === 200) {
//             return response.json();
//         } else if (response.status === 401) {
//             alert('Unauthorized access. Please log in again.');
//             window.location.href = '/signin.html';
//         } else {
//             throw new Error('Failed to fetch data');
//         }
//     })
//     .then(data => {
//             userGreenStatus = data["green-user-status"];
//         });

//     methods.forEach(method => {
//         method.addEventListener("click", () => {
//             const serviceType = method.dataset.serviceType;
//             const serviceName = method.dataset.serviceName;

//             document.getElementById("service-name").textContent = serviceName;
//             document.getElementById("service-image").src = `/images/${serviceName.toLowerCase()}.png`;
//             modal.style.display = "flex";

//             // Handle discounts
//             if (serviceType === "Merchant Payment" && userGreenStatus) {
//                 const discount = userGreenStatus === 1 ? 0.025 : userGreenStatus === 2 ? 0.05 : 0.15;
//                 discountLabel.textContent = `Discount: ${discount * 100}%`;
//             } else {
//                 discountLabel.textContent = "";
//             }
//         });
//     });

//     closeModal.addEventListener("click", () => {
//         modal.style.display = "none";
//     });

//     confirmCheckbox.addEventListener("change", () => {
//         confirmButton.disabled = !confirmCheckbox.checked;
//     });

//     confirmButton.addEventListener("click", () => {
//         const amount = document.getElementById("amount").value;
//         const serviceName = document.getElementById("service-name").textContent;
//         const serviceType = document.querySelector(".method.active").dataset.serviceType;

//         fetch("http://localhost:8000/payment/payment-portal/", {
//             method: "POST",
//             headers: {
//                 'Authorization': `Token ${token}`,
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ service_type: serviceType, service_name: serviceName, amount }),
//         })
//             .then(res => res.json())
//             .then(data => {
//                 alert(data.detail);
//                 modal.style.display = "none";
//             })
//             .catch(err => console.error(err));
//     });
// });


// js/payment.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('authToken');
    const modal = document.getElementById('payment-modal');
    const closeModal = modal.querySelector('.close');
    const confirmButton = modal.querySelector('#confirm-button');
    const confirmCheckbox = modal.querySelector('#confirm-checkbox');
    const messageContainer = document.getElementById('message-container');
    const amountInput = modal.querySelector('#amount');
    const serviceNameLabel = modal.querySelector('#service-name');
    const serviceImage = modal.querySelector('#service-image');

    messageContainer.id = 'message-container';
    modal.querySelector('.modal-content').appendChild(messageContainer);

    let selectedService = {
        service_type: '',
        service_name: ''
    };

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
    // Function to disable form inputs
    function disableForm() {
        confirmButton.disabled = true;
        confirmCheckbox.disabled = true;
        amountInput.disabled = true;
    }

    // Function to check wallet status
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
            } else {
                const errorMsg = data.detail || Object.values(data).join(' ');
                displayMessage(`Error: ${errorMsg}`, 'error');
                disableForm();
            }
        } catch (error) {
            console.error('Error fetching wallet status:', error);
            displayMessage('An error occurred while checking wallet status.', 'error');
            disableForm();
        }
    }

    // Attach event listeners to service methods
    document.querySelectorAll('.method').forEach(method => {
        method.addEventListener('click', () => {
            selectedService.service_type = method.dataset.serviceType;
            selectedService.service_name = method.dataset.serviceName;

            serviceNameLabel.textContent = selectedService.service_name;
            serviceImage.src = method.querySelector('img').src;
            modal.style.display = 'block';
        });
    });

    // Close modal
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Enable confirm button when checkbox is checked
    confirmCheckbox.addEventListener('change', () => {
        confirmButton.disabled = !confirmCheckbox.checked;
    });

    // Handle form submission
    confirmButton.addEventListener('click', async () => {
        const amount = parseFloat(amountInput.value);

        if (isNaN(amount) || amount <= 0) {
            displayMessage('Please enter a valid amount greater than 0.', 'error');
            return;
        }

        const data = {
            amount: amount,
            service_type: selectedService.service_type,
            service_name: selectedService.service_name
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/payment/payment-portal/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                displayMessage(result.detail || 'Payment successful.', 'success');
                modal.style.display = 'none';
            } else {
                displayMessage(result.detail || 'Payment failed.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            displayMessage('An unexpected error occurred. Please try again later.', 'error');
        }
    });

    // Check wallet status on page load
    checkWalletStatus();

    // Close modal when clicking outside it
    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});


