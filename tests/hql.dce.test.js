// tests/hql.dce.test.js

import HolographicQuantumLedger from '../src/core/hql';
import DimensionalCompressionEngine from '../src/core/dce';
import Transaction from '../src/core/transaction'; // Assuming Transaction class is defined

describe('HolographicQuantumLedger with DimensionalCompressionEngine Integration', () => {
    let ledger;

    beforeEach(() => {
        ledger = new HolographicQuantumLedger();
    });

    test('should create a transaction and compress data using DCE', () => {
        const user = { id: 'user1', name: 'Alice' }; // Mock user object
        const data = { value: 42, description: 'Test transaction' };

        // Create a transaction
        const transaction = ledger.createTransaction(data, user);
        
        // Check if the transaction is created
        expect(transaction).toBeInstanceOf(Transaction);
        expect(transaction.data).toHaveProperty('protected', true);
        
        // Check if the data is compressed in DCE
        const compressedData = DimensionalCompressionEngine.retrieveData(transaction.id);
        expect(compressedData).toHaveProperty('original', data);
        expect(compressedData).toHaveProperty('compressed');
        expect(compressedData).toHaveProperty('dimensions', 4);
    });

    test('should retrieve a transaction and check data integrity', () => {
        const user = { id: 'user1', name: 'Alice' }; // Mock user object
        const data = { value: 42, description: 'Test transaction' };

        // Create a transaction
        const transaction = ledger.createTransaction(data, user);
        
        // Retrieve the transaction
        const retrievedTransaction = ledger.getTransaction(transaction.id);
        
        // Check if the retrieved transaction matches the original
        expect(retrievedTransaction.id).toBe(transaction.id);
        expect(retrievedTransaction.data).toEqual(transaction.data);
    });

    test('should throw an error when retrieving a non-existent transaction', () => {
        expect(() => ledger.getTransaction('nonExistentId')).toThrow("Transaction not found.");
    });

    test('should handle data integrity issues when protection level is low', () => {
        const user = { id: 'user1', name: 'Alice' }; // Mock user object
        const data = { value: 42, description: 'Test transaction' };

        // Create a transaction
        ledger.createTransaction(data, user);
        
        // Simulate low protection level
        ledger.ces.protectionLevel = 40; // Set protection level below threshold
        
        // Attempt to retrieve the transaction
        expect(() => ledger.getTransaction(ledger.transactions[0].id)).toThrow("Data integrity compromised. Unable to retrieve transaction.");
    });

    test('should clear the ledger and DCE storage', () => {
        const user = { id: 'user1', name: 'Alice' }; // Mock user object
        const data = { value: 42, description: 'Test transaction' };

        // Create a transaction
        ledger.createTransaction(data, user);
        
        // Clear the ledger
        ledger.clearLedger();
        
        // Check if the ledger is cleared
        expect(ledger.getAllTransactions()).toHaveLength(0);
        
        // Check if DCE storage is also cleared
        expect(() => DimensionalCompressionEngine.retrieveData(ledger.transactions[0].id)).toThrow("No data found for key: " + ledger.transactions[0].id);
    });
});
