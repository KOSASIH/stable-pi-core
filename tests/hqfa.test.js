const HyperQuantumFluxAmplifier = require('../src/quantum/hqfa'); // Adjust the import path as necessary

describe('HyperQuantumFluxAmplifier', () => {
    beforeEach(() => {
        HyperQuantumFluxAmplifier.resetFluxLevel(); // Reset flux level before each test
    });

    test('should amplify flux correctly', async () => {
        const inputFlux = 50;
        const expectedFluxLevel = 100; // Default amplification factor is 2
        const amplifiedFlux = await HyperQuantumFluxAmplifier.amplifyFlux(inputFlux);
        expect(amplifiedFlux).toBe(expectedFluxLevel);
        expect(HyperQuantumFluxAmplifier.getCurrentFluxLevel()).toBe(expectedFluxLevel);
    });

    test('should throw an error if amplification is already in progress', async () => {
        await HyperQuantumFluxAmplifier.amplifyFlux(50); // Start amplification
        await expect(HyperQuantumFluxAmplifier.amplifyFlux(50)).rejects.toThrow("Amplification process is already in progress.");
    });

    test('should set the amplification factor correctly', () => {
        HyperQuantumFluxAmplifier.setAmplificationFactor(3);
        expect(HyperQuantumFluxAmplifier.amplificationFactor).toBe(3);
    });

    test('should throw an error when setting an invalid amplification factor', () => {
        expect(() => {
            HyperQuantumFluxAmplifier.setAmplificationFactor(0); // Invalid factor
        }).toThrow("Amplification factor must be greater than zero.");
    });

    test('should reset the flux level to zero', () => {
        HyperQuantumFluxAmplifier.amplifyFlux(50); // Amplify first
        expect(HyperQuantumFluxAmplifier.getCurrentFluxLevel()).toBe(100);
        HyperQuantumFluxAmplifier.resetFluxLevel(); // Reset
        expect(HyperQuantumFluxAmplifier.getCurrentFluxLevel()).toBe(0);
    });

    test('should monitor the quantum state correctly', async () => {
        await HyperQuantumFluxAmplifier.amplifyFlux(50); // Amplify first
        const quantumState = HyperQuantumFluxAmplifier.monitorQuantumState();
        expect(quantumState.fluxLevel).toBe(100);
        expect(quantumState.amplificationFactor).toBe(2);
        expect(quantumState.isAmplifying).toBe(false);
    });
});
