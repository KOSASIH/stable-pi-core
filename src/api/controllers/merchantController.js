const Merchant = require('../../models/Merchant');
const conversionService = require('../../services/conversionService'); // Ensure this exists for conversion

exports.addMerchant = async (req, res) => {
    const { name, walletAddress, items } = req.body;

    try {
        const newMerchant = new Merchant({ name, walletAddress, items });
        await newMerchant.save();
        res.status(201).json({ message: 'Merchant added successfully', merchant: newMerchant });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

exports.getMerchants = async (req, res) => {
    try {
        const merchants = await Merchant.find();
        res.status(200).json(merchants);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

exports.convertPiToGCV = async (req, res) => {
    const { amountInPi, merchantId } = req.body;

    try {
        const merchant = await Merchant.findById(merchantId);
        if (!merchant) {
            return res.status(404).json({ error: 'Merchant not found' });
        }

        const gcvValue = await conversionService.convertPiToGCV(amountInPi); // Implement conversion logic
        res.status(200).json({ gcvValue });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};
