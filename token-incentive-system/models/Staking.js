const mongoose = require('mongoose');

// Define the staking schema
const stakingSchema = new mongoose.Schema({
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User', // Reference to the User model
        required: true,
    },
    amountStaked: {
        type: Number,
        required: true,
        min: 0, // Ensure the amount is non-negative
    },
    stakingDate: {
        type: Date,
        default: Date.now,
    },
    rewardsEarned: {
        type: Number,
        default: 0,
    },
});

// Method to get staking records by user
stakingSchema.statics.getStakingRecordsByUser = async function(userId) {
    return await this.find({ user: userId }).sort({ stakingDate: -1 }); // Sort staking records by date
};

// Method to get total staked amount by user
stakingSchema.statics.getTotalStakedByUser = async function(userId) {
    const stakingRecords = await this.aggregate([
        { $match: { user: userId } },
        { $group: { _id: null, totalStaked: { $sum: "$amountStaked" } } }
    ]);
    return stakingRecords.length > 0 ? stakingRecords[0].totalStaked : 0; // Return total or 0 if no records
};

// Create the Staking model
const Staking = mongoose.model('Staking', stakingSchema);

module.exports = Staking;
