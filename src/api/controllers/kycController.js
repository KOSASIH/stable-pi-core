const KYC = require('../../models/KYC');

exports.submitKYC = async (req, res) => {
    const { userId, fullName, idNumber } = req.body;

    try {
        const existingKYC = await KYC.findOne({ userId });
        if (existingKYC) {
            return res.status(400).json({ message: 'KYC already submitted for this user.' });
        }

        const newKYC = new KYC({ userId, fullName, idNumber });
        await newKYC.save();
        res.status(201).json({ message: 'KYC submitted successfully' });
    } catch (error) {
        console.error('KYC submission failed:', error);
        res.status(500).json({ error: 'KYC submission failed' });
    }
};

exports.verifyKYC = async (req, res) => {
    const { userId } = req.body;

    try {
        const kycRecord = await KYC.findOne({ userId });
        if (!kycRecord) {
            return res.status(404).json({ message: 'KYC record not found' });
        }

        kycRecord.verified = true;
        kycRecord.verificationDate = new Date();
        await kycRecord.save();
        res.status(200).json({ message: 'KYC verified successfully' });
    } catch (error) {
        console.error('KYC verification failed:', error);
        res.status(500).json({ error: 'KYC verification failed' });
    }
};
