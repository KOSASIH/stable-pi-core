const express = require('express');
const authController = require('../controllers/authController');

const router = express.Router();

// Route for user registration
router.post('/register', authController.registerUser );

// Route for sending SMS with MFA token
router.post('/send-sms', authController.sendSms);

// Route for verifying the MFA token
router.post('/verify', authController.verifyToken);

module.exports = router;
