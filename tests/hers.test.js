// tests/hers.test.js

import HyperEntangledRealitySynchronizer from '../src/quantum/hers';

describe('HyperEntangledRealitySynchronizer', () => {
    let hers;

    beforeEach(() => {
        hers = new HyperEntangledRealitySynchronizer();
    });

    test('should initialize with no entangled realities and empty transaction history', () => {
        expect(hers.getEntangledRealities()).toEqual([]);
        expect(hers.getTransactionHistory()).toEqual([]);
    });

    test('should entangle a new reality', () => {
        hers.entangleReality('reality-1');
        expect(hers.getEntangledRealities()).toContain('reality-1');
    });

    test('should not entangle the same reality twice', () => {
        hers.entangleReality('reality-1');
        hers.entangleReality('reality-1'); // Attempt to entangle again
        expect(hers.getEntangledRealities()).toEqual(['reality-1']);
    });

    test('should disentangle a reality', () => {
        hers.entangleReality('reality-1');
        hers.disentangleReality('reality-1');
        expect(hers.getEntangledRealities()).not.toContain('reality-1');
    });

    test('should throw an error when trying to synchronize without entangled realities', async () => {
        await expect(hers.synchronizeTransaction({ data: 'test' })).rejects.toThrow('No entangled realities to synchronize with.');
    });

    test('should synchronize transactions across entangled realities', async () => {
        hers.entangleReality('reality-1');
        hers.entangleReality('reality-2');

        const transactionData = { amount: 100, from: 'A', to: 'B' };
        const results = await hers.synchronizeTransaction(transactionData);

        expect(results).toHaveLength(2);
        expect(results).toEqual([
            { realityId: 'reality-1', transactionData, status: 'success' },
            { realityId: 'reality-2', transactionData, status: 'success' },
        ]);
        expect(hers.getTransactionHistory()).toHaveLength(2);
    });

    test('should emit events when realities are entangled and transactions are synchronized', (done) => {
        hers.on('realityEntangled', (realityId) => {
            expect(realityId).toBe('reality-1');
        });

        hers.on('transactionSynchronized', (results) => {
            expect(results).toHaveLength(1);
            expect(results[0].realityId).toBe('reality-1');
            done();
        });

        hers.entangleReality('reality-1');
        hers.synchronizeTransaction({ data: 'test' });
    });

    test('should handle synchronization errors gracefully', async () => {
        hers.entangleReality('reality-1');

        // Mock the sendTransactionToReality method to simulate failure
        jest.spyOn(hers, 'sendTransactionToReality').mockImplementation(() => {
            return Promise.reject(new Error('Failed to send transaction'));
        });

        await expect(hers.synchronizeTransaction({ data: 'test' })).rejects.toThrow('Failed to send transaction');
        expect(hers.getTransactionHistory()).toHaveLength(0); // No transactions should be recorded
    });

    test('should clear the transaction history', () => {
        hers.entangleReality('reality-1');
        hers.synchronizeTransaction({ data: 'test' });
        expect(hers.getTransactionHistory()).toHaveLength(1);

        hers.clearTransactionHistory();
        expect(hers.getTransactionHistory()).toHaveLength(0);
    });
});
