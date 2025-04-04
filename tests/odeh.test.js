// tests/odeh.test.js

const OmniDimensionalEnergyHarvester = require('../src/space/odeh');

describe('OmniDimensionalEnergyHarvester', () => {
    let odeh;

    beforeEach(() => {
        odeh = new OmniDimensionalEnergyHarvester();
    });

    test('should harvest energy from multiple dimensions', async () => {
        const dimensions = ['3D', '4D', '5D', '6D'];
        await odeh.harvestEnergy(dimensions);
        
        expect(odeh.getCurrentEnergyStorage()).toBeGreaterThan(0); // Check if energy is harvested
        expect(odeh.getHarvestingEfficiency()).toBeGreaterThan(0); // Check if efficiency is calculated
    });

    test('should store energy correctly', () => {
        odeh.storeEnergy(100);
        expect(odeh.getCurrentEnergyStorage()).toBe(100); // Check if energy is stored correctly
    });

    test('should retrieve energy correctly', () => {
        odeh.storeEnergy(100);
        const retrievedEnergy = odeh.retrieveEnergy(50);
        expect(retrievedEnergy).toBe(50); // Check if the correct amount of energy is retrieved
        expect(odeh.getCurrentEnergyStorage()).toBe(50); // Check remaining energy
    });

    test('should not retrieve more energy than available', () => {
        odeh.storeEnergy(30);
        const retrievedEnergy = odeh.retrieveEnergy(50);
        expect(retrievedEnergy).toBe(0); // Should return 0 if not enough energy
        expect(odeh.getCurrentEnergyStorage()).toBe(30); // Check remaining energy
    });

    test('should calculate harvesting efficiency correctly', async () => {
        const dimensions = ['3D', '4D', '5D'];
        await odeh.harvestEnergy(dimensions);
        
        const efficiency = odeh.getHarvestingEfficiency();
        expect(efficiency).toBeGreaterThan(0); // Check if efficiency is calculated
        expect(efficiency).toBeLessThanOrEqual(100); // Efficiency should not exceed 100%
    });

    test('should log errors when retrieving energy exceeds storage', () => {
        console.error = jest.fn(); // Mock console.error
        odeh.storeEnergy(20);
        odeh.retrieveEnergy(50); // Attempt to retrieve more than stored
        expect(console.error).toHaveBeenCalledWith('Insufficient energy in storage.'); // Check error log
    });
});
