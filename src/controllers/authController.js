const Authy = require('authy');
const config = require('../config/config');
const authy = new Authy(config.authyApiKey);

// Register a new user for MFA
exports.registerUser  = (req, res) => {
    const { email, phone, countryCode } = req.body;

    // Validate input
    if (!email || !phone || !countryCode) {
        return res.status(400).json({ success: false, message: 'Email, phone, and country code are required.' });
    }

    authy.register_user(email, phone, countryCode, (err, response) => {
        if (err) {
            return res.status(500).json({ success: false, message: 'Error registering user', error: err });
        }

        if (response && response.success) {
            res.json({ success: true, userId: response.user.id });
        } else {
            res.status(400).json({ success: false, message: 'Registration failed', error: response });
        }
    });
};

// Send an SMS with the MFA token
exports.sendSms = (req, res) => {
    const { userId } = req.body;

    // Validate input
    if (!userId) {
        return res.status(400).json({ success: false, message: 'User  ID is required.' });
    }

    authy.send_sms(userId, true, (err, response) => {
        if (err) {
            return res.status(500).json({ success: false, message: 'Error sending SMS', error: err });
        }

        if (response && response.success) {
            res.json({ success: true, message: 'SMS sent successfully' });
        } else {
            res.status(400).json({ success: false, message: 'Failed to send SMS', error: response });
        }
    });
};

// Verify the MFA token
exports.verifyToken = (req, res) => {
    const { userId, token } = req.body;

    // Validate input
    if (!userId || !token) {
        return res.status(400).json({ success: false, message: 'User  ID and token are required.' });
    }

    authy.verify(userId, token, (err, response) => {
        if (err) {
            return res.status(500).json({ success: false, message: 'Error verifying token', error: err });
        }

        if (response && response.success) {
            res.json({ success: true, message: 'Token verified successfully' });
        } else {
            res.status(400).json({ success: false, message: 'Token verification failed', error: response });
        }
    });
};
