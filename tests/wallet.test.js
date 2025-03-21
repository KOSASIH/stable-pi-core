// tests/wallet.test.js

import Wallet from '../src/tokens/wallet';

describe('Wallet', () => {
    let wallet;

    beforeEach(() => {
        wallet = new Wallet();
    });

    test('should initialize with a balance of 0', () => {
        expect(wallet.getBalance()).toBe(0);
    });

    test('authenticate - should authenticate successfully with password', () => {
        const result = wallet.authenticate('validPassword');
        expect(result).toBe(true);
    });

    test('authenticateWithBQIL - should authenticate successfully with valid bio-signal', async () => {
        const bioSignal = 'validBioSignal';
        await expect(wallet.authenticateWithBQIL(bioSignal)).resolves.toBe(true);
    });

    test('authenticateWithBQIL - should throw error for invalid bio-signal', async () => {
        const bioSignal = 'invalidBioSignal';
        wallet.validateBioSignal = jest.fn().mockResolvedValue(false); // Mock validation to return false
        await expect(wallet.authenticateWithBQIL(bioSignal)).rejects.toThrow('Bio-signal authentication failed.');
    });

    test('performTransaction - should perform transaction successfully with valid bio-signal', async () => {
        const bioSignal = 'validBioSignal';
        await wallet.authenticateWithBQIL(bioSignal); // Authenticate first
        const newBalance = await wallet.performTransaction(100, bioSignal);
        expect(newBalance).toBe(100);
        expect(wallet.getTransactionHistory()).toHaveLength(1);
        expect(wallet.getTransactionHistory()[0]).toEqual({ amount: 100, timestamp: expect.any(Date) });
    });

    test('performTransaction - should throw error for negative transaction amount', async () => {
        const bioSignal = 'validBioSignal';
        await wallet.authenticateWithBQIL(bioSignal); // Authenticate first
        await expect(wallet.performTransaction(-50, bioSignal)).rejects.toThrow('Transaction amount must be positive.');
    });

    test('performTransaction - should throw error if not authenticated', async () => {
        await expect(wallet.performTransaction(50, 'validBioSignal')).rejects.toThrow('User  must be authenticated to perform transactions.');
    });

    test('resetBioSignalAuthentication - should reset bio-signal authentication', async () => {
        const bioSignal = 'validBioSignal';
        await wallet.authenticateWithBQIL(bioSignal); // Authenticate first
        wallet.resetBioSignalAuthentication();
        expect(wallet.isBioSignalAuthenticated).toBe(false);
    });

    test('getTransactionHistory - should return transaction history', async () => {
        const bioSignal = 'validBioSignal';
        await wallet.authenticateWithBQIL(bioSignal); // Authenticate first
        await wallet.performTransaction(100, bioSignal);
        await wallet.performTransaction(200, bioSignal);
        const history = wallet.getTransactionHistory();
        expect(history).toHaveLength(2);
        expect(history[0]).toEqual({ amount: 100, timestamp: expect.any(Date) });
        expect(history[1]).toEqual({ amount: 200, timestamp: expect.any(Date) });
    });
});
