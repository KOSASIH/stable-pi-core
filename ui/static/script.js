// Function to send a message to the AI assistant
function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    const chatBox = document.getElementById('chat-box');

    if (userInput === "") {
        alert("Please enter a message.");
        return;
    }

    // Display user message in chat box
    chatBox.innerHTML += `<div>User: ${userInput}</div>`;
    document.getElementById('user-input').value = ''; // Clear input field

    // Send the message to the server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Display AI response in chat box
        chatBox.innerHTML += `<div>AI: ${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    })
    .catch(error => {
        console.error('Error:', error);
        chatBox.innerHTML += `<div>AI: Sorry, there was an error processing your request.</div>`;
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    });
}

// Function to run a simulation based on user input
function runSimulation() {
    const userDecision = document.getElementById('user-decision').value.trim();
    const simulationResult = document.getElementById('simulation-result');

    if (userDecision === "") {
        alert("Please enter a decision.");
        return;
    }

    // Send the decision to the server for simulation
    fetch('/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ decision: userDecision })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Display simulation result
        simulationResult.innerHTML = `Simulation Result: ${data.result}`;
        document.getElementById('user-decision').value = ''; // Clear input field
    })
    .catch(error => {
        console.error('Error:', error);
        simulationResult.innerHTML = "Sorry, there was an error processing your simulation.";
    });
}
