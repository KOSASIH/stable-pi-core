// tests/ghrf.test.js

import GalacticHarmonyResonanceField from '../src/core/ghrf';

describe('GalacticHarmonyResonanceField', () => {
    let ghrf;
    let mockGalacticCore;
    let mockHarmonicLink;

    beforeEach(() => {
        mockGalacticCore = {
            synchronizeWithGHRF: jest.fn().mockResolvedValue(),
        };
        mockHarmonicLink = {
            synchronizeWithGHRF: jest.fn().mockResolvedValue(),
        };
        ghrf = new GalacticHarmonyResonanceField();
        ghrf.initialize(mockGalacticCore, mockHarmonicLink);
    });

    test('should initialize with default resonance frequency', () => {
        expect(ghrf.getResonanceFrequency()).toBe(432);
    });

    test('should set a new resonance frequency', () => {
        ghrf.setResonanceFrequency(440);
        expect(ghrf.getResonanceFrequency()).toBe(440);
    });

    test('should throw an error when setting a non-positive frequency', () => {
        expect(() => {
            ghrf.setResonanceFrequency(0);
        }).toThrow('Resonance frequency must be positive.');
    });

    test('should generate the resonance field', async () => {
        await ghrf.generateResonanceField();
        expect(ghrf.isFieldActive).toBe(true);
    });

    test('should synchronize the resonance field with QGC and HQL', async () => {
        await ghrf.generateResonanceField();
        await ghrf.synchronizeResonanceField();
        expect(mockGalacticCore.synchronizeWithGHRF).toHaveBeenCalledWith(ghrf.getResonanceFrequency());
        expect(mockHarmonicLink.synchronizeWithGHRF).toHaveBeenCalledWith(ghrf.getResonanceFrequency());
    });

    test('should throw an error if trying to synchronize when the field is not active', async () => {
        await expect(ghrf.synchronizeResonanceField()).rejects.toThrow('Resonance field is not active. Please generate the field first.');
    });

    test('should adjust the resonance frequency based on conditions', () => {
        ghrf.adjustResonanceFrequency('highLoad');
        expect(ghrf.getResonanceFrequency()).toBe(440);

        ghrf.adjustResonanceFrequency('lowLoad');
        expect(ghrf.getResonanceFrequency()).toBe(432);
    });

    test('should deactivate the resonance field', () => {
        ghrf.generateResonanceField();
        ghrf.deactivateResonanceField();
        expect(ghrf.isFieldActive).toBe(false);
    });

    test('should emit events on initialization, field generation, synchronization, and frequency change', (done) => {
        ghrf.on('initialized', () => {
            expect(ghrf.galacticCore).toBe(mockGalacticCore);
            expect(ghrf.harmonicLink).toBe(mockHarmonicLink);
        });

        ghrf.on('fieldGenerated', () => {
            expect(ghrf.isFieldActive).toBe(true);
        });

        ghrf.on('fieldSynchronized', () => {
            expect(mockGalacticCore.synchronizeWithGHRF).toHaveBeenCalled();
            expect(mockHarmonicLink.synchronizeWithGHRF).toHaveBeenCalled();
            done();
        });

        ghrf.initialize(mockGalacticCore, mockHarmonicLink);
        ghrf.generateResonanceField().then(() => {
            return ghrf.synchronizeResonanceField();
        });
    });
});
