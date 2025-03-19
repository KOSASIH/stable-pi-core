const mongoose = require('mongoose');

// Define the contribution schema
const contributionSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User', // Reference to the User model
        required: true,
    },
    amount: {
        type: Number,
        required: true,
        min: 0, // Ensure the amount is non-negative
    },
    contributionDate: {
        type: Date,
        default: Date.now,
    },
});

// Method to get contributions by user
contributionSchema.statics.getContributionsByUser = async function(userId) {
    return await this.find({ user: userId }).sort({ contributionDate: -1 }); // Sort contributions by date
};

// Method to get total contributions by user
contributionSchema.statics.getTotalContributionsByUser = async function(userId) {
    const contributions = await this.aggregate([
        { $match: { user: userId } },
        { $group: { _id: null, total: { $sum: "$amount" } } }
    ]);
    return contributions.length > 0 ? contributions[0].total : 0; // Return total or 0 if no contributions
};

// Create the Contribution model
const Contribution = mongoose.model('Contribution', contributionSchema);

module.exports = Contribution;
