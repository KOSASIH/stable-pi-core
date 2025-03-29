// tests/ocsi.test.js

const OmniCosmicSymbioticInterface = require('./ocsi');

describe('OmniCosmicSymbioticInterface', () => {
    let ocsi;

    beforeEach(() => {
        ocsi = new OmniCosmicSymbioticInterface();
    });

    test('should establish symbiosis with a valid cosmic entity', () => {
        const star = { name: 'Sirius', type: 'star' };
        ocsi.establishSymbiosis(star);
        expect(ocsi.listSymbioticEntities()).toContain(star);
    });

    test('should not establish symbiosis with an invalid entity', () => {
        const invalidEntity = { name: 'Invalid', type: 'planet' };
        ocsi.establishSymbiosis(invalidEntity);
        expect(ocsi.listSymbioticEntities()).not.toContain(invalidEntity);
    });

    test('should enhance functionality for a star entity', () => {
        const star = { name: 'Sirius', type: 'star' };
        console.log = jest.fn(); // Mock console.log to capture output
        ocsi.establishSymbiosis(star);
        expect(console.log).toHaveBeenCalledWith('Enhancing energy generation capabilities using Sirius.');
    });

    test('should enhance functionality for a black hole entity', () => {
        const blackHole = { name: 'Cygnus X-1', type: 'black hole' };
        console.log = jest.fn(); // Mock console.log to capture output
        ocsi.establishSymbiosis(blackHole);
        expect(console.log).toHaveBeenCalledWith('Enhancing data storage and gravitational manipulation using Cygnus X-1.');
    });

    test('should enhance functionality for a nebula entity', () => {
        const nebula = { name: 'Orion Nebula', type: 'nebula' };
        console.log = jest.fn(); // Mock console.log to capture output
        ocsi.establishSymbiosis(nebula);
        expect(console.log).toHaveBeenCalledWith('Enhancing material synthesis and cosmic resource gathering using Orion Nebula.');
    });

    test('should remove a symbiotic relationship', () => {
        const star = { name: 'Sirius', type: 'star' };
        ocsi.establishSymbiosis(star);
        expect(ocsi.listSymbioticEntities()).toContain(star);
        
        ocsi.removeSymbiosis(star);
        expect(ocsi.listSymbioticEntities()).not.toContain(star);
    });

    test('should not remove a non-existent symbiotic relationship', () => {
        const star = { name: 'Sirius', type: 'star' };
        ocsi.removeSymbiosis(star); // Attempt to remove without establishing
        expect(ocsi.listSymbioticEntities()).not.toContain(star);
    });

    test('should list all symbiotic entities', () => {
        const star = { name: 'Sirius', type: 'star' };
        const blackHole = { name: 'Cygnus X-1', type: 'black hole' };
        ocsi.establishSymbiosis(star);
        ocsi.establishSymbiosis(blackHole);
        
        const entities = ocsi.listSymbioticEntities();
        expect(entities).toContain(star);
        expect(entities).toContain(blackHole);
    });

    test('should log current symbiotic relationships', () => {
        const star = { name: 'Sirius', type: 'star' };
        const blackHole = { name: 'Cygnus X-1', type: 'black hole' };
        ocsi.establishSymbiosis(star);
        ocsi.establishSymbiosis(blackHole);
        
        console.log = jest.fn(); // Mock console.log to capture output
        ocsi.logSymbioticRelationships();
        expect(console.log).toHaveBeenCalledWith('Current symbiotic relationships:');
        expect(console.log).toHaveBeenCalledWith('- Sirius (star)');
        expect(console.log).toHaveBeenCalledWith('- Cygnus X-1 (black hole)');
    });
});
