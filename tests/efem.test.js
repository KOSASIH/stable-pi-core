// tests/efem.test.js

const EternalFluxEvolutionMatrix = require('../src/core/efem');

describe('EternalFluxEvolutionMatrix', () => {
    let efem;

    beforeEach(() => {
        efem = new EternalFluxEvolutionMatrix();
    });

    test('should evolve features based on cosmic flux', async () => {
        const features = ['FeatureA', 'FeatureB', 'FeatureC'];
        const evolvedFeatures = await efem.evolveFeatures(features);
        
        expect(evolvedFeatures).toEqual(['FeatureA-Evolved', 'FeatureB-Evolved', 'FeatureC-Evolved']);
        expect(efem.getEvolutionHistory()).toHaveLength(1); // Check if evolution history is recorded
    });

    test('should record evolution history correctly', async () => {
        const features = ['FeatureX', 'FeatureY'];
        await efem.evolveFeatures(features);
        
        const history = efem.getEvolutionHistory();
        expect(history).toHaveLength(1);
        expect(history[0]).toHaveProperty('timestamp');
        expect(history[0]).toHaveProperty('flux');
        expect(history[0].features).toEqual(['FeatureX-Evolved', 'FeatureY-Evolved']);
    });

    test('should adapt features based on user feedback', async () => {
        const userFeedback = ['User Feature1', 'User Feature2'];
        const adaptedFeatures = await efem.adaptFeatures(userFeedback);
        
        expect(adaptedFeatures).toHaveLength(2);
        expect(adaptedFeatures[0]).toMatch(/User Feature1-Adapted-\d+/); // Check if adapted with flux
        expect(adaptedFeatures[1]).toMatch(/User Feature2-Adapted-\d+/); // Check if adapted with flux
        expect(efem.getEvolutionHistory()).toHaveLength(1); // Check if adaptation history is recorded
    });

    test('should throw an error if evolution fails', async () => {
        // Mock the harnessFlux method to throw an error
        jest.spyOn(efem.eqfc, 'harnessFlux').mockImplementation(() => {
            throw new Error('Flux harnessing failed');
        });

        await expect(efem.evolveFeatures(['FeatureA'])).rejects.toThrow('Evolution process failed.');
    });

    test('should throw an error if adaptation fails', async () => {
        // Mock the harnessFlux method to throw an error
        jest.spyOn(efem.eqfc, 'harnessFlux').mockImplementation(() => {
            throw new Error('Flux harnessing failed');
        });

        await expect(efem.adaptFeatures(['User Feature1'])).rejects.toThrow('Feature adaptation process failed.');
    });
});
