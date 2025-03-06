const express = require('express');
const router = express.Router();
const merchantController = require('../controllers/merchantController');

// Route to add a new merchant
router.post('/add', merchantController.addMerchant);

// Route to get all merchants
router.get('/', merchantController.getMerchants);

// Route to convert Pi to GCV
router.post('/convert', merchantController.convertPiToGCV);

module.exports = router;
