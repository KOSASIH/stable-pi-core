// src/tests/ttr.test.js

import TemporalTransactionRewind from '../core/ttr';
import HolographicQuantumLedger from '../core/hql';
import Transaction from '../core/transaction';

describe('Temporal Transaction Rewind', () => {
    let ledger;
    let ttr;
    let user;
    let transaction;

    beforeEach(() => {
        ledger = new HolographicQuantumLedger();
        ttr = new TemporalTransactionRewind(ledger);
        user = { username: 'testUser', hasQuantumAccess: true };
        transaction = new Transaction({ amount: 100 }, user);
        transaction.sign('privateKey'); // Mock signing
        ledger.createTransaction(transaction);
    });

    test('should rewind a transaction to a previous state', () => {
        const targetTimestamp = Date.now() - 1000; // 1 second ago
        const rewindedTransaction = ttr.rewindTransaction(transaction.id, targetTimestamp, user);
        expect(rewindedTransaction.timestamp).toBeLessThan(transaction.timestamp);
    });

    test('should throw error for unauthorized user', () => {
        user.hasQuantumAccess = false;
        expect(() => {
            ttr.rewindTransaction(transaction.id, Date.now() - 1000, user);
        }).toThrow("Unauthorized access to TTR feature.");
    });

    test('should throw error for non-existent transaction', () => {
        expect(() => {
            ttr.rewindTransaction('nonExistentId', Date.now() - 1000, user);
        }).toThrow("Transaction not found.");
    });

    test('should throw error for invalid target timestamp', () => {
        expect(() => {
            ttr.rewindTransaction(transaction.id, transaction.timestamp + 1000, user);
        }).toThrow("Target timestamp must be earlier than the transaction timestamp.");
    });
});
