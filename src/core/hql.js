// src/core/hql.js

import TemporalTransactionRewind from './ttr';
import AccessControl from './accessControl';
import Transaction from './transaction';
import { generateQuantumHash, validateQuantumSignature } from './utils';

class HolographicQuantumLedger {
    constructor() {
        this.transactions = [];
        this.ttr = new TemporalTransactionRewind(this);
        this.accessControl = new AccessControl();
    }

    // Method to create a new transaction
    createTransaction(data, user) {
        if (!this.accessControl.isAuthorized(user)) {
            throw new Error("Unauthorized access to create transaction.");
        }

        const transaction = new Transaction(data);
        transaction.hash = this.generateTransactionHash(transaction);
        this.transactions.push(transaction);
        return transaction;
    }

    // Method to retrieve a transaction by ID
    getTransaction(transactionId) {
        return this.transactions.find(tx => tx.id === transactionId) || null;
    }

    // Method to update a transaction
    updateTransaction(updatedTransaction) {
        const index = this.transactions.findIndex(tx => tx.id === updatedTransaction.id);
        if (index === -1) {
            throw new Error("Transaction not found.");
        }
        this.transactions[index] = updatedTransaction;
    }

    // Method to rewind a transaction to a previous state
    rewindTransaction(transactionId, targetTimestamp, user) {
        return this.ttr.rewindTransaction(transactionId, targetTimestamp, user);
    }

    // Method to generate a quantum hash for a transaction
    generateTransactionHash(transaction) {
        return generateQuantumHash(transaction);
    }

    // Method to validate a transaction's signature
    validateTransactionSignature(transaction) {
        return validateQuantumSignature(transaction);
    }

    // Method to get all transactions
    getAllTransactions() {
        return this.transactions;
    }

    // Method to clear the ledger (for testing or reset purposes)
    clearLedger() {
        this.transactions = [];
    }
}

export default HolographicQuantumLedger;
