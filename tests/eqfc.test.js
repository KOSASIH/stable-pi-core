// tests/eqfc.test.js

import EternalQuantumFluxCapacitor from '../src/space/eqfc';

describe('EternalQuantumFluxCapacitor', () => {
    let eqfc;

    beforeEach(() => {
        eqfc = new EternalQuantumFluxCapacitor();
    });

    test('should initialize with zero energy storage', () => {
        expect(eqfc.getCurrentEnergyStorage()).toBe(0);
    });

    test('should store energy correctly', () => {
        eqfc.storeEnergy(100);
        expect(eqfc.getCurrentEnergyStorage()).toBe(100);
    });

    test('should throw an error when storing negative energy', () => {
        expect(() => {
            eqfc.storeEnergy(-50);
        }).toThrow('Cannot store negative energy.');
    });

    test('should distribute energy correctly', () => {
        eqfc.storeEnergy(200);
        const distributedEnergy = eqfc.distributeEnergy(100);
        expect(distributedEnergy).toBe(100);
        expect(eqfc.getCurrentEnergyStorage()).toBe(100);
    });

    test('should throw an error when distributing more energy than available', () => {
        eqfc.storeEnergy(50);
        expect(() => {
            eqfc.distributeEnergy(100);
        }).toThrow('Insufficient energy storage.');
    });

    test('should throw an error when distributing negative energy', () => {
        expect(() => {
            eqfc.distributeEnergy(-50);
        }).toThrow('Cannot distribute negative energy.');
    });

    test('should set and get the energy distribution rate', () => {
        eqfc.setEnergyDistributionRate(2e6);
        expect(eqfc.getEnergyDistributionRate()).toBe(2e6);
    });

    test('should throw an error when setting a non-positive distribution rate', () => {
        expect(() => {
            eqfc.setEnergyDistributionRate(0);
        }).toThrow('Distribution rate must be positive.');
    });

    test('should convert dark matter energy correctly', async () => {
        const convertedEnergy = await eqfc.convertDarkMatterEnergy(100);
        expect(eqfc.getCurrentEnergyStorage()).toBe(150); // 100 * 1.5
        expect(convertedEnergy).toBe(150);
    });

    test('should predict future energy needs based on usage patterns', () => {
        const usagePatterns = [50, 100, 150];
        const predictedNeeds = eqfc.predictEnergyNeeds(usagePatterns);
        expect(predictedNeeds).toBe(300); // 50 + 100 + 150
    });

    test('should safely distribute energy based on predicted needs', async () => {
        eqfc.storeEnergy(500);
        const distributedEnergy = await eqfc.safeDistributeEnergy(300);
        expect(distributedEnergy).toBe(300);
        expect(eqfc.getCurrentEnergyStorage()).toBe(200);
    });

    test('should warn when trying to safely distribute more energy than available', async () => {
        eqfc.storeEnergy(200);
        await expect(eqfc.safeDistributeEnergy(300)).rejects.toThrow('Insufficient energy storage.');
    });
});
