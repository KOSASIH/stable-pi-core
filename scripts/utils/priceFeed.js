// scripts/utils/priceFeed.js

const axios = require('axios');

const CHAINLINK_PRICE_FEED_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd';

async function fetchPrice() {
    try {
        const response = await axios.get(CHAINLINK_PRICE_FEED_URL);
        const price = response.data.ethereum.usd;
        console.log(`Current ETH price: $${price}`);
        return price;
    } catch (error) {
        console.error('Error fetching price:', error);
        throw error;
    }
}

module.exports = { fetchPrice };
