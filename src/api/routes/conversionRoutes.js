// src/api/routes/conversionRoutes.js

const express = require('express');
const router = express.Router();
const { deposit, convert, checkBalance } = require('../controllers/conversionController');

// Route to deposit Pi Coin
router.post('/deposit', deposit);

// Route to convert Pi Coin to market price
router.post('/convert', convert);

// Route to check user balance
router.get('/balance', checkBalance);

module.exports = router;
