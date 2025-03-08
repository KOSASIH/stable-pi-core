const mongoose = require('mongoose');

// Define the user schema
const userSchema = new mongoose.Schema({
    address: {
        type: String,
        required: true,
        unique: true, // Ensure each address is unique
        index: true, // Create an index for faster queries
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
    balance: {
        type: Number,
        default: 0,
    },
    stakingBalance: {
        type: Number,
        default: 0,
    },
});

// Method to update user balance
userSchema.methods.updateBalance = async function(amount) {
    this.balance += amount;
    await this.save();
};

// Method to update user staking balance
userSchema.methods.updateStakingBalance = async function(amount) {
    this.stakingBalance += amount;
    await this.save();
};

// Method to reset user staking balance
userSchema.methods.resetStakingBalance = async function() {
    this.stakingBalance = 0;
    await this.save();
};

// Create the User model
const User = mongoose.model('User', userSchema);

module.exports = User;
