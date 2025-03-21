// tests/hql.test.js

import HolographicQuantumLedger from '../src/core/hql';
import Transaction from '../src/core/transaction';
import AccessControl from '../src/core/accessControl';

jest.mock('../src/core/accessControl'); // Mock the AccessControl module

describe('CosmicEntropyShield', () => {
    let ces;

    beforeEach(() => {
        ces = new HolographicQuantumLedger().ces; // Get the Cosmic Entropy Shield instance
    });

    test('should initialize with maximum protection level', () => {
        expect(ces.getProtectionLevel()).toBe(100);
    });

    test('should enhance protection level', () => {
        ces.enhanceProtection(10);
        expect(ces.getProtectionLevel()).toBe(100); // Should not exceed 100
    });

    test('should warn when protection level is low', () => {
        ces.enhanceProtection(-60); // Reduce protection level to 40
        console.warn = jest.fn(); // Mock console.warn
        ces.protectData({ data: 'test' });
        expect(console.warn).toHaveBeenCalledWith("Warning: Protection level is low. Data may be at risk of degradation.");
    });

    test('should protect data', () => {
        const protectedData = ces.protectData({ data: 'test' });
        expect(protectedData).toEqual(expect.objectContaining({ protected: true }));
    });

    test('should degrade data if protection level is low', () => {
        ces.enhanceProtection(-60); // Reduce protection level to 40
        const result = ces.degradeData({ data: 'test' });
        expect(result).toBe(null); // Data should be lost
    });

    test('should maintain data integrity if protection level is sufficient', () => {
        const result = ces.degradeData({ data: 'test' });
        expect(result).toEqual({ data: 'test' }); // Data should be intact
    });

    test('should reset protection level to maximum', () => {
        ces.enhanceProtection(-60); // Reduce protection level to 40
        ces.resetProtection();
        expect(ces.getProtectionLevel()).toBe(100);
    });
});

describe('HolographicQuantumLedger', () => {
    let ledger;
    let accessControl;

    beforeEach(() => {
        ledger = new HolographicQuantumLedger();
        accessControl = new AccessControl();
        accessControl.isAuthorized = jest.fn().mockReturnValue(true); // Mock authorization
    });

    test('should create a new transaction', () => {
        const data = { amount: 100 };
        const user = '0xUser1';
        const transaction = ledger.createTransaction(data, user);
        expect(transaction).toBeInstanceOf(Transaction);
        expect(ledger.transactions).toContain(transaction);
    });

    test('should throw error if user is not authorized to create transaction', () => {
        accessControl.isAuthorized.mockReturnValue(false); // Mock unauthorized access
        const data = { amount: 100 };
        const user = '0xUser1';
        expect(() => ledger.createTransaction(data, user)).toThrow("Unauthorized access to create transaction.");
    });

    test('should retrieve a transaction by ID', () => {
        const data = { amount: 100 };
        const user = '0xUser1';
        const transaction = ledger.createTransaction(data, user);
        const retrievedTransaction = ledger.getTransaction(transaction.id);
        expect(retrievedTransaction).toEqual(transaction);
    });

    test('should throw error for non-existent transaction', () => {
        expect(() => ledger.getTransaction('non-existent-id')).toThrow("Transaction not found.");
    });

    test('should update a transaction', () => {
        const data = { amount: 100 };
        const user = '0xUser1';
        const transaction = ledger.createTransaction(data, user);
        const updatedTransaction = { ...transaction, amount: 200 };
        ledger.updateTransaction(updatedTransaction);
        expect(ledger.getTransaction(transaction.id).data.amount).toBe(200);
    });

    test('should throw error when updating a non-existent transaction', () => {
        const updatedTransaction = new Transaction({ id: 'non-existent-id', amount: 200 });
        expect(() => ledger.updateTransaction(updatedTransaction)).toThrow("Transaction not found.");
    });

    test('should rewind a transaction', async () => {
        const data = { amount: 100 };
        const user = '0xUser1';
        const transaction = ledger.createTransaction(data, user);
        const rewindedTransaction = await ledger.rewindTransaction(transaction.id, Date.now(), user);
        expect(rewindedTransaction).toBeDefined(); // Assuming TTR logic is implemented
    });

    test('should clear the ledger', () => {
        const data = { amount: 100 };
        const user = '0xUser1';
        ledger.createTransaction(data, user);
        ledger.clearLedger();
        expect(ledger.getAllTransactions()).toHaveLength(0);
    });
});
