const mongoose = require('mongoose');

const kycSchema = new mongoose.Schema({
    userId: {
        type: String,
        required: true,
        unique: true,
    },
    fullName: {
        type: String,
        required: true,
    },
    idNumber: {
        type: String,
        required: true,
    },
    verified: {
        type: Boolean,
        default: false,
    },
    verificationDate: {
        type: Date,
    },
});

module.exports = mongoose.model('KYC', kycSchema);
