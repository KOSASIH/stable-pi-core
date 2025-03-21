// src/tests/hql.test.js

import HolographicQuantumLedger from '../core/hql';
import Transaction from '../core/transaction';

describe('Holographic Quantum Ledger', () => {
    let ledger;
    let user;

    beforeEach(() => {
        ledger = new HolographicQuantumLedger();
        user = { username: 'testUser', hasQuantumAccess: true };
    });

    test('should create a new transaction', () => {
        const transaction = new Transaction({ amount: 100 }, user);
        transaction.sign('privateKey'); // Mock signing
        ledger.createTransaction(transaction);
        expect(ledger.getTransaction(transaction.id)).toEqual(transaction);
    });

    test('should update an existing transaction', () => {
        const transaction = new Transaction({ amount: 100 }, user);
        transaction.sign('privateKey'); // Mock signing
        ledger.createTransaction(transaction);

        transaction.data.amount = 200; // Update amount
        ledger.updateTransaction(transaction);
        expect(ledger.getTransaction(transaction.id).data.amount).toBe(200);
    });

    test('should throw error for non-existent transaction update', () => {
        const transaction = new Transaction({ amount: 100 }, user);
        expect(() => {
            ledger.updateTransaction(transaction);
        }).toThrow("Transaction not found.");
    });

    test('should retrieve all transactions', () => {
        const transaction1 = new Transaction({ amount: 100 }, user);
        transaction1.sign('privateKey'); // Mock signing
        ledger.createTransaction(transaction1);

        const transaction2 = new Transaction({ amount: 200 }, user);
        transaction2.sign('privateKey'); // Mock signing
        ledger.createTransaction(transaction2);

        expect(ledger.getAllTransactions().length).toBe(2);
    });
});
