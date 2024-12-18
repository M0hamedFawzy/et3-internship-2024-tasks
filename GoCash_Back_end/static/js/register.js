document.getElementById('registration-form').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent the form from submitting normally

    const username = document.getElementById('username').value;
    const phone = document.getElementById('phone').value;

    // Validate inputs
    if (!username || !phone) {
        displayMessage('Both fields are required.', 'error');
        return;
    }

    fetch('/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            username: username,
            phone: phone
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayMessage(data.success, 'success');
        } else {
            displayMessage(data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayMessage('An unexpected error occurred.', 'error');
    });
});

// Function to display messages
function displayMessage(message, type) {
    const messageBox = document.getElementById('message-box');
    messageBox.innerHTML = `<p class="${type}">${message}</p>`;
}
