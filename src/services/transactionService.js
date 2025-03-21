// src/services/transactionService.js

import HolographicQuantumLedger from '../core/hql';
import Transaction from '../core/transaction';
import AccessControl from '../core/accessControl';
import { formatTimestamp } from '../core/utils';

class TransactionService {
    constructor() {
        this.ledger = new HolographicQuantumLedger();
        this.accessControl = new AccessControl();
    }

    // Create a new transaction
    createTransaction(data, user, privateKey) {
        try {
            // Check user authorization
            if (!this.accessControl.isAuthorized(user, 'create')) {
                throw new Error("User is not authorized to create transactions.");
            }

            // Create a new transaction
            const transaction = new Transaction(data, user);
            transaction.sign(privateKey); // Sign the transaction

            // Add transaction to the ledger
            this.ledger.createTransaction(transaction);
            this.logTransaction(transaction, 'created');
            return transaction;
        } catch (error) {
            this.handleError(error);
        }
    }

    // Retrieve a transaction by ID
    getTransaction(transactionId) {
        try {
            const transaction = this.ledger.getTransaction(transactionId);
            if (!transaction) {
                throw new Error("Transaction not found.");
            }
            return transaction;
        } catch (error) {
            this.handleError(error);
        }
    }

    // Update an existing transaction
    updateTransaction(transactionId, updatedData, user, privateKey) {
        try {
            // Check user authorization
            if (!this.accessControl.isAuthorized(user, 'update')) {
                throw new Error("User is not authorized to update transactions.");
            }

            const transaction = this.ledger.getTransaction(transactionId);
            if (!transaction) {
                throw new Error("Transaction not found.");
            }

            // Update transaction data
            transaction.data = updatedData;
            transaction.sign(privateKey); // Re-sign the transaction

            // Update the transaction in the ledger
            this.ledger.updateTransaction(transaction);
            this.logTransaction(transaction, 'updated');
            return transaction;
        } catch (error) {
            this.handleError(error);
        }
    }

    // Rewind a transaction to a previous state
    rewindTransaction(transactionId, targetTimestamp, user) {
        try {
            // Check user authorization
            if (!this.accessControl.isAuthorized(user, 'rewind')) {
                throw new Error("User is not authorized to rewind transactions.");
            }

            const rewindedTransaction = this.ledger.rewindTransaction(transactionId, targetTimestamp, user);
            this.logTransaction(rewindedTransaction, 'rewinded');
            return rewindedTransaction;
        } catch (error) {
            this.handleError(error);
        }
    }

    // Log transaction actions
    logTransaction(transaction, action) {
        const timestamp = formatTimestamp(Date.now());
        console.log(`[${timestamp}] Transaction ${action}:`, transaction);
    }

    // Handle errors and log them
    handleError(error) {
        const timestamp = formatTimestamp(Date.now());
        console.error(`[${timestamp}] Error: ${error.message}`);
        throw new Error(error.message); // Rethrow the error for further handling
    }
}

export default TransactionService;
