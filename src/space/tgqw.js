// src/space/tgqw.js

class TransGalacticQuantumWeaver {
    constructor() {
        this.networks = []; // Array to hold created networks
        this.resourcePool = {}; // Global resource pool for efficient management
    }

    /**
     * Create a new trans-galactic network.
     * @param {String} galaxyName - The name of the galaxy where the network will be created.
     * @param {Object} resources - The local resources to be utilized.
     * @returns {Object} - The created network object.
     */
    createNetwork(galaxyName, resources) {
        const newNetwork = {
            id: this.generateNetworkId(),
            galaxyName: galaxyName,
            resources: this.allocateResources(resources),
            state: 'active', // State of the network
            createdAt: new Date(),
            nodes: [], // Array to hold nodes in the network
        };
        this.networks.push(newNetwork);
        console.log(`Trans-galactic network created in "${galaxyName}" with resources:`, newNetwork.resources);
        return newNetwork;
    }

    /**
     * Generate a unique ID for the network.
     * @returns {String} - The unique network ID.
     */
    generateNetworkId() {
        return `network-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
    }

    /**
     * Allocate resources from the global resource pool.
     * @param {Object} requestedResources - The resources requested for allocation.
     * @returns {Object} - The allocated resources.
     */
    allocateResources(requestedResources) {
        const allocatedResources = {};
        for (const resource in requestedResources) {
            if (this.resourcePool[resource] && this.resourcePool[resource] >= requestedResources[resource]) {
                allocatedResources[resource] = requestedResources[resource];
                this.resourcePool[resource] -= requestedResources[resource];
            } else {
                console.warn(`Insufficient ${resource} in the resource pool. Allocating available amount.`);
                allocatedResources[resource] = this.resourcePool[resource] || 0;
                this.resourcePool[resource] = 0; // Set to zero after allocation
            }
        }
        return allocatedResources;
    }

    /**
     * Expand the network by utilizing local resources.
     * @param {String} networkId - The ID of the network to expand.
     * @param {Object} additionalResources - Additional resources to be utilized for expansion.
     */
    expandNetwork(networkId, additionalResources) {
        const network = this.networks.find(n => n.id === networkId);
        if (!network) {
            console.error(`Network with ID "${networkId}" not found.`);
            return;
        }

        // Example logic for expanding the network
        const allocatedResources = this.allocateResources(additionalResources);
        network.resources = { ...network.resources, ...allocatedResources };
        console.log(`Network "${networkId}" expanded with additional resources:`, allocatedResources);
    }

    /**
     * Create a new node in the specified network.
     * @param {String} networkId - The ID of the network where the node will be created.
     * @param {Object} nodeData - The data for the new node.
     * @returns {Object} - The created node object.
     */
    createNode(networkId, nodeData) {
        const network = this.networks.find(n => n.id === networkId);
        if (!network) {
            console.error(`Network with ID "${networkId}" not found.`);
            return;
        }

        const newNode = {
            id: this.generateNodeId(),
            data: nodeData,
            state: 'active',
            createdAt: new Date(),
        };
        network.nodes.push(newNode);
        console.log(`Node created in network "${networkId}":`, newNode);
        return newNode;
    }

    /**
     * Generate a unique ID for the node.
     * @returns {String} - The unique node ID.
     */
    generateNodeId() {
        return `node-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
    }

    /**
     * List all created trans-galactic networks.
     */
    listNetworks() {
        console.log("Current Trans-Galactic Networks:");
        this.networks.forEach(network => {
            console.log(`- ID: ${network.id}, Galaxy: ${network.galaxyName}, Resources:`, network.resources, `, Nodes: ${network.nodes.length}`);
        });
    }

    /**
     * Destroy a trans-galactic network.
     * @param {String} networkId - The ID of the network to destroy.
     * @returns {Boolean} - True if the network was destroyed, false otherwise.
     */
    destroyNetwork(networkId) {
        const index = this.networks.findIndex(n => n.id === networkId);
        if (index === -1) {
            console.error(`Network with ID "${networkId}" not found.`);
            return false;
        }

        this.networks.splice(index, 1);
        console.log(`Network with ID "${networkId}" has been destroyed.`);
        return true;
    }

    /**
     * Add resources to the global resource pool.
     * @param {Object} resources - The resources to add to the pool.
     */
    addResourcesToPool(resources) {
        for (const resource in resources) {
            if (!this.resourcePool[resource]) {
                this.resourcePool[resource] = 0;
            }
            this.resourcePool[resource] += resources[resource];
            console.log(`Added ${resources[resource]} of ${resource} to the resource pool.`);
        }
    }

    /**
     * Get the current state of the resource pool.
     * @returns {Object} - The current state of the resource pool.
     */
    getResourcePoolState() {
        return this.resourcePool;
    }
}

// Export the module
export default TransGalacticQuantumWeaver;
