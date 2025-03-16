// stable-pi-core/api-gateway/routes/avalancheRoutes.js

const express = require('express');
const router = express.Router();
const avalancheAdapter = require('../adapters/avalancheAdapter');

// Middleware for error handling
const handleError = (res, error) => {
    console.error(error);
    res.status(500).json({ error: error.message });
};

// Get balance
router.get('/balance/:address', async (req, res) => {
    try {
        const balance = await avalancheAdapter.getBalance(req.params.address);
        res.json({ balance });
    } catch (error) {
        handleError(res, error);
    }
});

// Send AVAX
router.post('/send', async (req, res) => {
    const { fromAddress, toAddress, amount, senderPrivateKey } = req.body;
    try {
        const txId = await avalancheAdapter.sendAVAX(fromAddress, toAddress, amount, senderPrivateKey);
        res.json({ txId });
    } catch (error) {
        handleError(res, error);
    }
});

// Monitor transaction status
router.get('/transaction/:txId', async (req, res) => {
    try {
        const transactionStatus = await avalancheAdapter.monitorTransaction(req.params.txId);
        res.json(transactionStatus);
    } catch (error) {
        handleError(res, error);
    }
});

// Fetch transaction details
router.get('/transaction/details/:txId', async (req, res) => {
    try {
        const transactionDetails = await avalancheAdapter.getTransactionDetails(req.params.txId);
        res.json(transactionDetails);
    } catch (error) {
        handleError(res, error);
    }
});

// Interact with a smart contract
router.post('/contract/:contractAddress', async (req, res) => {
    const { params, senderPrivateKey } = req.body;
    try {
        const txId = await avalancheAdapter.interactWithContract(req.params.contractAddress, params, senderPrivateKey);
        res.json({ txId });
    } catch (error) {
        handleError(res, error);
    }
});

// Batch transaction endpoint
router.post('/send/batch', async (req, res) => {
    const { transactions, senderPrivateKey } = req.body; // transactions should be an array of { toAddress, amount }
    try {
        const txIds = [];
        for (const tx of transactions) {
            const txId = await avalancheAdapter.sendAVAX(req.body.fromAddress, tx.toAddress, tx.amount, senderPrivateKey);
            txIds.push(txId);
        }
        res.json({ txIds });
    } catch (error) {
        handleError(res, error);
    }
});

// Export the router
module.exports = router;
