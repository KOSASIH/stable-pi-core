// stable-pi-core/api-gateway/routes/litecoinRoutes.js

const express = require('express');
const router = express.Router();
const litecoinAdapter = require('../adapters/litecoinAdapter');

// Middleware for error handling
const handleError = (res, error) => {
    console.error(error);
    res.status(500).json({ error: error.message });
};

// Get balance
router.get('/balance/:address', async (req, res) => {
    try {
        const balance = await litecoinAdapter.getBalance(req.params.address);
        res.json({ balance });
    } catch (error) {
        handleError(res, error);
    }
});

// Send LTC
router.post('/send', async (req, res) => {
    const { fromAddress, toAddress, amount, senderPrivateKey } = req.body;
    try {
        const txId = await litecoinAdapter.sendLTC(fromAddress, toAddress, amount, senderPrivateKey);
        res.json({ txId });
    } catch (error) {
        handleError(res, error);
    }
});

// Monitor transaction status
router.get('/transaction/:txId', async (req, res) => {
    try {
        const transactionStatus = await litecoinAdapter.monitorTransaction(req.params.txId);
        res.json(transactionStatus);
    } catch (error) {
        handleError(res, error);
    }
});

// Fetch transaction details
router.get('/transaction/details/:txId', async (req, res) => {
    try {
        const transactionDetails = await litecoinAdapter.getTransactionDetails(req.params.txId);
        res.json(transactionDetails);
    } catch (error) {
        handleError(res, error);
    }
});

// Interact with a smart contract (if applicable)
router.post('/contract/:contractAddress', async (req, res) => {
    const { params } = req.body;
    try {
        // Note: Litecoin does not have traditional smart contracts like Ethereum.
        // This is a placeholder for any future functionality related to payment channels or similar features.
        throw new Error('Smart contract interaction is not applicable for Litecoin.');
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
            const txId = await litecoinAdapter.sendLTC(req.body.fromAddress, tx.toAddress, tx.amount, senderPrivateKey);
            txIds.push(txId);
        }
        res.json({ txIds });
    } catch (error) {
        handleError(res, error);
    }
});

// Export the router
module.exports = router;
