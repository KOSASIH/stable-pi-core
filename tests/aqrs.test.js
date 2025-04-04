// tests/aqrs.test.js

const AstroQuantumRealitySynthesizer = require('../../src/core/aqrs');

describe('AstroQuantumRealitySynthesizer', () => {
    let aqrs;

    beforeEach(() => {
        aqrs = new AstroQuantumRealitySynthesizer();
    });

    test('should synthesize a new reality', async () => {
        const parameters = { type: 'Trade Simulation', features: ['immersive', 'interactive'] };
        const environment = await aqrs.synthesizeReality(parameters);
        
        expect(environment).toHaveProperty('id');
        expect(environment.type).toBe('Trade Simulation');
        expect(environment.features).toContain('immersive');
        expect(environment.features).toContain('interactive');
        expect(aqrs.getAllEnvironments()).toContainEqual(environment);
    });

    test('should throw an error when synthesizing reality fails', async () => {
        // Mock the createSyntheticEnvironment method to throw an error
        jest.spyOn(aqrs.anrf, 'createSyntheticEnvironment').mockImplementation(() => {
            throw new Error('Environment creation failed');
        });

        await expect(aqrs.synthesizeReality({})).rejects.toThrow('Failed to synthesize reality');
    });

    test('should stabilize the quantum field for a new environment', async () => {
        const parameters = { type: 'Trade Simulation', features: ['immersive', 'interactive'] };
        const environment = await aqrs.synthesizeReality(parameters);
        
        expect(environment.stabilized).toBe(true);
    });

    test('should simulate an operation in a specific environment', async () => {
        const parameters = { type: 'Trade Simulation', features: ['immersive', 'interactive'] };
        const environment = await aqrs.synthesizeReality(parameters);
        
        const operationResult = await aqrs.simulateOperation(environment.id, 'Trade Negotiation');
        expect(operationResult).toHaveProperty('environmentId', environment.id);
        expect(operationResult.operation).toBe('Trade Negotiation');
        expect(operationResult.result).toContain('completed successfully');
    });

    test('should throw an error when simulating an operation in a non-existent environment', async () => {
        await expect(aqrs.simulateOperation('non-existent-id', 'Trade Negotiation')).rejects.toThrow('Environment not found');
    });

    test('should adjust environment parameters dynamically', async () => {
        const parameters = { type: 'Trade Simulation', features: ['immersive', 'interactive'] };
        const environment = await aqrs.synthesizeReality(parameters);
        
        const adjustedEnvironment = aqrs.adjustEnvironment(environment.id, { features: ['immersive', 'interactive', 'AI-driven'] });
        expect(adjustedEnvironment.features).toContain('AI-driven');
        expect(adjustedEnvironment.features).toHaveLength(3); // Should have 3 features now
    });

    test('should throw an error when adjusting a non-existent environment', () => {
        expect(() => {
            aqrs.adjustEnvironment('non-existent-id', { features: ['new-feature'] });
        }).toThrow('Environment not found');
    });
});
