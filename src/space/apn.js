// src/space/apn.js

class AntimatterPropulsionNetwork {
    constructor() {
        this.nodes = []; // Array to hold satellite nodes
        this.status = {}; // Object to hold the status of each node
    }

    // Method to add a new satellite node
    addNode(node) {
        if (this.nodes.find(n => n.name === node.name)) {
            throw new Error(`Node ${node.name} already exists in the network.`);
        }
        this.nodes.push(node);
        this.status[node.name] = { propulsionActive: false, currentOrbit: null };
        console.log(`Node ${node.name} added to the Antimatter Propulsion Network.`);
    }

    // Method to initiate propulsion for a specific node
    async initiatePropulsion(nodeName, targetOrbit) {
        const node = this.nodes.find(n => n.name === nodeName);
        if (!node) {
            throw new Error(`Node ${nodeName} not found in the network.`);
        }

        console.log(`Initiating propulsion for ${nodeName} to reach orbit ${targetOrbit}...`);
        this.status[nodeName].propulsionActive = true;

        const travelTime = this.calculateTravelTime(targetOrbit);
        await this.simulateTravel(travelTime);
        
        this.status[nodeName].currentOrbit = targetOrbit;
        this.status[nodeName].propulsionActive = false;
        console.log(`${nodeName} has reached orbit ${targetOrbit}.`);
    }

    // Method to calculate travel time based on target orbit
    calculateTravelTime(targetOrbit) {
        const speedOfLight = 299792458; // Speed of light in m/s
        const distanceToOrbit = this.getDistanceToOrbit(targetOrbit); // Distance in meters
        const timeInSeconds = distanceToOrbit / speedOfLight; // Time = Distance / Speed
        return timeInSeconds;
    }

    // Method to simulate travel time (mock implementation)
    async simulateTravel(seconds) {
        return new Promise(resolve => setTimeout(resolve, seconds * 1000)); // Simulate travel time
    }

    // Method to get distance to a specific orbit (mock implementation)
    getDistanceToOrbit(targetOrbit) {
        const orbits = {
            'Earth': 1.496e11, // Distance from the Sun to Earth in meters
            'Mars': 2.279e11, // Distance from the Sun to Mars in meters
            'Jupiter': 7.785e11, // Distance from the Sun to Jupiter in meters
            // Add more orbits as needed
        };
        return orbits[targetOrbit] || 0; // Return 0 if orbit not found
    }

    // Method to get the status of a specific node
    getNodeStatus(nodeName) {
        const status = this.status[nodeName];
        if (!status) {
            throw new Error(`Node ${nodeName} not found in the network.`);
        }
        return {
            name: nodeName,
            propulsionActive: status.propulsionActive,
            currentOrbit: status.currentOrbit,
        };
    }

    // Method to get the status of all nodes
    getAllNodesStatus() {
        return this.nodes.map(node => this.getNodeStatus(node.name));
    }
}

export default AntimatterPropulsionNetwork;
