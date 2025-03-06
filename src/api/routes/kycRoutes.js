const express = require('express');
const router = express.Router();
const kycController = require('../controllers/kycController');

// Route to submit KYC
router.post('/submit', kycController.submitKYC);

// Route to verify KYC
router.post('/verify', kycController.verifyKYC);

module.exports = router;
