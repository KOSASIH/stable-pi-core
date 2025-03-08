// config/web3.js

const Web3 = require('web3');

// Replace with your Ethereum node URL (e.g., Infura, Alchemy, or local node)
const providerURL = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'; // Replace with your Infura project ID

const web3 = new Web3(new Web3.providers.HttpProvider(providerURL));

// Example function to get the latest block number
const getLatestBlock = async () => {
    try {
        const blockNumber = await web3.eth.getBlockNumber();
        console.log('Latest Ethereum Block Number:', blockNumber);
        return blockNumber;
    } catch (error) {
        console.error('Error fetching latest block:', error);
        throw error; // Rethrow the error for further handling
    }
};

module.exports = {
    web3,
    getLatestBlock,
};
