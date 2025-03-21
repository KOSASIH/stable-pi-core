// tests/bqil.test.js

import BioQuantumIntegrationLayer from '../src/tokens/bqil';

describe('BioQuantumIntegrationLayer', () => {
    let bqil;

    beforeEach(() => {
        bqil = new BioQuantumIntegrationLayer();
    });

    test('should initialize with authentication status as false', () => {
        expect(bqil.checkAuthentication()).toBe(false);
    });

    test('addValidBioSignal - should add a valid bio-signal', () => {
        bqil.addValidBioSignal('validBioSignal');
        expect(bqil.isValidBioSignal('validBioSignal')).toBe(true);
    });

    test('authenticate - should authenticate successfully with valid bio-signal', async () => {
        bqil.addValidBioSignal('validBioSignal');
        await expect(bqil.authenticate('validBioSignal')).resolves.toBe(true);
        expect(bqil.checkAuthentication()).toBe(true);
    });

    test('authenticate - should throw error for invalid bio-signal', async () => {
        await expect(bqil.authenticate('invalidBioSignal')).rejects.toThrow('Bio-signal authentication failed.');
        expect(bqil.checkAuthentication()).toBe(false);
    });

    test('validateBioSignal - should validate a valid bio-signal', async () => {
        bqil.addValidBioSignal('validBioSignal');
        const isValid = await bqil.validateBioSignal('validBioSignal');
        expect(isValid).toBe(true);
    });

    test('validateBioSignal - should not validate an invalid bio-signal', async () => {
        const isValid = await bqil.validateBioSignal('invalidBioSignal');
        expect(isValid).toBe(false);
    });

    test('resetAuthentication - should reset authentication status', async () => {
        bqil.addValidBioSignal('validBioSignal');
        await bqil.authenticate('validBioSignal'); // Authenticate first
        bqil.resetAuthentication();
        expect(bqil.checkAuthentication()).toBe(false);
    });

    test('performSecureTransaction - should throw error if not authenticated', async () => {
        await expect(bqil.performSecureTransaction(100, 'validBioSignal')).rejects.toThrow('User  must be authenticated to perform transactions.');
    });

    test('performSecureTransaction - should perform transaction successfully if authenticated', async () => {
        bqil.addValidBioSignal('validBioSignal');
        await bqil.authenticate('validBioSignal'); // Authenticate first
        await expect(bqil.performSecureTransaction(100, 'validBioSignal')).resolves.toBe(true);
    });
});
