// stable-pi-core/self-healing/apiGateway.js

const express = require('express');
const bodyParser = require('body-parser');
const { interactWithEthereumContract, interactWithBSCContract } = require('./blockchainService');
const winston = require('winston');

// Configure logging
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'apiGateway.log' }),
        new winston.transports.Console()
    ]
});

// Initialize Express app
const app = express();
app.use(bodyParser.json());

// Endpoint to add liquidity to the Ethereum contract
app.post('/api/ethereum/addLiquidity', async (req, res) => {
    const { amountA, amountB } = req.body;
    try {
        const result = await interactWithEthereumContract('addLiquidity', [amountA, amountB]);
        res.json({ success: true, result });
    } catch (error) {
        logger.error(`Error adding liquidity: ${error.message}`);
        res.status(500).json({ success: false, message: error.message });
    }
});

// Endpoint to swap tokens on the Ethereum contract
app.post('/api/ethereum/swap', async (req, res) => {
    const { amountIn, isAToB } = req.body;
    try {
        const result = await interactWithEthereumContract('swap', [amountIn, isAToB]);
        res.json({ success: true, result });
    } catch (error) {
        logger.error(`Error swapping tokens: ${error.message}`);
        res.status(500).json({ success: false, message: error.message });
    }
});

// Endpoint to create a proposal in the DAO
app.post('/api/dao/createProposal', async (req, res) => {
    const { description } = req.body;
    try {
        const result = await interactWithEthereumContract('createProposal', [description]);
        res.json({ success: true, result });
    } catch (error) {
        logger.error(`Error creating proposal: ${error.message}`);
        res.status(500).json({ success: false, message: error.message });
    }
});

// Endpoint to vote on a proposal
app.post('/api/dao/vote', async (req, res) => {
    const { proposalId, support } = req.body;
    try {
        const result = await interactWithEthereumContract('vote', [proposalId, support]);
        res.json({ success: true, result });
    } catch (error) {
        logger.error(`Error voting on proposal: ${error.message}`);
        res.status(500).json({ success: false, message: error.message });
    }
});

// Endpoint to fetch market data
app.get('/api/market/data', async (req, res) => {
    try {
        const marketData = await fetchMarketData(); // Assuming fetchMarketData is defined in marketAnalysis.js
        res.json({ success: true, marketData });
    } catch (error) {
        logger.error(`Error fetching market data: ${error.message}`);
        res.status(500).json({ success: false, message: error.message });
    }
});

// Start the API server
const PORT = process.env.API_PORT || 3000;
app.listen(PORT, () => {
    logger.info(`API Gateway listening on port ${PORT}`);
});

module.exports = app; // Export the app for testing purposes
