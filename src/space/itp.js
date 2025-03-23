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
        if (amount <= 0) {
            throw new Error('Transaction amount must be greater than zero.');
        }

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

    // Remove peer node
    removePeer(node) {
        this.peers = this.peers.filter(peer => peer !== node);
        this.logger.log(`Peer removed: ${node}`);
    }

    // Get the list of peers
    getPeers() {
        return this.peers;
    }
}

// Interdimensional Transaction Gateway (ITG) extending ITP
class InterdimensionalTransactionGateway extends InterplanetaryTransactionProtocol {
    constructor() {
        super();
    }

    // Create a new interdimensional transaction
    createInterdimensionalTransaction(sender, receiver, amount, conditions = null) {
        const transaction = this.createTransaction(sender, receiver, amount, conditions);
        transaction.type = 'interdimensional'; // Mark as interdimensional
        this.logger.log(`Interdimensional transaction created: ${JSON.stringify(transaction)}`);
        return transaction;
    }

    // Handle incoming interdimensional transactions
    async handleIncomingInterdimensionalTransaction(transaction) {
        this.logger.log('Handling incoming interdimensional transaction...');
        await this.handleIncomingTransaction(transaction);
    }

    // Simulate interdimensional communication delay
    async simulateInterdimensionalCommunicationDelay() {
        const delay = Math.floor(Math.random() * 10000); // Random delay up to 10 seconds
        return new Promise(resolve => setTimeout(resolve, delay));
    }
}

// Example usage
(async () => {
    const itg = new InterdimensionalTransactionGateway();

    // Add peers (in a real scenario, this would be dynamic)
    itg.addPeer('http://node1.example.com');
    itg.addPeer('http://node2.example.com');

    // Create a new interdimensional transaction
    try {
        const transaction = itg.createInterdimensionalTransaction('PlanetA', 'PlanetB', 100, { condition: 'ifPlanetBIsReady' });
        console.log('Created interdimensional transaction:', transaction);

        // Simulate communication delay before handling the transaction
        await itg.simulateInterdimensionalCommunicationDelay();
        
        // Handle the transaction (simulate receiving it)
        await itg.handleIncomingInterdimensionalTransaction(transaction);

        // Retrieve all transactions
        const allTransactions = itg.getAllTransactions();
        console.log('All transactions:', allTransactions);

        // Retrieve blockchain
        const blockchain = itg.getBlockchain();
        console.log('Blockchain:', blockchain);
    } catch (error) {
        console.error('Error:', error.message);
    }
})();

module.exports = InterdimensionalTransactionGateway;
