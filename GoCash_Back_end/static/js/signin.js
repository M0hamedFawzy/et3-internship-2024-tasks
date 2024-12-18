document.getElementById('signin-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const phone = document.getElementById('phone').value;

    if (!phone) {
        displayMessage('Phone number is required.', 'error');
        return;
    }

    fetch('/sign_up/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ phone: phone })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayMessage(data.success, 'success');
            window.location.href = '/users'; // Redirect after successful login
        } else {
            displayMessage(data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayMessage('An unexpected error occurred.', 'error');
    });
});

function displayMessage(message, type) {
    const messageBox = document.getElementById('message-box');
    messageBox.innerHTML = `<p class="${type}">${message}</p>`;
}
