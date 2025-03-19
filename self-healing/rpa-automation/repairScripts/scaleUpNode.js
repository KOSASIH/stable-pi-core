// stable-pi-core/self-healing/rpa-automation/repairScripts/scaleUpNode.js

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
        new winston.transports.File({ filename: 'scaleUpNode.log' }),
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
 * Scales up resources for a specified node.
 * @param {string} nodeId - The identifier of the node to scale up.
 * @param {number} additionalCores - The number of additional CPU cores to allocate.
 * @param {number} additionalMemory - The amount of additional memory (in MB) to allocate.
 * @param {number} retries - The number of retries if the scaling operation fails.
 */
async function scaleUpNode(nodeId, additionalCores, additionalMemory, retries = 3) {
    logger.info(`Attempting to scale up node: ${nodeId} with ${additionalCores} cores and ${additionalMemory}MB memory`);

    // Command to scale up the node (this is a placeholder; adjust as needed)
    const scaleCommand = `ssh user@${nodeId} 'sudo scale-node --cores ${additionalCores} --memory ${additionalMemory}'`;

    try {
        // Step 1: Execute the scaling command
        await executeCommand(scaleCommand);
        logger.info(`Node ${nodeId} scaled up successfully.`);

        // Step 2: Perform health check after scaling
        const healthCheckCommand = `ssh user@${nodeId} 'curl -f http://localhost:your_health_check_port/health'`;
        await executeCommand(healthCheckCommand);
        logger.info(`Node ${nodeId} is healthy after scaling.`);
    } catch (error) {
        logger.error(`Error scaling up node ${nodeId}: ${error.message}`);
        await notifyAdmin('Node Scaling Error', `Failed to scale up node ${nodeId}: ${error.message}`);

        // Retry mechanism
        for (let attempt = 1; attempt <= retries; attempt++) {
            logger.info(`Retrying scaling for node ${nodeId}, attempt ${attempt}...`);
            try {
                await executeCommand(scaleCommand);
                logger.info(`Node ${nodeId} scaled up successfully on retry.`);
                
                // Health check after retry
                await executeCommand(healthCheckCommand);
                logger.info(`Node ${nodeId} is healthy after scaling on retry.`);
                return; // Exit if successful
            } catch (retryError) {
                logger.warn(`Retry attempt ${attempt} failed for node ${nodeId}: ${retryError.message}`);
                if (attempt === retries) {
                    await notifyAdmin('Node Scaling Failed', `Node ${nodeId} failed to scale up after ${retries} attempts.`);
                }
            }
        }
    }
}

// Example usage
if (require.main === module) {
    const nodeId = process.argv[2]; // Get the node ID from command line arguments
    const additionalCores = parseInt(process.argv[3], 10); // Get additional cores
    const additionalMemory = parseInt(process.argv[4], 10); // Get additional memory

    if (!nodeId || isNaN(additionalCores) || isNaN(additionalMemory)) {
        logger.error('Node ID, additional cores, and additional memory are required as command line arguments.');
        process.exit(1);
    }
    scaleUpNode(nodeId, additionalCores, additionalMemory);
}

module.exports = scaleUpNode;
