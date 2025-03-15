// stable-pi-core/api-gateway/graphql/resolvers.js

const EthereumAdapter = require('../adapters/ethereumAdapter');
const BitcoinAdapter = require('../adapters/bitcoinAdapter');

// Initialize adapters with the appropriate API URLs
const ethereumAdapter = new EthereumAdapter(process.env.ETHEREUM_API_URL || 'https://api.etherscan.io/api');
const bitcoinAdapter = new BitcoinAdapter(process.env.BITCOIN_API_URL || 'https://api.blockcypher.com/v1/btc/main');

const resolvers = {
    Query: {
        // Ethereum Resolvers
        ethereumBlock: async (_, { blockNumber }) => {
            try {
                const blockData = await ethereumAdapter.getBlock(blockNumber);
                return blockData;
            } catch (error) {
                console.error('Error fetching Ethereum block:', error);
                throw new Error('Failed to fetch Ethereum block');
            }
        },
        ethereumTransaction: async (_, { transactionHash }) => {
            try {
                const transactionData = await ethereumAdapter.getTransaction(transactionHash);
                return transactionData;
            } catch (error) {
                console.error('Error fetching Ethereum transaction:', error);
                throw new Error('Failed to fetch Ethereum transaction');
            }
        },

        // Bitcoin Resolvers
        bitcoinBlock: async (_, { blockHeight }) => {
            try {
                const blockData = await bitcoinAdapter.getBlock(blockHeight);
                return blockData;
            } catch (error) {
                console.error('Error fetching Bitcoin block:', error);
                throw new Error('Failed to fetch Bitcoin block');
            }
        },
        bitcoinTransaction: async (_, { transactionHash }) => {
            try {
                const transactionData = await bitcoinAdapter.getTransaction(transactionHash);
                return transactionData;
            } catch (error) {
                console.error('Error fetching Bitcoin transaction:', error);
                throw new Error('Failed to fetch Bitcoin transaction');
            }
        },
        bitcoinPrice: async () => {
            try {
                const price = await bitcoinAdapter.getCurrentPrice();
                return price;
            } catch (error) {
                console.error('Error fetching Bitcoin price:', error);
                throw new Error('Failed to fetch Bitcoin price');
            }
        },
    },
};

module.exports = resolvers;
