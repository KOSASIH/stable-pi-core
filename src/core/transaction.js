// src/core/transaction.js

import { generateQuantumHash, validateQuantumSignature, signTransaction } from './utils';

class Transaction {
    constructor(data, user) {
        this.id = this.generateId();
        this.timestamp = Date.now();
        this.data = data;
        this.user = user;
        this.signature = null;
        this.hash = this.generateHash();
    }

    // Generate a unique ID for the transaction
    generateId() {
        return `tx_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    // Generate a quantum hash for the transaction
    generateHash() {
        return generateQuantumHash(this);
    }

    // Sign the transaction using the user's private key
    sign(privateKey) {
        this.signature = signTransaction(this, privateKey);
    }

    // Validate the transaction's signature
    validate() {
        if (!this.signature) {
            throw new Error("Transaction is not signed.");
        }
        if (!validateQuantumSignature(this)) {
            throw new Error("Invalid transaction signature.");
        }
        return true;
    }

    // Method to serialize the transaction for storage or transmission
    serialize() {
        return JSON.stringify({
            id: this.id,
            timestamp: this.timestamp,
            data: this.data,
            user: this.user,
            signature: this.signature,
            hash: this.hash,
        });
    }

    // Method to deserialize a transaction from a JSON string
    static deserialize(jsonString) {
        const obj = JSON.parse(jsonString);
        const transaction = new Transaction(obj.data, obj.user);
        transaction.id = obj.id;
        transaction.timestamp = obj.timestamp;
        transaction.signature = obj.signature;
        transaction.hash = obj.hash;
        return transaction;
    }
}

export default Transaction;
