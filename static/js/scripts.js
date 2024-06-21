document.getElementById('automationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const actions = formData.getAll('actions');
    const interval = formData.get('interval');
    const timeCap = formData.get('time_cap');

    fetch('/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ actions, interval, timeCap })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = data.message;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'An error occurred. Please try again.';
    });
});
