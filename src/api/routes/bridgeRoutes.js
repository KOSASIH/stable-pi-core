const express = require('express');
const router = express.Router();
const bridgeController = require('../controllers/bridgeController');

// Route to deposit Pi Coin to the bridge
router.post('/deposit', bridgeController.deposit);

// Route to withdraw Pi Coin from the bridge
router.post('/withdraw', bridgeController.withdraw);

// Route to bridge Pi Coin to another chain
router.post('/bridge', bridgeController.bridge);

module.exports = router;
