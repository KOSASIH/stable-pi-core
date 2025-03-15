// stable-pi-core/api-gateway/routes/ethereumRoutes.js

const express = require('express');
const EthereumAdapter = require('../adapters/ethereumAdapter');
const authMiddleware = require('../middleware/authMiddleware');

const router = express.Router();
const ethereumAdapter = new EthereumAdapter(process.env.ETHEREUM_API_URL || 'https://api.etherscan.io/api');

// Route to fetch Ethereum block data by block number
router.get('/block/:blockNumber', async (req, res) => {
    const { blockNumber } = req.params;
    try {
        const blockData = await ethereumAdapter.getBlock(blockNumber);
        res.json(blockData);
    } catch (error) {
        console.error('Error fetching Ethereum block:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to fetch Ethereum transaction data by transaction hash
router.get('/transaction/:transactionHash', async (req, res) => {
    const { transactionHash } = req.params;
    try {
        const transactionData = await ethereumAdapter.getTransaction(transactionHash);
        res.json(transactionData);
    } catch (error) {
        console.error('Error fetching Ethereum transaction:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to call a method on a smart contract
router.post('/contract/:contractAddress/call', authMiddleware, async (req, res) => {
    const { contractAddress } = req.params;
    const { methodName, params } = req.body;

    if (!methodName || !Array.isArray(params)) {
        return res.status(400).json({ error: 'Method name and parameters are required.' });
    }

    try {
        const result = await ethereumAdapter.callContractMethod(contractAddress, methodName, params);
        res.json(result);
    } catch (error) {
        console.error('Error calling contract method:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to get the current Ethereum price (optional)
router.get('/price', async (req, res) => {
    try {
        const price = await ethereumAdapter.getCurrentPrice();
        res.json({ price });
    } catch (error) {
        console.error('Error fetching Ethereum price:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

module.exports = router;
