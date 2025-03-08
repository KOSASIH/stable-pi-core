// config/server.js

const express = require('express');
const connectDB = require('./db'); // Import the database connection
const { web3, getLatestBlock } = require('./web3'); // Import Web3 configuration

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(express.json()); // Parse JSON bodies

// Connect to the database
connectDB();

// Sample route to get the latest block number
app.get('/api/latest-block', async (req, res) => {
    try {
        const blockNumber = await getLatestBlock();
        res.json({ blockNumber });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch latest block' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
