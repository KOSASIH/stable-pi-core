// tests/sebd.test.js

import SelfEvolvingBlockchainDNA from '../src/core/sebd';

describe('SelfEvolvingBlockchainDNA', () => {
    let sebd;

    beforeEach(() => {
        sebd = new SelfEvolvingBlockchainDNA();
    });

    test('should initialize with an empty genetic pool', () => {
        expect(sebd.geneticPool).toEqual([]);
    });

    test('should add valid genetic information', () => {
        const geneticData = { fitness: 0.8 };
        sebd.addGeneticInformation(geneticData);
        expect(sebd.geneticPool).toContain(geneticData);
    });

    test('should throw error when adding invalid genetic information', () => {
        expect(() => sebd.addGeneticInformation(null)).toThrow("Invalid genetic information. Must be an object with a fitness property.");
        expect(() => sebd.addGeneticInformation({})).toThrow("Invalid genetic information. Must be an object with a fitness property.");
    });

    test('should evolve the blockchain if average fitness exceeds threshold', () => {
        sebd.addGeneticInformation({ fitness: 0.2 });
        sebd.addGeneticInformation({ fitness: 0.3 });
        sebd.addGeneticInformation({ fitness: 0.4 });
        
        const initialFitness = sebd.calculateAverageFitness();
        sebd.evolveBlockchain();
        
        expect(sebd.calculateAverageFitness()).toBeGreaterThan(initialFitness); // Fitness should increase
    });

    test('should not evolve the blockchain if average fitness is below threshold', () => {
        sebd.addGeneticInformation({ fitness: 0.1 });
        sebd.addGeneticInformation({ fitness: 0.1 });
        
        const initialFitness = sebd.calculateAverageFitness();
        sebd.evolveBlockchain();
        
        expect(sebd.calculateAverageFitness()).toEqual(initialFitness); // Fitness should remain the same
    });

    test('should throw error if evolving without genetic information', () => {
        expect(() => sebd.evolveBlockchain()).toThrow("No genetic information available for evolution.");
    });

    test('should integrate with Holographic Quantum Ledger', () => {
        const integrateSpy = jest.spyOn(sebd, 'addGeneticInformation');
        sebd.integrateWithLedger();
        expect(integrateSpy).toHaveBeenCalled(); // Ensure integration method was called
    });

    test('should reset the genetic pool', () => {
        sebd.addGeneticInformation({ fitness: 0.5 });
        sebd.resetGeneticPool();
        expect(sebd.geneticPool).toEqual([]); // Genetic pool should be empty
    });

    test('should self-heal by removing low-fitness genes', () => {
        sebd.addGeneticInformation({ fitness: 0.1 });
        sebd.addGeneticInformation({ fitness: 0.3 });
        sebd.addGeneticInformation({ fitness: 0.05 }); // Low fitness
        
        sebd.selfHeal();
        expect(sebd.geneticPool).toHaveLength(2); // One low-fitness gene should be removed
    });

    test('should simulate gravitational wave detection and add genetic information', () => {
        sebd.simulateGravitationalWaveDetection();
        expect(sebd.geneticPool).toHaveLength(1); // One genetic entry should be added
    });
});
