// stable-pi-core/api-gateway/adapters/ethereumAdapter.js

const axios = require('axios');
const EventEmitter = require('events');

class EthereumAdapter extends EventEmitter {
    constructor(apiUrl) {
        this.apiUrl = apiUrl || process.env.ETHEREUM_API_URL; // Use environment variable or default
        this.cache = new Map(); // Simple in-memory cache
    }

    // Function to fetch block data
    async getBlock(blockNumber) {
        if (this.cache.has(`block_${blockNumber}`)) {
            console.log(`Fetching block ${blockNumber} from cache.`);
            return this.cache.get(`block_${blockNumber}`);
        }

        try {
            const response = await axios.get(`${this.apiUrl}/api?module=proxy&action=eth_getBlockByNumber&tag=${blockNumber}&boolean=true`);
            const blockData = response.data.result;

            if (blockData) {
                this.cache.set(`block_${blockNumber}`, blockData); // Cache the result
                this.emit('blockFetched', blockNumber, blockData); // Emit event
                return blockData;
            } else {
                throw new Error('Block not found');
            }
        } catch (error) {
            console.error('Error fetching block:', error);
            throw new Error('Failed to fetch block');
        }
    }

    // Function to fetch transaction data
    async getTransaction(transactionHash) {
        if (this.cache.has(`transaction_${transactionHash}`)) {
            console.log(`Fetching transaction ${transactionHash} from cache.`);
            return this.cache.get(`transaction_${transactionHash}`);
        }

        try {
            const response = await axios.get(`${this.apiUrl}/api?module=proxy&action=eth_getTransactionByHash&txhash=${transactionHash}`);
            const transactionData = response.data.result;

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

    // Function to interact with a smart contract
    async callContractMethod(contractAddress, methodName, params) {
        try {
            const response = await axios.post(this.apiUrl, {
                jsonrpc: "2.0",
                method: "eth_call",
                params: [{
                    to: contractAddress,
                    data: this.encodeMethod(methodName, params)
                }, "latest"],
                id: 1
            });

            const result = response.data.result;
            if (result) {
                this.emit('contractMethodCalled', contractAddress, methodName, result); // Emit event
                return result;
            } else {
                throw new Error('Failed to call contract method');
            }
        } catch (error) {
            console.error('Error calling contract method:', error);
            throw new Error('Failed to call contract method');
        }
    }

    // Helper function to encode method call
    encodeMethod(methodName, params) {
        // This is a placeholder for actual ABI encoding logic
        // You would typically use a library like ethers.js or web3.js to encode the method call
        return `0x${methodName}${params.map(param => param.toString(16).padStart(64, '0')).join('')}`;
    }
}

module.exports = EthereumAdapter;
