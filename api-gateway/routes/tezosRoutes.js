// stable-pi-core/api-gateway/routes/tezosRoutes.js

const express = require('express');
const router = express.Router();
const tezosAdapter = require('../adapters/tezosAdapter');

// Middleware for error handling
const handleError = (res, error) => {
    console.error(error);
    res.status(500).json({ error: error.message });
};

// Get balance
router.get('/balance/:address', async (req, res) => {
    try {
        const balance = await tezosAdapter.getBalance(req.params.address);
        res.json({ balance });
    } catch (error) {
        handleError(res, error);
    }
});

// Send XTZ
router.post('/send', async (req, res) => {
    const { fromAddress, toAddress, amount, senderPrivateKey } = req.body;
    try {
        const txHash = await tezosAdapter.sendXTZ(fromAddress, toAddress, amount, senderPrivateKey);
        res.json({ txHash });
    } catch (error) {
        handleError(res, error);
    }
});

// Monitor transaction status
router.get('/transaction/:txHash', async (req, res) => {
    try {
        const transactionStatus = await tezosAdapter.monitorTransaction(req.params.txHash);
        res.json(transactionStatus);
    } catch (error) {
        handleError(res, error);
    }
});

// Fetch transaction details
router.get('/transaction/details/:txHash', async (req, res) => {
    try {
        const transactionDetails = await tezosAdapter.getTransactionDetails(req.params.txHash);
        res.json(transactionDetails);
    } catch (error) {
        handleError(res, error);
    }
});

// Interact with a smart contract
router.post('/contract/:contractAddress', async (req, res) => {
    const { params, senderPrivateKey } = req.body;
    try {
        const txHash = await tezosAdapter.interactWithContract(req.params.contractAddress, params, senderPrivateKey);
        res.json({ txHash });
    } catch (error) {
        handleError(res, error);
    }
});

// Batch transaction endpoint (example)
router.post('/send/batch', async (req, res) => {
    const { transactions, senderPrivateKey } = req.body; // transactions should be an array of { toAddress, amount }
    try {
        const txHashes = [];
        for (const tx of transactions) {
            const txHash = await tezosAdapter.sendXTZ(req.body.fromAddress, tx.toAddress, tx.amount, senderPrivateKey);
            txHashes.push(txHash);
        }
        res.json({ txHashes });
    } catch (error) {
        handleError(res, error);
    }
});

// Export the router
module.exports = router;
