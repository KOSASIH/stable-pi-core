// tests/cqma.test.js

import CosmoQuantumMorphicAdaptor from '../../src/space/cqma';
import AstroQuantumEvolutionCatalyst from '../../src/space/cqma'; // Assuming AQEC is in this file

jest.mock('../../src/space/cqma'); // Mock the AQEC class

describe('CosmoQuantumMorphicAdaptor', () => {
    let cqma;

    beforeEach(() => {
        cqma = new CosmoQuantumMorphicAdaptor();
    });

    test('should update environmental conditions', () => {
        const conditions = { gravity: 'extreme', radiationLevel: 1200 };
        cqma.updateEnvironmentalConditions('black hole', conditions);
        
        expect(cqma.environmentalConditions['black hole']).toEqual(conditions);
    });

    test('should adapt to black hole environment', () => {
        const conditions = { gravity: 'extreme', radiationLevel: 1200 };
        cqma.updateEnvironmentalConditions('black hole', conditions);
        
        expect(cqma.aqec.enhanceNodeForBlackHole).toHaveBeenCalledWith(conditions);
        expect(cqma.nodeState).toEqual({
            density: 'extreme',
            energyAbsorption: 'high',
            gravitationalStability: 'high'
        });
    });

    test('should adapt to nebula environment', () => {
        const conditions = { density: 0.05, gasComposition: 'hydrogen' };
        cqma.updateEnvironmentalConditions('nebula', conditions);
        
        expect(cqma.aqec.enhanceNodeForNebula).toHaveBeenCalledWith(conditions);
        expect(cqma.nodeState).toEqual({
            visibility: 'high',
            gasInteraction: 'high',
            energyDispersion: 'medium'
        });
    });

    test('should adapt to vacuum environment', () => {
        const conditions = { pressure: 'zero', temperature: 'absolute zero' };
        cqma.updateEnvironmentalConditions('vacuum', conditions);
        
        expect(cqma.aqec.enhanceNodeForVacuum).toHaveBeenCalledWith(conditions);
        expect(cqma.nodeState).toEqual({
            stability: 'high',
            energyConservation: 'optimal',
            structuralIntegrity: 'enhanced'
        });
    });

    test('should adapt to supernova environment', () => {
        const conditions = { explosionIntensity: 'high', radiationLevel: 5000 };
        cqma.updateEnvironmentalConditions('supernova', conditions);
        
        expect(cqma.aqec.enhanceNodeForSupernova).toHaveBeenCalledWith(conditions);
        expect(cqma.nodeState).toEqual({
            resilience: 'extreme',
            energyOutput: 'high',
            shockwaveAbsorption: 'advanced'
        });
    });

    test('should adapt to dark matter environment', () => {
        const conditions = { darkMatterDensity: 'high', energyManipulationAbility: 'advanced' };
        cqma.updateEnvironmentalConditions('dark matter', conditions);
        
        expect(cqma.aqec.enhanceNodeForDarkMatter).toHaveBeenCalledWith(conditions);
        expect(cqma.nodeState).toEqual({
            darkMatterInteraction: 'high',
            energyManipulation: 'advanced',
            stability: 'enhanced'
        });
    });

    test('should log error for unknown environment type', () => {
        console.warn = jest.fn(); // Mock console.warn
        cqma.adaptToEnvironment('unknown');
        
        expect(console.warn).toHaveBeenCalledWith(expect.stringContaining("Unknown environment type: unknown"));
    });

    test('should log error for missing conditions', () => {
        console.error = jest.fn(); // Mock console.error
        cqma.adaptToEnvironment('black hole'); // No conditions set
        
        expect(console.error).toHaveBeenCalledWith(expect.stringContaining("No conditions found for environment type: black hole"));
    });
});
