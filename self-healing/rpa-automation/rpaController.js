// stable-pi-core/self-healing/rpa-automation/rpaController.js

const restartNode = require('./repairScripts/restartNode'); // Import the restart node script
const scaleUpNode = require('./repairScripts/scaleUpNode'); // Import the scale up node script
const notifyAdmin = require('./repairScripts/notifyAdmin'); // Import the notify admin script
const winston = require('winston'); // For logging

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'rpaController.log' }),
        new winston.transports.Console()
    ]
});

/**
 * Handles the action to take based on the detected issue.
 * @param {Object} issue - The detected issue object.
 */
async function handleIssue(issue) {
    logger.info(`Handling issue: ${issue.type}`);

    switch (issue.type) {
        case 'NODE_FAILURE':
            logger.info(`Detected node failure for node ID: ${issue.nodeId}`);
            await restartNode(issue.nodeId);
            break;

        case 'HIGH_LATENCY':
            logger.info(`Detected high latency for node ID: ${issue.nodeId}`);
            await scaleUpNode(issue.nodeId, issue.additionalCores, issue.additionalMemory);
            break;

        case 'RESOURCE_EXHAUSTION':
            logger.info(`Detected resource exhaustion for node ID: ${issue.nodeId}`);
            await scaleUpNode(issue.nodeId, issue.additionalCores, issue.additionalMemory);
            break;

        default:
            logger.warn(`Unknown issue type: ${issue.type}`);
            await notifyAdmin('Unknown Issue Detected', `An unknown issue type "${issue.type}" was detected for node ID: ${issue.nodeId}`);
            break;
    }
}

// Example usage
if (require.main === module) {
    const exampleIssue = {
        type: 'NODE_FAILURE',
        nodeId: 'node-1',
        additionalCores: 2,
        additionalMemory: 2048
    };

    handleIssue(exampleIssue)
        .then(() => logger.info('Issue handled successfully.'))
        .catch(error => logger.error('Error handling issue:', error));
}

module.exports = {
    handleIssue
};
