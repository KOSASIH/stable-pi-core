// tests/hdtN.test.js

const HyperDimensionalTransactionNexus = require('./hdtN');

describe('HyperDimensionalTransactionNexus', () => {
    let hdtN;

    beforeEach(() => {
        hdtN = new HyperDimensionalTransactionNexus();
    });

    test('should initiate a valid hyper-dimensional transaction', () => {
        const transactionDetails = {
            sender: 'User  A',
            receiver: 'User  B',
            amount: 100
        };
        hdtN.initiateTransaction(transactionDetails);
        expect(hdtN.listTransactions()).toHaveLength(1);
        expect(hdtN.listTransactions()[0].details).toEqual(transactionDetails);
    });

    test('should not initiate an invalid transaction (negative amount)', () => {
        const invalidTransactionDetails = {
            sender: 'User  A',
            receiver: 'User  B',
            amount: -50 // Invalid amount
        };
        console.error = jest.fn(); // Mock console.error to capture output
        hdtN.initiateTransaction(invalidTransactionDetails);
        expect(hdtN.listTransactions()).toHaveLength(0);
        expect(console.error).toHaveBeenCalledWith('Invalid transaction details.');
    });

    test('should not initiate an invalid transaction (missing sender)', () => {
        const invalidTransactionDetails = {
            receiver: 'User  B',
            amount: 100
        };
        console.error = jest.fn(); // Mock console.error to capture output
        hdtN.initiateTransaction(invalidTransactionDetails);
        expect(hdtN.listTransactions()).toHaveLength(0);
        expect(console.error).toHaveBeenCalledWith('Invalid transaction details.');
    });

    test('should create a unique transaction ID', () => {
        const transactionDetails = {
            sender: 'User  A',
            receiver: 'User  B',
            amount: 100
        };
        hdtN.initiateTransaction(transactionDetails);
        const transactionId = hdtN.listTransactions()[0].id;
        expect(transactionId).toMatch(/^HDTN-\d+-[a-z0-9]{9}$/); // Check ID format
    });

    test('should calculate the transaction dimension based on amount', () => {
        const transactionDetails = {
            sender: 'User  A',
            receiver: 'User  B',
            amount: 500 // This should lead to a higher dimension
        };
        hdtN.initiateTransaction(transactionDetails);
        const transaction = hdtN.listTransactions()[0];
        expect(transaction.dimension).toBeGreaterThan(4); // Expect dimension to be greater than 4D
    });

    test('should execute the transaction successfully', async () => {
        const transactionDetails = {
            sender: 'User  A',
            receiver: 'User  B',
            amount: 100
        };
        hdtN.initiateTransaction(transactionDetails);
        const transaction = hdtN.listTransactions()[0];

        // Wait for the transaction to complete
        await new Promise(resolve => setTimeout(resolve, 1100)); // Wait slightly longer than the execution time

        expect(transaction.status).toBe('completed');
    });

    test('should handle errors during transaction execution', async () => {
        const transactionDetails = {
            sender: 'User  A',
            receiver: 'User  B',
            amount: 100
        };

        // Mock the random failure in executeTransaction
        jest.spyOn(Math, 'random').mockReturnValue(0.1); // Force a failure

        hdtN.initiateTransaction(transactionDetails);
        const transaction = hdtN.listTransactions()[0];

        // Wait for the transaction to complete
        await new Promise(resolve => setTimeout(resolve, 1100)); // Wait slightly longer than the execution time

        expect(transaction.status).toBe('failed');
        expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Quantum tunneling error occurred during transaction execution.'));
        
        // Restore the original Math.random
        Math.random.mockRestore();
    });

    test('should list all transactions', () => {
        const transactionDetails1 = {
            sender: 'User  A',
            receiver: 'User  B',
            amount: 100
        };
        const transactionDetails2 = {
            sender: 'User  C',
            receiver: 'User  D',
            amount: 200
        };

        hdtN.initiateTransaction(transactionDetails1);
        hdtN.initiateTransaction(transactionDetails2);

        const transactions = hdtN.listTransactions();
        expect(transactions).toHaveLength(2);
        expect(transactions[0].details).toEqual(transactionDetails1);
        expect(transactions[1].details).toEqual(transactionDetails2);
    });
});
