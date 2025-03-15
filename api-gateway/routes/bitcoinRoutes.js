// stable-pi-core/api-gateway/routes/bitcoinRoutes.js

const express = require('express');
const BitcoinAdapter = require('../adapters/bitcoinAdapter');
const authMiddleware = require('../middleware/authMiddleware');

const router = express.Router();
const bitcoinAdapter = new BitcoinAdapter(process.env.BITCOIN_API_URL || 'https://api.blockcypher.com/v1/btc/main');

// Route to fetch Bitcoin block data by block height
router.get('/block/:blockHeight', async (req, res) => {
    const { blockHeight } = req.params;
    try {
        const blockData = await bitcoinAdapter.getBlock(blockHeight);
        res.json(blockData);
    } catch (error) {
        console.error('Error fetching Bitcoin block:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to fetch Bitcoin transaction data by transaction hash
router.get('/transaction/:transactionHash', async (req, res) => {
    const { transactionHash } = req.params;
    try {
        const transactionData = await bitcoinAdapter.getTransaction(transactionHash);
        res.json(transactionData);
    } catch (error) {
        console.error('Error fetching Bitcoin transaction:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to send a Bitcoin transaction
router.post('/send', authMiddleware, async (req, res) => {
    const { rawTransaction } = req.body;

    if (!rawTransaction) {
        return res.status(400).json({ error: 'Raw transaction data is required.' });
    }

    try {
        const txid = await bitcoinAdapter.sendTransaction(rawTransaction);
        res.json({ txid });
    } catch (error) {
        console.error('Error sending Bitcoin transaction:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Route to get the current Bitcoin price (optional)
router.get('/price', async (req, res) => {
    try {
        const price = await bitcoinAdapter.getCurrentPrice();
        res.json({ price });
    } catch (error) {
        console.error('Error fetching Bitcoin price:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

module.exports = router;
