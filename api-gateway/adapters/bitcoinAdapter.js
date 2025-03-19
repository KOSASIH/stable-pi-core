// stable-pi-core/api-gateway/adapters/bitcoinAdapter.js

const axios = require('axios');
const EventEmitter = require('events');

class BitcoinAdapter extends EventEmitter {
    constructor(apiUrl) {
        super();
        this.apiUrl = apiUrl || process.env.BITCOIN_API_URL; // Use environment variable or default
        this.cache = new Map(); // Simple in-memory cache
    }

    // Function to fetch block data by block height
    async getBlock(blockHeight) {
        if (this.cache.has(`block_${blockHeight}`)) {
            console.log(`Fetching block ${blockHeight} from cache.`);
            return this.cache.get(`block_${blockHeight}`);
        }

        try {
            const response = await axios.get(`${this.apiUrl}/block-height/${blockHeight}?format=json`);
            const blockData = response.data;

            if (blockData) {
                this.cache.set(`block_${blockHeight}`, blockData); // Cache the result
                this.emit('blockFetched', blockHeight, blockData); // Emit event
                return blockData;
            } else {
                throw new Error('Block not found');
            }
        } catch (error) {
            console.error('Error fetching block:', error);
            throw new Error('Failed to fetch block');
        }
    }

    // Function to fetch transaction data by transaction hash
    async getTransaction(transactionHash) {
        if (this.cache.has(`transaction_${transactionHash}`)) {
            console.log(`Fetching transaction ${transactionHash} from cache.`);
            return this.cache.get(`transaction_${transactionHash}`);
        }

        try {
            const response = await axios.get(`${this.apiUrl}/tx/${transactionHash}?format=json`);
            const transactionData = response.data;

            if (transactionData) {
                this.cache.set(`transaction_${transactionHash}`, transactionData); // Cache the result
                this.emit('transactionFetched', transactionHash, transactionData); // Emit event
                return transactionData;
            } else {
                throw new Error('Transaction not found');
            }
        } catch (error) {
            console.error('Error fetching transaction:', error);
            throw new Error('Failed to fetch transaction');
        }
    }

    // Function to send a transaction
    async sendTransaction(rawTransaction) {
        try {
            const response = await axios.post(`${this.apiUrl}/tx/send`, {
                tx: rawTransaction
            });
            const result = response.data;

            if (result && result.txid) {
                this.emit('transactionSent', result.txid); // Emit event
                return result.txid;
            } else {
                throw new Error('Failed to send transaction');
            }
        } catch (error) {
            console.error('Error sending transaction:', error);
            throw new Error('Failed to send transaction');
        }
    }

    // Function to get the current Bitcoin price (optional)
    async getCurrentPrice() {
        try {
            const response = await axios.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json');
            return response.data.bpi.USD.rate_float; // Return the current price in USD
        } catch (error) {
            console.error('Error fetching Bitcoin price:', error);
            throw new Error('Failed to fetch Bitcoin price');
        }
    }
}

module.exports = BitcoinAdapter;
