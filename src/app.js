const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');
const kycRoutes = require('./api/routes/kycRoutes');
const walletService = require('./services/walletService');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/stable-pi-core', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.error('MongoDB connection error:', err));

// Use KYC routes
app.use('/api/kyc', kycRoutes);

// Endpoint to connect wallet and get balance
app.post('/api/wallet/connect', async (req, res) => {
    try {
        const account = await walletService.connectWallet();
        const balance = await walletService.getBalance(account);
        res.status(200).json({ account, balance });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
