// tests/gers.test.js

import GalacticEntropyReversalSystem from '../src/core/gers';

describe('GalacticEntropyReversalSystem', () => {
    let gers;

    beforeEach(() => {
        gers = new GalacticEntropyReversalSystem();
    });

    test('should initialize GERS with a Dark Matter Energy Converter', () => {
        const mockConverter = {}; // Mock Dark Matter Energy Converter
        gers.initializeGERS(mockConverter);
        expect(gers.darkMatterEnergyConverter).toBe(mockConverter);
        expect(gers.isActive).toBe(true);
    });

    test('should throw an error when reversing entropy if GERS is not active', () => {
        const data = { example: 'data' };
        gers.deactivateGERS(); // Ensure GERS is inactive
        expect(() => {
            gers.reverseEntropy(data);
        }).toThrow('GERS is not active. Please initialize the system.');
    });

    test('should reverse entropy on a given data set', () => {
        const data = { example: 'data' };
        gers.initializeGERS({}); // Initialize with a mock converter
        const reversedData = gers.reverseEntropy(data);
        expect(reversedData).toEqual({ example: 'data', entropyReversed: true });
    });

    test('should update the entropy level correctly', () => {
        gers.initializeGERS({}); // Initialize with a mock converter
        gers.updateEntropyLevel(1);
        expect(gers.getEntropyLevel()).toBe(1);
        gers.updateEntropyLevel(-1);
        expect(gers.getEntropyLevel()).toBe(0);
    });

    test('should get the current entropy level', () => {
        gers.initializeGERS({}); // Initialize with a mock converter
        gers.updateEntropyLevel(2);
        expect(gers.getEntropyLevel()).toBe(2);
    });

    test('should deactivate the GERS', () => {
        gers.initializeGERS({}); // Initialize with a mock converter
        gers.deactivateGERS();
        expect(gers.isActive).toBe(false);
    });

    test('should throw an error when harnessing energy if converter is not initialized', () => {
        expect(() => {
            gers.harnessDarkMatterEnergy();
        }).toThrow('Dark Matter Energy Converter is not initialized.');
    });

    test('should harness energy from Dark Matter', () => {
        const mockConverter = {}; // Mock Dark Matter Energy Converter
        gers.initializeGERS(mockConverter);
        const result = gers.harnessDarkMatterEnergy();
        expect(result).toBe('Energy harnessed successfully.');
    });
});
