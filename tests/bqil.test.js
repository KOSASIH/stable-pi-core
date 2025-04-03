// tests/bqil.test.js

import BioQuantumIntegrationLayer from './bioQuantumIntegrationLayer';
import AstroNeuralRealityForge from './anrf'; // Import the ANRF module

describe('BioQuantumIntegrationLayer', () => {
    let bqil;

    beforeEach(() => {
        bqil = new BioQuantumIntegrationLayer();
        bqil.addValidBioSignal('valid-signal'); // Add a valid bio-signal for testing
    });

    test('should authenticate user with valid bio-signal', async () => {
        const result = await bqil.authenticate('valid-signal');
        expect(result).toBe(true);
        expect(bqil.checkAuthentication()).toBe(true);
    });

    test('should fail authentication with invalid bio-signal', async () => {
        await expect(bqil.authenticate('invalid-signal')).rejects.toThrow('Bio-signal authentication failed.');
        expect(bqil.checkAuthentication()).toBe(false);
    });

    test('should perform a secure transaction after authentication', async () => {
        await bqil.authenticate('valid-signal');
        const result = await bqil.performSecureTransaction(100, 'valid-signal');
        expect(result).toBe(true);
    });

    test('should not perform a transaction if not authenticated', async () => {
        await expect(bqil.performSecureTransaction(100, 'valid-signal')).rejects.toThrow('User must be authenticated to perform transactions.');
    });

    test('should create a new virtual reality', () => {
        const vr = bqil.createVirtualReality("Test Reality", { economyType: "barter" });
        expect(vr.name).toBe("Test Reality");
        expect(vr.parameters).toEqual({ economyType: "barter" });
    });

    test('should simulate economy in the created virtual reality', () => {
        bqil.createVirtualReality("Test Reality", { economyType: "barter" });
        console.log = jest.fn(); // Mock console.log
        bqil.simulateEconomy("Test Reality", { tradeVolume: 1000 });
        expect(console.log).toHaveBeenCalledWith(`Simulating economy in "Test Reality"...`);
    });

    test('should manage user interactions in the virtual reality', () => {
        bqil.createVirtualReality("Test Reality", { economyType: "barter" });
        const userActions = { action: "trade", amount: 100 };
        console.log = jest.fn(); // Mock console.log
        bqil.manageUserInteractions("Test Reality", userActions);
        expect(console.log).toHaveBeenCalledWith(`Managing user interactions in "Test Reality" with actions:`, userActions);
    });

    test('should destroy a virtual reality', () => {
        bqil.createVirtualReality("Test Reality", { economyType: "barter" });
        const result = bqil.destroyVirtualReality("Test Reality");
        expect(result).toBe(true);
        expect(bqil.anrf.virtualRealities.length).toBe(0); // Ensure the virtual reality is removed
    });
});
