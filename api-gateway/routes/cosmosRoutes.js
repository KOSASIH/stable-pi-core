// stable-pi-core/api-gateway/routes/cosmosRoutes.js

const express = require('express');
const router = express.Router();
const cosmosAdapter = require('../adapters/cosmosAdapter');

// Middleware for error handling
const handleError = (res, error) => {
    console.error(error);
    res.status(500).json({ error: error.message });
};

// Get balance
router.get('/balance/:address', async (req, res) => {
    try {
        const balance = await cosmosAdapter.getBalance(req.params.address);
        res.json({ balance });
    } catch (error) {
        handleError(res, error);
    }
});

// Send tokens
router.post('/send', async (req, res) => {
    const { fromAddress, toAddress, amount, denom, senderMnemonic } = req.body;
    try {
        const txHash = await cosmosAdapter.sendTokens(fromAddress, toAddress, amount, denom, senderMnemonic);
        res.json({ txHash });
    } catch (error) {
        handleError(res, error);
    }
});

// Monitor transaction status
router.get('/transaction/:txHash', async (req, res) => {
    try {
        const transactionStatus = await cosmosAdapter.monitorTransaction(req.params.txHash);
        res.json(transactionStatus);
    } catch (error) {
        handleError(res, error);
    }
});

// Fetch transaction details
router.get('/transaction/details/:txHash', async (req, res) => {
    try {
        const transactionDetails = await cosmosAdapter.getTransactionDetails(req.params.txHash);
        res.json(transactionDetails);
    } catch (error) {
        handleError(res, error);
    }
});

// Interact with a smart contract (CosmWasm)
router.post('/contract/:contractAddress', async (req, res) => {
    const { params, senderMnemonic } = req.body;
    try {
        const txHash = await cosmosAdapter.interactWithContract(req.params.contractAddress, params, senderMnemonic);
        res.json({ txHash });
    } catch (error) {
        handleError(res, error);
    }
});

// Batch transaction endpoint
router.post('/send/batch', async (req, res) => {
    const { transactions, senderMnemonic } = req.body; // transactions should be an array of { toAddress, amount, denom }
    try {
        const txHashes = [];
        for (const tx of transactions) {
            const txHash = await cosmosAdapter.sendTokens(req.body.fromAddress, tx.toAddress, tx.amount, tx.denom, senderMnemonic);
            txHashes.push(txHash);
        }
        res.json({ txHashes });
    } catch (error) {
        handleError(res, error);
    }
});

// Export the router
module.exports = router;
