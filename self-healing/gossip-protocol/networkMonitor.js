// stable-pi-core/self-healing/gossip-protocol/networkMonitor.js

const { exec } = require('child_process'); // For executing shell commands
const winston = require('winston'); // For logging
const EventEmitter = require('events'); // For event handling
const axios = require('axios'); // For making HTTP requests

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'networkMonitor.log' }),
        new winston.transports.Console()
    ]
});

class NetworkMonitor extends EventEmitter {
    constructor(checkInterval = 5000) {
        super();
        this.checkInterval = checkInterval; // Interval for health checks
        this.nodes = new Map(); // Map to store node statuses
    }

    // Add a node to monitor
    addNode(nodeId, address) {
        this.nodes.set(nodeId, { address, status: 'unknown' });
        logger.info(`Added node to monitor: ${nodeId} at ${address}`);
    }

    // Remove a node from monitoring
    removeNode(nodeId) {
        this.nodes.delete(nodeId);
        logger.info(`Removed node from monitoring: ${nodeId}`);
    }

    // Check the health of a node
    async checkNodeHealth(nodeId, address) {
        try {
            const response = await axios.get(`http://${address}/health`);
            if (response.status === 200) {
                this.nodes.get(nodeId).status = 'healthy';
                logger.info(`Node ${nodeId} is healthy.`);
            } else {
                this.nodes.get(nodeId).status = 'unhealthy';
                logger.warn(`Node ${nodeId} is unhealthy. Status code: ${response.status}`);
                this.emit('nodeUnhealthy', nodeId);
            }
        } catch (error) {
            this.nodes.get(nodeId).status = 'unreachable';
            logger.error(`Node ${nodeId} is unreachable: ${error.message}`);
            this.emit('nodeUnreachable', nodeId);
        }
    }

    // Monitor all nodes
    async monitorNodes() {
        for (const [nodeId, { address }] of this.nodes) {
            await this.checkNodeHealth(nodeId, address);
        }
    }

    // Start monitoring the network
    startMonitoring() {
        logger.info('Starting network monitoring...');
        this.monitorInterval = setInterval(() => {
            this.monitorNodes();
        }, this.checkInterval);
    }

    // Stop monitoring the network
    stopMonitoring() {
        clearInterval(this.monitorInterval);
        logger.info('Stopped network monitoring.');
    }
}

// Example usage
if (require.main === module) {
    const networkMonitor = new NetworkMonitor(10000); // Check every 10 seconds
    networkMonitor.addNode('node-1', '192.168.1.10');
    networkMonitor.addNode('node-2', '192.168.1.11');

    // Listen for unhealthy nodes
    networkMonitor.on('nodeUnhealthy', (nodeId) => {
        logger.warn(`Triggering action for unhealthy node: ${nodeId}`);
        // Trigger appropriate action (e.g., restart node, notify admin)
    });

    // Listen for unreachable nodes
    networkMonitor.on('nodeUnreachable', (nodeId) => {
        logger.warn(`Triggering action for unreachable node: ${nodeId}`);
        // Trigger appropriate action (e.g., notify admin)
    });

    networkMonitor.startMonitoring();
}

module.exports = NetworkMonitor;
