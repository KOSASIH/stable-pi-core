// tests/csp.test.js

import CosmicSingularityProcessor from '../src/core/csp';

describe('CosmicSingularityProcessor', () => {
    let csp;

    beforeEach(() => {
        csp = new CosmicSingularityProcessor();
    });

    test('should initialize with zero computational power', () => {
        expect(csp.getComputationalPower()).toBe(0);
    });

    test('should simulate a black hole singularity', () => {
        csp.singularitySimulation.updateSingularity('black hole', 1000);
        csp.simulateSingularity();
        expect(csp.getComputationalPower()).toBe(1000);
    });

    test('should simulate a Big Bang singularity', () => {
        csp.singularitySimulation.updateSingularity('Big Bang', 5000);
        csp.simulateSingularity();
        expect(csp.getComputationalPower()).toBe(5000);
    });

    test('should amplify computational power', () => {
        csp.singularitySimulation.updateSingularity('black hole', 2000);
        csp.amplifyComputationalPower();
        expect(csp.getComputationalPower()).toBe(2000);
        
        csp.singularitySimulation.updateSingularity('Big Bang', 3000);
        csp.amplifyComputationalPower();
        expect(csp.getComputationalPower()).toBe(5000); // 2000 + 3000
    });

    test('should track history of computational power changes', () => {
        csp.singularitySimulation.updateSingularity('black hole', 1000);
        csp.amplifyComputationalPower();
        csp.singularitySimulation.updateSingularity('Big Bang', 2000);
        csp.amplifyComputationalPower();

        const history = csp.getHistory();
        expect(history).toHaveLength(2);
        expect(history[0]).toEqual(expect.objectContaining({
            type: 'black hole',
            amplification: 1000,
        }));
        expect(history[1]).toEqual(expect.objectContaining({
            type: 'Big Bang',
            amplification: 2000,
        }));
    });

    test('should reset computational power and history', () => {
        csp.singularitySimulation.updateSingularity('black hole', 1000);
        csp.amplifyComputationalPower();
        expect(csp.getComputationalPower()).toBe(1000);
        expect(csp.getHistory()).toHaveLength(1);

        csp.resetComputationalPower();
        expect(csp.getComputationalPower()).toBe(0);
        expect(csp.getHistory()).toHaveLength(0);
    });
});
