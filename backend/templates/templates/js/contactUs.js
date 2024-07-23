async function submitForm() {
    const branch = document.getElementById('branch').value;
    const name = document.getElementById('name').value;
    const phone = document.getElementById('phone').value;
    const message = document.getElementById('message').value;

    if (!branch || !name || !phone || !message) {
        alert("Please fill out all fields.");
        return;
    }

    const contactData = {
        branch,
        name,
        phone,
        message
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/contactus/contacts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(contactData)
        });

        if (response.ok) {
            alert("Message sent successfully!");
        } else {
            alert("Failed to send message.");
        }
    } catch (error) {
        console.error('Error:', error);
        alert("Error sending message.");
    }
}
