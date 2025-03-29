import HolographicQuantumLedger from '../src/core/hql';
import GalacticEntropyReversalSystem from '../src/core/gers';
import AccessControl from '../src/core/accessControl';
import Transaction from '../src/core/transaction';
import CSRFProtection from '../src/core/csrf_layer'; // Import CSRF Protection
import { generateQuantumHash, validateQuantumSignature } from '../src/core/utils'; // Import utility functions
import CosmicMemoryImprintNetwork from '../src/core/cmin'; // Import Cosmic Memory Imprint Network

jest.mock('../src/core/gers'); // Mock GERS
jest.mock('../src/core/accessControl'); // Mock AccessControl
jest.mock('../src/core/transaction'); // Mock Transaction
jest.mock('../src/core/csrf_layer'); // Mock CSRF Protection
jest.mock('../src/core/utils'); // Mock utility functions
jest.mock('../src/core/cmin'); // Mock Cosmic Memory Imprint Network

describe('HolographicQuantumLedger', () => {
    let ledger;
    let mockUser ;

    beforeEach(() => {
        ledger = new HolographicQuantumLedger();
        mockUser  = { id: 'user1' };
        ledger.accessControl.isAuthorized.mockReturnValue(true); // Mock authorization
        ledger.gers.reverseEntropy.mockImplementation(data => ({ ...data, entropyReversed: true })); // Mock reverseEntropy
        CSRFProtection.prototype.verify_token.mockImplementation(() => {}); // Mock CSRF verification
    });

    test('should initialize HQL with GERS', () => {
        const mockConverter = {}; // Mock Dark Matter Energy Converter
        ledger.initializeHQL(mockConverter);
        expect(ledger.gers.initializeGERS).toHaveBeenCalledWith(mockConverter);
    });

    test('should create a new transaction with valid CSRF token', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        const transaction = ledger.createTransaction(data, mockUser , 'valid-csrf-token');
        expect(transaction).toEqual({ id: transactionId, data: { example: 'data', entropyReversed: true } });
        expect(ledger.transactions).toContainEqual(transaction);
        expect(ledger.gers.reverseEntropy).toHaveBeenCalledWith({ protected: true, timestamp: expect.any(Number) });
        expect(ledger.cmin.captureMemoryImprint).toHaveBeenCalledWith({ transactionId, data: { protected: true, timestamp: expect.any(Number) } }, mockUser .id, 'valid-csrf-token');
    });

    test('should throw an error when creating a transaction with invalid CSRF token', () => {
        ledger.accessControl.isAuthorized.mockReturnValue(true); // Ensure user is authorized
        const data = { example: 'data' };
        CSRFProtection.prototype.verify_token.mockImplementation(() => {
            throw new Error('Invalid CSRF token');
        });

        expect(() => {
            ledger.createTransaction(data, mockUser , 'invalid-csrf-token');
        }).toThrow('Invalid CSRF token');

        expect(ledger.transactions).toHaveLength(0);
    });

    test('should retrieve a transaction by ID', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        ledger.createTransaction(data, mockUser , 'valid-csrf-token');
        const retrievedTransaction = ledger.getTransaction(transactionId);
        expect(retrievedTransaction).toEqual({ id: transactionId, data: { example: 'data', entropyReversed: true } });
    });

    test('should throw an error when retrieving a non-existent transaction', () => {
        expect(() => {
            ledger.getTransaction('nonExistentId');
        }).toThrow("Transaction not found.");
    });

    test('should update a transaction with valid CSRF token', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        const transaction = ledger.createTransaction(data, mockUser , 'valid-csrf-token');
        const updatedTransaction = { ...transaction, data: { example: 'updated data' } };

        ledger.updateTransaction(updatedTransaction, 'valid-csrf-token');

        expect(ledger.transactions[0].data).toEqual({ example: 'updated data' });
        expect(ledger.cmin.captureMemoryImprint).toHaveBeenCalledWith({ transactionId: updatedTransaction.id, data: updatedTransaction.data }, updatedTransaction.userId, 'valid-csrf-token');
    });

    test('should throw an error when updating a transaction with invalid CSRF token', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        const transaction = ledger.createTransaction(data, mockUser  , 'valid-csrf-token');
        const updatedTransaction = { ...transaction, data: { example: 'updated data' } };

        CSRFProtection.prototype.verify_token.mockImplementation(() => {
            throw new Error('Invalid CSRF token');
        });

        expect(() => {
            ledger.updateTransaction(updatedTransaction, 'invalid-csrf-token');
        }).toThrow('Invalid CSRF token');

        expect(ledger.transactions[0].data).toEqual({ example: 'data' }); // Ensure original data is unchanged
    });

    test('should rewind a transaction to a previous state', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        ledger.createTransaction(data, mockUser  , 'valid-csrf-token');
        const targetTimestamp = Date.now(); // Simulate a target timestamp
        const rewindedTransaction = ledger.rewindTransaction(transactionId, targetTimestamp, mockUser  , 'valid-csrf-token');

        expect(rewindedTransaction).toBeDefined(); // Assuming the rewindTransaction method returns something
        expect(ledger.ttr.rewindTransaction).toHaveBeenCalledWith(transactionId, targetTimestamp, mockUser  );
    });

    test('should generate a quantum hash for a transaction', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        const transaction = ledger.createTransaction(data, mockUser  , 'valid-csrf-token');
        const hash = ledger.generateTransactionHash(transaction);

        expect(hash).toBeDefined(); // Assuming generateQuantumHash returns a hash
        expect(generateQuantumHash).toHaveBeenCalledWith(transaction);
    });

    test('should validate a transaction\'s signature', () => {
        const data = { example: 'data' };
        const transactionId = 'tx1';
        Transaction.mockImplementation(() => ({ id: transactionId, data }));

        const transaction = ledger.createTransaction(data, mockUser  , 'valid-csrf-token');
        const isValid = ledger.validateTransactionSignature(transaction);

        expect(isValid).toBe(true); // Assuming validateQuantumSignature returns true
        expect(validateQuantumSignature).toHaveBeenCalledWith(transaction);
    });

    test('should get all transactions', () => {
        const data1 = { example: 'data1' };
        const data2 = { example: 'data2' };
        ledger.createTransaction(data1, mockUser  , 'valid-csrf-token');
        ledger.createTransaction(data2, mockUser  , 'valid-csrf-token');

        const allTransactions = ledger.getAllTransactions();
        expect(allTransactions.length).toBe(2);
    });

    test('should clear the ledger', () => {
        const data = { example: 'data' };
        ledger.createTransaction(data, mockUser  , 'valid-csrf-token');
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

    test('should handle empty data when creating a transaction', () => {
        expect(() => {
            ledger.createTransaction({}, mockUser  , 'valid-csrf-token');
        }).toThrow('Data cannot be empty');
    });

    test('should handle invalid user when creating a transaction', () => {
        const data = { example: 'data' };
        const invalidUser  = null; // Simulate an invalid user

        expect(() => {
            ledger.createTransaction(data, invalidUser  , 'valid-csrf-token');
        }).toThrow('User  is not authorized');
    });
});
