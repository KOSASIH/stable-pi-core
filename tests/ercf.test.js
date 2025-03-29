// tests/ercf.test.js

const EternalResonanceContinuityField = require('../src/tokens/ercf');

describe('Eternal Resonance Continuity Field', () => {
    let ercf;

    beforeEach(() => {
        ercf = new EternalResonanceContinuityField();
    });

    test('should initialize with inactive status', () => {
        expect(ercf.isActive).toBe(false);
        expect(ercf.resonanceFrequency).toBe(0);
        expect(ercf.entropyResistanceLevel).toBe(100);
    });

    test('should activate the ERCF', () => {
        ercf.activate();
        expect(ercf.isActive).toBe(true);
        expect(ercf.resonanceFrequency).toBeGreaterThan(0);
    });

    test('should not activate if already active', () => {
        ercf.activate();
        const consoleSpy = jest.spyOn(console, 'log');
        ercf.activate();
        expect(consoleSpy).toHaveBeenCalledWith('Eternal Resonance Continuity Field is already active.');
        consoleSpy.mockRestore();
    });

    test('should deactivate the ERCF', () => {
        ercf.activate();
        ercf.deactivate();
        expect(ercf.isActive).toBe(false);
    });

    test('should not deactivate if already inactive', () => {
        const consoleSpy = jest.spyOn(console, 'log');
        ercf.deactivate();
        expect(consoleSpy).toHaveBeenCalledWith('Eternal Resonance Continuity Field is already inactive.');
        consoleSpy.mockRestore();
    });

    test('should protect against cosmic entropy when active', () => {
        ercf.activate();
        const consoleSpy = jest.spyOn(console, 'log');
        ercf.protectAgainstEntropy(30); // Below threshold
        expect(consoleSpy).toHaveBeenCalledWith('Data is being protected from cosmic entropy...');
        consoleSpy.mockRestore();
    });

    test('should warn when protection level is low', () => {
        ercf.activate();
        ercf.entropyResistanceLevel = 40; // Set below threshold
        const consoleSpy = jest.spyOn(console, 'warn');
        ercf.protectAgainstEntropy(60); // Above threshold
        expect(consoleSpy).toHaveBeenCalledWith("Warning: Protection level is low. Data may be at risk of degradation.");
        consoleSpy.mockRestore();
    });

    test('should not protect against entropy when inactive', () => {
        const consoleSpy = jest.spyOn(console, 'error');
        ercf.protectAgainstEntropy(60); // Above threshold
        expect(consoleSpy).toHaveBeenCalledWith('Cannot protect against entropy. ERCF is inactive.');
        consoleSpy.mockRestore();
    });

    test('should return status of the ERCF', () => {
        ercf.activate();
        const status = ercf.getStatus();
        expect(status).toEqual(expect.objectContaining({
            isActive: true,
            resonanceFrequency: expect.any(Number),
            entropyResistanceLevel: 100
        }));
    });

    test('should reset protection level', () => {
        ercf.entropyResistanceLevel = 50; // Change protection level
        ercf.resetProtection();
        expect(ercf.entropyResistanceLevel).toBe(100);
    });
});
