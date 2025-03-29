// tests/singularitySeedGenerator.test.js

const SingularitySeedGenerator = require('./singularitySeedGenerator');

describe('SingularitySeedGenerator', () => {
    let ssg;

    beforeEach(() => {
        ssg = new SingularitySeedGenerator();
    });

    test('should activate the generator', () => {
        ssg.activate();
        expect(ssg.isActive).toBe(true);
    });

    test('should deactivate the generator', () => {
        ssg.activate();
        ssg.deactivate();
        expect(ssg.isActive).toBe(false);
    });

    test('should generate singularity when activated', () => {
        ssg.activate();
        ssg.generateSingularity();
        expect(ssg.getEnergyOutput()).toBeGreaterThan(0);
        expect(ssg.getStorageCapacity()).toBeGreaterThan(0);
    });

    test('should not generate singularity when inactive', () => {
        ssg.generateSingularity();
        expect(ssg.getEnergyOutput()).toBe(0);
        expect(ssg.getStorageCapacity()).toBe(0);
    });

    test('should respect the safety threshold for energy output', () => {
        ssg.activate();
        // Force a high energy output for testing
        ssg.maxEnergyOutput = 1e12; // Set max energy output
        ssg.safetyThreshold = 0.5; // Set safety threshold to 50%
        
        ssg.generateSingularity();
        expect(ssg.getEnergyOutput()).toBeLessThanOrEqual(ssg.maxEnergyOutput * ssg.safetyThreshold);
    });

    test('should integrate with Dark Matter Energy Converter', () => {
        const mockConverter = {
            convertEnergy: jest.fn()
        };
        ssg.setDarkMatterEnergyConverter(mockConverter);
        
        ssg.activate();
        ssg.generateSingularity();
        
        expect(mockConverter.convertEnergy).toHaveBeenCalledWith(ssg.getEnergyOutput());
    });

    test('should reset the generator', () => {
        ssg.activate();
        ssg.generateSingularity();
        ssg.reset();
        
        expect(ssg.getEnergyOutput()).toBe(0);
        expect(ssg.getStorageCapacity()).toBe(0);
    });

    test('should not throw error when deactivating an inactive generator', () => {
        expect(() => ssg.deactivate()).not.toThrow();
    });

    test('should not throw error when generating singularity while inactive', () => {
        expect(() => ssg.generateSingularity()).not.toThrow();
    });
});
