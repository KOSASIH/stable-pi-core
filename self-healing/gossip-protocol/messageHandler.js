// stable-pi-core/self-healing/gossip-protocol/messageHandler.js

const winston = require('winston'); // For logging

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'messageHandler.log' }),
        new winston.transports.Console()
    ]
});

/**
 * Validates the incoming message.
 * @param {Object} message - The message to validate.
 * @returns {boolean} - True if the message is valid, false otherwise.
 */
function validateMessage(message) {
    if (!message || typeof message !== 'object') {
        logger.error('Invalid message format: Message is not an object.');
        return false;
    }
    if (!message.type) {
        logger.error('Invalid message format: Missing message type.');
        return false;
    }
    // Add more validation rules as needed
    return true;
}

/**
 * Processes an incoming message.
 * @param {Object} message - The incoming message.
 * @param {Function} handleMessage - The function to call for further processing.
 */
function processIncomingMessage(message, handleMessage) {
    if (validateMessage(message)) {
        logger.info(`Processing incoming message: ${JSON.stringify(message)}`);
        handleMessage(message);
    } else {
        logger.warn(`Received invalid message: ${JSON.stringify(message)}`);
    }
}

/**
 * Formats a message for sending to peers.
 * @param {string} type - The type of the message.
 * @param {Object} payload - The payload of the message.
 * @returns {Object} - The formatted message.
 */
function formatMessage(type, payload) {
    return {
        type: type,
        timestamp: new Date().toISOString(),
        ...payload
    };
}

/**
 * Sends a message to a peer.
 * @param {Object} peer - The peer address to send the message to.
 * @param {Object} message - The message to send.
 * @param {Function} sendFunction - The function to call to send the message.
 */
function sendMessageToPeer(peer, message, sendFunction) {
    const formattedMessage = formatMessage(message.type, message.payload);
    sendFunction(peer, formattedMessage);
    logger.info(`Sent message to ${peer}: ${JSON.stringify(formattedMessage)}`);
}

// Example usage
if (require.main === module) {
    // Example of how to use the message handler
    const exampleMessage = {
        type: 'STATUS_UPDATE',
        payload: {
            nodeId: 'node-1',
            status: 'healthy'
        }
    };

    processIncomingMessage(exampleMessage, (msg) => {
        logger.info(`Handled message: ${JSON.stringify(msg)}`);
    });
}

module.exports = {
    processIncomingMessage,
    sendMessageToPeer
};
