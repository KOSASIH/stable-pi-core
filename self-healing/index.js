// stable-pi-core/self-healing/index.js

const GossipNode = require('./gossip-protocol/gossipNode'); // Import the gossip node implementation
const NetworkMonitor = require('./gossip-protocol/networkMonitor'); // Import the network monitor
const RPAController = require('./rpa-automation/rpaController'); // Import the RPA controller
const winston = require('winston'); // For logging
require('dotenv').config(); // Load environment variables from .env file

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'selfHealing.log' }),
        new winston.transports.Console()
    ]
});

// Initialize the gossip node
const port = process.env.GOSSIP_PORT || 8080; // Use provided port or default to 8080
const gossipNode = new GossipNode(port);
gossipNode.start();

// Initialize the network monitor
const networkMonitor = new NetworkMonitor(10000); // Check every 10 seconds
networkMonitor.addNode('node-1', '192.168.1.10'); // Example node
networkMonitor.addNode('node-2', '192.168.1.11'); // Example node

// Listen for unhealthy nodes and trigger actions
networkMonitor.on('nodeUnhealthy', async (nodeId) => {
    logger.warn(`Node ${nodeId} is unhealthy. Triggering RPA actions.`);
    await RPAController.handleIssue({ type: 'NODE_FAILURE', nodeId });
});

// Listen for unreachable nodes and notify admin
networkMonitor.on('nodeUnreachable', async (nodeId) => {
    logger.warn(`Node ${nodeId} is unreachable. Notifying admin.`);
    await RPAController.handleIssue({ type: 'NODE_UNREACHABLE', nodeId });
});

// Start monitoring the network
networkMonitor.startMonitoring();

// Example of adding a new node dynamically
setTimeout(() => {
    networkMonitor.addNode('node-3', '192.168.1.12'); // Dynamically add a new node
}, 30000); // Add after 30 seconds

logger.info('Self-healing network protocol initialized successfully.');
