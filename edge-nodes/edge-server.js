// edge-nodes/edge-server.js

const express = require('express');
const bodyParser = require('body-parser');
const { storeData } = require('../scripts/utils/ipfsUtils');
const { submitDataToOracle } = require('../scripts/offchain_processing');
const rateLimit = require('express-rate-limit');
const { body, validationResult } = require('express-validator');
const winston = require('winston');
require('dotenv').config(); // Load environment variables from .env file

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());

// Logger setup
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.json(),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' }),
    ],
});

// Rate limiting middleware
const limiter = rateLimit({
    windowMs: 1 * 60 * 1000, // 1 minute
    max: 100, // Limit each IP to 100 requests per windowMs
    message: 'Too many requests, please try again later.',
});
app.use(limiter);

// Health check endpoint
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'UP' });
});

// Endpoint to handle incoming data for processing
app.post('/process', 
    // Input validation
    body('dataType').isString().notEmpty().withMessage('Data type must be a non-empty string.'),
    body('data').isString().notEmpty().withMessage('Data must be a non-empty string.'),
    async (req, res) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }

        const { dataType, data } = req.body;

        try {
            // Step 1: Store data on IPFS
            const cid = await storeData({ dataType, data });

            // Step 2: Submit the CID to the Oracle contract
            await submitDataToOracle(dataType, cid);

            // Respond with success
            res.status(200).json({ message: 'Data processed successfully', cid });
        } catch (error) {
            logger.error('Error processing data:', error);
            res.status(500).json({ error: 'Internal server error', details: error.message });
        }
    }
);

// Start the server
app.listen(PORT, () => {
    logger.info(`Edge server is running on http://localhost:${PORT}`);
});
