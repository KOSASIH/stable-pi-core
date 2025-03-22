// tests/hql.test.js

import HolographicQuantumLedger from '../src/core/hql';
import GalacticEntropyReversalSystem from '../src/core/gers';
import AccessControl from '../src/core/accessControl';
import Transaction from '../src/core/transaction';

jest.mock('../src/core/gers'); // Mock GERS
jest.mock('../src/core/accessControl'); // Mock AccessControl
jest.mock('../src/core/transaction'); // Mock Transaction

describe('HolographicQuantumLedger', () => {
    let ledger;
    let mockUser ;

    beforeEach(() => {
        ledger = new HolographicQuantumLedger();
        mockUser  = { id: 'user1' };
        ledger.accessControl.isAuthorized.mockReturnValue(true); // Mock authorization
        ledger.gers.reverseEntropy.mockImplementation(data => ({ ...data, entropyReversed: true })); // Mock reverseEntropy
    });

    test('should initialize HQL with GERS', () => {
        const mockConverter = {}; // Mock Dark Matter Energy Converter
        ledger.initializeHQL(mockConverter);
        expect(ledger.gers.initializeGERS).toHaveBeenCalledWith(mockConverter);
    });

    test('should create a new transaction', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        const transaction = ledger.createTransaction(data, mockUser );
        expect(transaction).toEqual({ id: transactionId, data: { example: 'data', entropyReversed: true } });
        expect(ledger.transactions).toContainEqual(transaction);
        expect(ledger.gers.reverseEntropy).toHaveBeenCalledWith({ protected: true, timestamp: expect.any(Number) });
    });

    test('should throw an error when creating a transaction if unauthorized', () => {
        ledger.accessControl.isAuthorized.mockReturnValue(false); // Mock unauthorized access
        const data = { example: 'data' };
        expect(() => {
            ledger.createTransaction(data, mockUser );
        }).toThrow("Unauthorized access to create transaction.");
    });

    test('should retrieve a transaction by ID', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        ledger.createTransaction(data, mockUser );
        const retrievedTransaction = ledger.getTransaction(transactionId);
        expect(retrievedTransaction).toEqual({ id: transactionId, data: { example: 'data', entropyReversed: true } });
    });

    test('should throw an error when retrieving a non-existent transaction', () => {
        expect(() => {
            ledger.getTransaction('nonExistentId');
        }).toThrow("Transaction not found.");
    });

    test('should update a transaction', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        const transaction = ledger.createTransaction(data, mockUser );
        const updatedTransaction = { ...transaction, data: { example: 'updated data' } };
        ledger.updateTransaction(updatedTransaction);

        expect(ledger.transactions[0].data).toEqual({ example: 'updated data' });
    });

    test('should throw an error when updating a non-existent transaction', () => {
        const updatedTransaction = { id: 'nonExistentId', data: { example: 'data' } };
        expect(() => {
            ledger.updateTransaction(updatedTransaction);
        }).toThrow("Transaction not found.");
    });

    test('should rewind a transaction to a previous state', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        ledger.createTransaction(data, mockUser );
        const targetTimestamp = Date.now(); // Simulate a target timestamp
        const rewindedTransaction = ledger.rewindTransaction(transactionId, targetTimestamp, mockUser );

        expect(rewindedTransaction).toBeDefined(); // Assuming the rewindTransaction method returns something
        expect(ledger.ttr.rewindTransaction).toHaveBeenCalledWith(transactionId, targetTimestamp, mockUser);
    });

    test('should generate a quantum hash for a transaction', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        const transaction = ledger.createTransaction(data, mockUser );
        const hash = ledger.generateTransactionHash(transaction);
        
        expect(hash).toBeDefined(); // Assuming generateQuantumHash returns a hash
        expect(generateQuantumHash).toHaveBeenCalledWith(transaction);
    });

    test('should validate a transaction\'s signature', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        const transaction = ledger.createTransaction(data, mockUser );
        const isValid = ledger.validateTransactionSignature(transaction);
        
        expect(isValid).toBe(true); // Assuming validateQuantumSignature returns true
        expect(validateQuantumSignature).toHaveBeenCalledWith(transaction);
    });

    test('should get all transactions', () => {
        const data1 = { example: 'data1' };
        const data2 = { example: 'data2' };
        ledger.createTransaction(data1, mockUser );
        ledger.createTransaction(data2, mockUser );

        const allTransactions = ledger.getAllTransactions();
        expect(allTransactions.length).toBe(2);
    });

    test('should clear the ledger', () => {
        const data = { example: 'data' };
        ledger.createTransaction(data, mockUser );
        expect(ledger.transactions.length).toBe(1);

        ledger.clearLedger();
        expect(ledger.transactions.length).toBe(0);
    });

    test('should enhance protection level', () => {
        const initialProtectionLevel = ledger.getProtectionLevel();
        ledger.enhanceProtection(10);
        expect(ledger.getProtectionLevel()).toBe(initialProtectionLevel + 10);
    });

    test('should reset protection level', () => {
        ledger.enhanceProtection(20);
        expect(ledger.getProtectionLevel()).toBe(100); // Assuming max protection level is 100
        ledger.resetProtection();
        expect(ledger.getProtectionLevel()).toBe(100);
    });

    test('should trigger self-healing in the blockchain', () => {
        ledger.triggerSelfHealing();
        expect(ledger.sebd.selfHeal).toHaveBeenCalled();
    });
});
