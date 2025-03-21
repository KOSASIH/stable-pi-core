// src/tests/transaction.test.js

import Transaction from '../core/transaction';

describe('Transaction Model', () => {
    let user;
    let transaction;

    beforeEach(() => {
        user = { username: 'testUser', publicKey: 'publicKey' };
        transaction = new Transaction({ amount: 100 }, user);
    });

    test('should generate a unique ID for the transaction', () => {
        expect(transaction.id).toMatch(/tx_\d+_[a-z0-9]{9}/);
    });

    test('should generate a hash for the transaction', () => {
        expect(transaction.hash).toBeDefined();
    });

    test('should sign the transaction', () => {
       transaction.sign('privateKey');
        expect(transaction.signature).toBeDefined();
        expect(transaction.signature).not.toBeNull();
    });

    test('should validate the transaction signature', () => {
        transaction.sign('privateKey');
        const isValid = transaction.validateSignature();
        expect(isValid).toBe(true);
    });

    test('should throw error for invalid transaction data', () => {
        expect(() => {
            new Transaction(null, user);
        }).toThrow("Transaction data is required.");
    });
});
