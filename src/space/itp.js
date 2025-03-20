// itp.js - Interplanetary Transaction Protocol

const crypto = require('crypto');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

class InterplanetaryTransactionProtocol {
    constructor() {
        this.transactions = [];
        this.nodeId = uuidv4(); // Unique identifier for this node
        this.peers = []; // List of peer nodes
        this.blockchain = []; // Simple blockchain to store confirmed transactions
        this.logger = this.createLogger();
    }

    // Create a logger for logging events
    createLogger() {
        return {
            log: (message) => {
                const timestamp = new Date().toISOString();
                console.log(`[${timestamp}] ${message}`);
                fs.appendFileSync('itp.log', `[${timestamp}] ${message}\n`);
            }
        };
    }

    // Generate a secure hash for transaction data
    generateHash(data) {
        return crypto.createHash('sha256').update(JSON.stringify(data)).digest('hex');
    }

    // Create a new transaction
    createTransaction(sender, receiver, amount, conditions = null) {
        const transaction = {
            id: uuidv4(),
            sender,
            receiver,
            amount,
            conditions,
            timestamp: Date.now(),
            status: 'pending',
        };

        transaction.hash = this.generateHash(transaction);
        this.transactions.push(transaction);
        this.logger.log(`Transaction created: ${JSON.stringify(transaction)}`);
        return transaction;
    }

    // Validate a transaction
    validateTransaction(transaction) {
        const { sender, receiver, amount, hash } = transaction;
        const validHash = this.generateHash({ sender, receiver, amount, conditions: transaction.conditions, timestamp: transaction.timestamp });

        return hash === validHash && amount > 0;
    }

    // Broadcast transaction to other nodes
    async broadcastTransaction(transaction) {
        const promises = this.peers.map(node => {
            return axios.post(`${node}/transactions`, transaction)
                .catch(err => this.logger.log(`Failed to send transaction to ${node}: ${err.message}`));
        });

        return Promise.all(promises);
    }

    // Handle incoming transactions
    async handleIncomingTransaction(transaction) {
        if (this.validateTransaction(transaction)) {
            this.transactions.push(transaction);
            this.logger.log('Transaction added: ' + JSON.stringify(transaction));
            await this.broadcastTransaction(transaction);
            this.addToBlockchain(transaction); // Add to blockchain after validation
        } else {
            this.logger.log('Invalid transaction: ' + JSON.stringify(transaction));
        }
    }

    // Add transaction to blockchain
    addToBlockchain(transaction) {
        this.blockchain.push(transaction);
        this.logger.log('Transaction added to blockchain: ' + JSON.stringify(transaction));
    }

    // Fetch peer nodes (stub for demonstration)
    async getPeerNodes() {
        // In a real implementation, this would fetch the list of peer nodes from a registry
        return ['http://node1.example.com', 'http://node2.example.com'];
    }

    // Simulate interplanetary communication delay
    async simulateCommunicationDelay() {
        const delay = Math.floor(Math.random() * 5000); // Random delay up to 5 seconds
        return new Promise(resolve => setTimeout(resolve, delay));
    }

    // Get all transactions
    getAllTransactions() {
        return this.transactions;
    }

    // Get blockchain
    getBlockchain() {
        return this.blockchain;
    }

    // Add peer node
    addPeer(node) {
        if (!this.peers.includes(node)) {
            this.peers.push(node);
            this.logger.log(`Peer added: ${node}`);
        }
    }
}

// Example usage
(async () => {
    const itp = new InterplanetaryTransactionProtocol();

    // Add peers (in a real scenario, this would be dynamic)
    itp.addPeer('http://node1.example.com');
    itp.addPeer('http://node2.example.com');

    // Create a new transaction
    const transaction = itp.createTransaction('PlanetA', 'PlanetB', 100, { condition: 'ifPlanetBIsReady' });
    console.log('Created transaction:', transaction);

    // Simulate communication delay before handling the transaction
    await itp.simulateCommunicationDelay();
    
    // Handle the transaction (simulate receiving it)
    await itp.handleIncomingTransaction(transaction);

    // Retrieve all transactions
    const allTransactions = itp.getAllTransactions();
    console.log('All transactions:', allTransactions);

    // Retrieve blockchain
    const blockchain = itp.getBlockchain();
    console.log('Blockchain:', blockchain);
})();

module.exports = InterplanetaryTransactionProtocol;
