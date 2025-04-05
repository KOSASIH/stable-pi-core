// tests/esc.test.js
const EternalSingularityCore = require('../src/core/esc');

describe('EternalSingularityCore Tests', () => {
    beforeEach(() => {
        // Reset the instance before each test
        EternalSingularityCore.resetEnergyStorage();
    });

    test('should generate base energy', async () => {
        const energy = await EternalSingularityCore.generateEnergy();
        expect(energy).toBe(100); // Default generation rate
        expect(EternalSingularityCore.getTotalEnergy()).toBe(100);
    });

    test('should generate energy with a factor', async () => {
        const energy = await EternalSingularityCore.generateEnergy(1.5);
        expect(energy).toBe(150); // 100 * 1.5
        expect(EternalSingularityCore.getTotalEnergy()).toBe(150);
    });

    test('should store total energy generated', async () => {
        await EternalSingularityCore.generateEnergy();
        await EternalSingularityCore.generateEnergy(2);
        expect(EternalSingularityCore.getTotalEnergy()).toBe(300); // 100 + 200
    });

    test('should retrieve energy generation history', async () => {
        await EternalSingularityCore.generateEnergy();
        await EternalSingularityCore.generateEnergy(1.5);
        
        const history = EternalSingularityCore.getEnergyHistory();
        expect(history.length).toBe(2);
        expect(history[0]).toEqual(expect.objectContaining({
            energy: 100,
            timestamp: expect.any(String),
        }));
        expect(history[1]).toEqual(expect.objectContaining({
            energy: 150,
            timestamp: expect.any(String),
        }));
    });

    test('should reset energy storage', async () => {
        await EternalSingularityCore.generateEnergy();
        expect(EternalSingularityCore.getTotalEnergy()).toBe(100);
        
        EternalSingularityCore.resetEnergyStorage();
        expect(EternalSingularityCore.getTotalEnergy()).toBe(0);
        expect(EternalSingularityCore.getEnergyHistory()).toEqual([]);
    });

    test('should simulate energy generation over time', async () => {
        jest.useFakeTimers(); // Use fake timers for simulation
        const duration = 6; // 6 seconds
        const interval = 2; // 2 seconds

        const simulationPromise = EternalSingularityCore.simulateEnergyGeneration(duration, interval);
        
        jest.advanceTimersByTime(6000); // Fast-forward time by 6 seconds
        await simulationPromise; // Wait for the simulation to complete

        expect(EternalSingularityCore.getTotalEnergy()).toBe(300); // 100 * 3 (3 intervals)
        expect(EternalSingularityCore.getEnergyHistory().length).toBe(3); // 3 entries in history
    });
});
