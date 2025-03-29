// tests/bqil.test.js

import BioQuantumIntegrationLayer from './bqil';

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

    // HTT Tests
    test('processUser Transaction - should throw error if not authenticated', async () => {
        const userIntent = {
            action: 'createTransaction',
            details: {
                sender: 'User  A',
                receiver: 'User  B',
                amount: 100
            }
        };
        await expect(bqil.processUser Transaction(userIntent)).rejects.toThrow('User  must be authenticated to process transactions.');
    });

    test('processUser Transaction - should process transaction successfully if authenticated', async () => {
        bqil.addValidBioSignal('validBioSignal');
        await bqil.authenticate('validBioSignal'); // Authenticate first

        const userIntent = {
            action: 'createTransaction',
            details: {
                sender: 'User  A',
                receiver: 'User  B',
                amount: 100
            }
        };

        await expect(bqil.processUser Transaction(userIntent)).resolves.toBe(true);
    });

    test('connectToCNSF - should connect user consciousness with a cosmic phenomenon', () => {
        const userConsciousness = { name: 'User  A' };
        const cosmicPhenomenon = { getFrequency: () => 42 };

        bqil.connectToCNSF(userConsciousness, cosmicPhenomenon);
        expect(bqil.cnsf.userConsciousness).toEqual(userConsciousness);
        expect(bqil.cnsf.cosmicPhenomenon).toEqual(cosmicPhenomenon);
    });

    test('connectToCNSF - should synchronize user consciousness', () => {
        const userConsciousness = { name: 'User  A' };
        const cosmicPhenomenon = { getFrequency: () => 42 };

        bqil.connectToCNSF(user Consciousness, cosmicPhenomenon);
        expect(bqil.cnsf.resonanceFrequency).toBeGreaterThan(0);
    });

    test('establishSymbiosis - should establish symbiosis with a valid cosmic entity', () => {
        const cosmicEntity = { name: 'Andromeda', type: 'galaxy' };
        bqil.establishSymbiosis(cosmicEntity);
        expect(bqil.listSymbioticEntities()).toContain(cosmicEntity);
    });

    test('establishSymbiosis - should not establish symbiosis with an invalid entity', () => {
        const invalidEntity = { name: 'Invalid', type: 'unknown' };
        bqil.establishSymbiosis(invalidEntity);
        expect(bqil.listSymbioticEntities()).not.toContain(invalidEntity);
    });

    test('removeSymbiosis - should remove a symbiotic relationship', () => {
        const cosmicEntity = { name: 'Andromeda', type: 'galaxy' };
        bqil.establishSymbiosis(cosmicEntity);
        expect(bqil.listSymbioticEntities()).toContain(cosmicEntity);
        
        bqil.removeSymbiosis(cosmicEntity);
        expect(bqil.listSymbioticEntities()).not.toContain(cosmicEntity);
    });

    test('removeSymbiosis - should not remove a non-existent symbiotic relationship', () => {
        const cosmicEntity = { name: 'Andromeda', type: 'galaxy' };
        bqil.removeSymbiosis(cosmicEntity); // Attempt to remove without establishing
        expect(bqil.listSymbioticEntities()).not.toContain(cosmicEntity);
    });

    test('logSymbioticRelationships - should log current symbiotic relationships', () => {
        const cosmicEntity = { name: 'Andromeda', type: 'galaxy' };
        bqil.establishSymbiosis(cosmicEntity);
        
        console.log = jest.fn(); // Mock console.log to capture output
        bqil.logSymbioticRelationships();
        expect(console.log).toHaveBeenCalledWith('Current symbiotic relationships:');
        expect(console.log).toHaveBeenCalledWith('- Andromeda (galaxy)');
    });
});
