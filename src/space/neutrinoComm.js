// src/space/neutrinoComm.js

class NeutrinoBasedCommunicationArray {
    constructor() {
        this.nodes = []; // Array to hold satellite nodes
        this.messageQueue = []; // Queue for messages to be sent
    }

    // Method to add a new satellite node
    addNode(node) {
        if (this.nodes.find(n => n.name === node.name)) {
            throw new Error(`Node ${node.name} already exists in the communication array.`);
        }
        this.nodes.push(node);
        console.log(`Node ${node.name} added to the Neutrino Communication Array.`);
    }

    // Method to send a message to a specific node
    async sendMessage(nodeName, message) {
        const node = this.nodes.find(n => n.name === nodeName);
        if (!node) {
            throw new Error(`Node ${nodeName} not found in the communication array.`);
        }

        console.log(`Sending message to ${nodeName}: ${message}`);
        this.messageQueue.push({ nodeName, message });
        await this.simulateTransmission(node, message);
    }

    // Method to simulate message transmission (mock implementation)
    async simulateTransmission(node, message) {
        // Simulate the time taken for neutrino communication
        const transmissionTime = this.calculateTransmissionTime(node);
        return new Promise(resolve => {
            setTimeout(() => {
                console.log(`Message sent to ${node.name} using neutrino communication: ${message}`);
                resolve();
            }, transmissionTime * 1000); // Simulate transmission time in seconds
        });
    }

    // Method to calculate transmission time based on distance to the node
    calculateTransmissionTime(node) {
        const speedOfNeutrinos = 299792458; // Speed of light in m/s (approximation for neutrinos)
        const distanceToNode = this.getDistanceToNode(node); // Distance in meters
        return distanceToNode / speedOfNeutrinos; // Time = Distance / Speed
    }

    // Method to get distance to a specific node (mock implementation)
    getDistanceToNode(node) {
        // Assuming each node has a predefined distance from the base station
        const distances = {
            'Node1': 1.496e11, // Example distance to Node1 (e.g., Earth)
            'Node2': 2.279e11, // Example distance to Node2 (e.g., Mars)
            'Node3': 7.785e11, // Example distance to Node3 (e.g., Jupiter)
            // Add more nodes and their distances as needed
        };
        return distances[node.name] || 0; // Return 0 if node not found
    }

    // Method to retrieve the message queue
    getMessageQueue() {
        return this.messageQueue;
    }

    // Method to clear the message queue
    clearMessageQueue() {
        this.messageQueue = [];
        console.log("Message queue cleared.");
    }
}

export default NeutrinoBasedCommunicationArray;
