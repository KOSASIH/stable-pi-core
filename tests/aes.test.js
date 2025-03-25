import AethericEnergySynthesizer from '../src/space/aes';

describe('AethericEnergySynthesizer', () => {
    let aes;

    beforeEach(() => {
        aes = new AethericEnergySynthesizer();
    });

    test('should initialize with energy level 0', () => {
        expect(aes.getEnergyLevel()).toBe(0);
    });

    test('should start synthesis process', () => {
        aes.startSynthesis();
        expect(aes.isSynthesizerActive()).toBe(true);
    });

    test('should stop synthesis process', () => {
        aes.startSynthesis();
        aes.stopSynthesis();
        expect(aes.isSynthesizerActive()).toBe(false);
    });

    test('should synthesize energy and increase energy level', async () => {
        aes.startSynthesis();
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds
        expect(aes.getEnergyLevel()).toBeGreaterThan(0);
        aes.stopSynthesis();
    });

    test('should reset energy level to zero', () => {
        aes.startSynthesis();
        aes.stopSynthesis();
        aes.resetEnergyLevel();
        expect(aes.getEnergyLevel()).toBe(0);
    });

    test('should set energy demand and adjust synthesis rate', async () => {
        aes.startSynthesis();
        aes.setEnergyDemand(300); // Set high demand
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds
        expect(aes.synthesisRate).toBeGreaterThan(100); // Check if synthesis rate increased
        aes.stopSynthesis();
    });

    test('should alert when energy level is below threshold', async () => {
        const consoleSpy = jest.spyOn(console, 'warn').mockImplementation(); // Spy on console.warn
        aes.startSynthesis();
        aes.setEnergyDemand(1000); // Set very high demand
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds
        expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Warning: Energy level is critically low'));
        aes.stopSynthesis();
        consoleSpy.mockRestore(); // Restore original console.warn
    });

    test('should not exceed maximum energy capacity', async () => {
        aes.startSynthesis();
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait for 2 seconds
        expect(aes.getEnergyLevel()).toBeLessThanOrEqual(aes.maxEnergyCapacity);
        aes.stopSynthesis();
    });
});
