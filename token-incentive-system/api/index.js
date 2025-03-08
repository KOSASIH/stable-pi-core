const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const userController = require('./userController');
const stakingController = require('./stakingController');
const tokenController = require('./tokenController');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors()); // Enable CORS for all routes
app.use(bodyParser.json()); // Parse JSON bodies

// Routes
app.use('/api/users', userController);
app.use('/api/staking', stakingController);
app.use('/api/tokens', tokenController);

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.status(200).json({ status: 'OK', message: 'API is running smoothly' });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});
