// tests/nsehm.test.js

import NeutronStarEnergyHarvestingModule from '../src/space/nsehm';

describe('NeutronStarEnergyHarvestingModule', () => {
    let nsehm;

    beforeEach(() => {
        nsehm = new NeutronStarEnergyHarvestingModule();
    });

    test('should initialize with zero energy storage', () => {
        expect(nsehm.energyStorage).toBe(0);
    });

    test('should harvest energy and store it', () => {
        nsehm.harvestEnergy();
        expect(nsehm.energyStorage).toBeGreaterThan(0); // Energy should be harvested
    });

    test('should calculate harvested energy based on cosmic radiation', () => {
        const initialStorage = nsehm.energyStorage;
        nsehm.harvestEnergy();
        expect(nsehm.energyStorage).toBeGreaterThan(initialStorage); // Energy should increase
    });

    test('should store energy without exceeding maximum capacity', () => {
        nsehm.maxStorageCapacity = 100; // Set a lower max capacity for testing
        nsehm.storeEnergy(50);
        nsehm.storeEnergy(60); // This should trigger a warning
        expect(nsehm.energyStorage).toBe(nsehm.maxStorageCapacity); // Should cap at max capacity
    });

    test('should retrieve stored energy correctly', () => {
        nsehm.storeEnergy(100);
        const retrievedEnergy = nsehm.retrieveEnergy(50);
        expect(retrievedEnergy).toBe(50); // Should retrieve the requested amount
        expect(nsehm.energyStorage).toBe(50); // Remaining energy should be 50
    });

    test('should warn when retrieving more energy than stored', () => {
        console.warn = jest.fn(); // Mock console.warn
        nsehm.storeEnergy(30);
        const retrievedEnergy = nsehm.retrieveEnergy(50); // Request more than available
        expect(retrievedEnergy).toBe(30); // Should retrieve maximum available
        expect(console.warn).toHaveBeenCalledWith("Warning: Not enough energy stored. Retrieving maximum available energy.");
    });

    test('should get current energy storage status', () => {
        nsehm.storeEnergy(500);
        const status = nsehm.getEnergyStorageStatus();
        expect(status).toEqual({
            currentStorage: 500,
            maxCapacity: nsehm.maxStorageCapacity,
        });
    });

    test('should reset energy storage', () => {
        nsehm.storeEnergy(100);
        nsehm.resetEnergyStorage();
        expect(nsehm.energyStorage).toBe(0); // Energy storage should be reset to zero
    });

    test('should simulate quantum flux fluctuations', () => {
        nsehm.simulateQuantumFluxFluctuation();
        expect(nsehm.quantumFlux).toBeGreaterThanOrEqual(0); // Quantum flux should be a valid number
        expect(nsehm.quantumFlux).toBeLessThan(1); // Quantum flux should be less than 1
    });

    test('should self-sustain energy harvesting when storage is low', () => {
        nsehm.maxStorageCapacity = 100; // Set a lower max capacity for testing
        nsehm.storeEnergy(30); // Below half capacity
        const initialStorage = nsehm.energyStorage;
        nsehm.selfSustainEnergyHarvesting();
        expect(nsehm.energyStorage).toBeGreaterThan(initialStorage); // Energy should be harvested
    });

    test('should not self-sustain energy harvesting when storage is sufficient', () => {
        nsehm.maxStorageCapacity = 100; // Set a lower max capacity for testing
        nsehm.storeEnergy(70); // Above half capacity
        const initialStorage = nsehm.energyStorage;
        nsehm.selfSustainEnergyHarvesting();
        expect(nsehm.energyStorage).toBe(initialStorage); // Energy should not be harvested
    });
});
