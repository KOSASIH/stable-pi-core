const mongoose = require('mongoose');

const transactionSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User ',
        required: true,
    },
    type: {
        type: String,
        enum: ['deposit', 'conversion'],
        required: true,
    },
    amount: {
        type: Number,
        required: true,
    },
    convertedAmount: {
        type: Number,
        default: 0,
    },
    fee: {
        type: Number,
        default: 0,
    },
    transactionHash: {
        type: String,
        required: true,
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
});

// Middleware to set createdAt timestamp
transactionSchema.pre('save', function (next) {
    this.createdAt = Date.now();
    next();
});

const Transaction = mongoose.model('Transaction', transactionSchema);

module.exports = Transaction;
