// src/api/index.js

const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { deposit, convert, checkBalance } = require('./controllers/conversionController');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Routes
app.post('/api/deposit', deposit);
app.post('/api/convert', convert);
app.get('/api/balance', checkBalance);

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
