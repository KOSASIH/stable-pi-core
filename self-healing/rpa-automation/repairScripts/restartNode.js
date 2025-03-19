// stable-pi-core/self-healing/rpa-automation/repairScripts/restartNode.js

const { exec } = require('child_process'); // For executing shell commands
const winston = require('winston'); // For logging
const notifyAdmin = require('./notifyAdmin'); // Import the notifyAdmin function

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
 * Executes a shell command and returns a promise.
 * @param {string} command - The command to execute.
 * @returns {Promise<string>} - The output of the command.
 */
function executeCommand(command) {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                logger.error(`Command failed: ${command}. Error: ${error.message}`);
                reject(error);
            } else if (stderr) {
                logger.error(`Command error output: ${stderr}`);
                reject(new Error(stderr));
            } else {
                resolve(stdout);
            }
        });
    });
}

/**
 * Restarts a node in the network.
 * @param {string} nodeId - The identifier of the node to restart.
 * @param {number} retries - The number of retries if the restart fails.
 */
async function restartNode(nodeId, retries = 3) {
    logger.info(`Attempting to restart node: ${nodeId}`);

    const shutdownCommand = `ssh user@${nodeId} 'sudo systemctl stop your-node-service'`;
    const startCommand = `ssh user@${nodeId} 'sudo systemctl start your-node-service'`;

    try {
        // Step 1: Gracefully shut down the node
        await executeCommand(shutdownCommand);
        logger.info(`Node ${nodeId} shut down successfully.`);

        // Step 2: Start the node and check health
        for (let attempt = 1; attempt <= retries; attempt++) {
            await executeCommand(startCommand);
            logger.info(`Node ${nodeId} started successfully. Checking health...`);

            // Perform health check (this is a placeholder; implement your health check logic)
            const healthCheckCommand = `ssh user@${nodeId} 'curl -f http://localhost:your_health_check_port/health'`;
            try {
                await executeCommand(healthCheckCommand);
                logger.info(`Node ${nodeId} is healthy after restart.`);
                return; // Exit if healthy
            } catch (healthError) {
                logger.warn(`Health check failed on attempt ${attempt} for node ${nodeId}: ${healthError.message}`);
                if (attempt === retries) {
                    await notifyAdmin('Node Restart Failed', `Node ${nodeId} failed to restart after ${retries} attempts.`);
                }
            }
        }
    } catch (error) {
        logger.error(`Error restarting node ${nodeId}: ${error.message}`);
        await notifyAdmin('Node Restart Error', `Failed to restart node ${nodeId}: ${error.message}`);
    }
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
