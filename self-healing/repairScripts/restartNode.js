// stable-pi-core/rpa-automation/repairScripts/restartNode.js

const { exec } = require('child_process'); // For executing shell commands
const winston = require('winston'); // For logging

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'restartNode.log' }),
        new winston.transports.Console()
    ]
});

/**
 * Restarts a node in the network.
 * @param {string} nodeId - The identifier of the node to restart.
 */
function restartNode(nodeId) {
    logger.info(`Attempting to restart node: ${nodeId}`);

    // Command to restart the node (this is a placeholder; adjust as needed)
    const command = `ssh user@${nodeId} 'sudo systemctl restart your-node-service'`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            logger.error(`Error restarting node ${nodeId}: ${error.message}`);
            return;
        }
        if (stderr) {
            logger.error(`Error output from node ${nodeId}: ${stderr}`);
            return;
        }
        logger.info(`Node ${nodeId} restarted successfully. Output: ${stdout}`);
    });
}

// Example usage
if (require.main === module) {
    const nodeId = process.argv[2]; // Get the node ID from command line arguments
    if (!nodeId) {
        logger.error('Node ID is required as a command line argument.');
        process.exit(1);
    }
    restartNode(nodeId);
}

module.exports = restartNode;
