// stable-pi-core/api-gateway/routes/rippleRoutes.js

const express = require('express');
const router = express.Router();
const rippleAdapter = require('../adapters/rippleAdapter');

// Middleware for error handling
const handleError = (res, error) => {
    console.error(error);
    res.status(500).json({ error: error.message });
};

// Get balance
router.get('/balance/:address', async (req, res) => {
    try {
        const balance = await rippleAdapter.getBalance(req.params.address);
        res.json({ balance });
    } catch (error) {
        handleError(res, error);
    }
});

// Send XRP
router.post('/send', async (req, res) => {
    const { fromAddress, toAddress, amount, senderSecret } = req.body;
    try {
        const txHash = await rippleAdapter.sendXRP(fromAddress, toAddress, amount, senderSecret);
        res.json({ txHash });
    } catch (error) {
        handleError(res, error);
    }
});

// Monitor transaction status
router.get('/transaction/:txHash', async (req, res) => {
    try {
        const transactionStatus = await rippleAdapter.monitorTransaction(req.params.txHash);
        res.json(transactionStatus);
    } catch (error) {
        handleError(res, error);
    }
});

// Fetch transaction details
router.get('/transaction/details/:txHash', async (req, res) => {
    try {
        const transactionDetails = await rippleAdapter.getTransactionDetails(req.params.txHash);
        res.json(transactionDetails);
    } catch (error) {
        handleError(res, error);
    }
});

// Interact with a smart contract (if applicable)
router.post('/contract/:contractAddress', async (req, res) => {
    const { params } = req.body;
    try {
        // Note: Ripple does not have traditional smart contracts like Ethereum.
        // This is a placeholder for any future functionality related to payment channels or similar features.
        throw new Error('Smart contract interaction is not applicable for Ripple.');
    } catch (error) {
        handleError(res, error);
    }
});

// Batch transaction endpoint
router.post('/send/batch', async (req, res) => {
    const { transactions, senderSecret } = req.body; // transactions should be an array of { toAddress, amount }
    try {
        const txHashes = [];
        for (const tx of transactions) {
            const txHash = await rippleAdapter.sendXRP(req.body.fromAddress, tx.toAddress, tx.amount, senderSecret);
            txHashes.push(txHash);
        }
        res.json({ txHashes });
    } catch (error) {
        handleError(res, error);
    }
});

// Export the router
module.exports = router;
