const mongoose = require('mongoose');

const merchantSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    walletAddress: {
        type: String,
        required: true,
    },
    items: [
        {
            name: String,
            priceInPi: Number,
            priceInGCV: Number, // Price in GCV
        },
    ],
});

// Method to add an item with price conversion to GCV
merchantSchema.methods.addItem = function(item) {
    this.items.push({
        name: item.name,
        priceInPi: item.priceInPi,
        priceInGCV: item.priceInPi * 314159.00, // Convert price to GCV
    });
};

module.exports = mongoose.model('Merchant', merchantSchema);
