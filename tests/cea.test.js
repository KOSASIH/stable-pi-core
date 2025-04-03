const cea = require('../src/core/cea');

describe('Cosmic Evolution Accelerator', () => {
    test('should simulate evolution for a given time', async () => {
        const realTimeSeconds = 1; // Simulate for 1 second
        const { evolutionData, analysis } = await cea.accelerateEvolution(realTimeSeconds);
        
        expect(evolutionData).toBeDefined();
        expect(evolutionData.length).toBe(1000000); // Should simulate 1 million years
        expect(evolutionData[0]).toHaveProperty('year');
        expect(evolutionData[0]).toHaveProperty('technologyLevel');
        expect(evolutionData[0]).toHaveProperty('ecosystemDiversity');

        // Check analysis results
        expect(analysis).toHaveProperty('averageTechnologyLevel');
        expect(analysis).toHaveProperty('averageEcosystemDiversity');
        expect(analysis.averageTechnologyLevel).toBeGreaterThan(0);
        expect(analysis.averageEcosystemDiversity).toBeGreaterThan(0);
    });

    test('should handle zero real time', async () => {
        const { evolutionData, analysis } = await cea.accelerateEvolution(0); // Simulate for 0 seconds
        expect(evolutionData).toEqual([]); // No evolution data should be generated
        expect(analysis).toEqual({
            averageTechnologyLevel: 0,
            averageEcosystemDiversity: 0
        });
    });

    test('should simulate evolution with varying real time', async () => {
        const realTimeSeconds = 2; // Simulate for 2 seconds
        const { evolutionData, analysis } = await cea.accelerateEvolution(realTimeSeconds);
        
        expect(evolutionData).toBeDefined();
        expect(evolutionData.length).toBe(2000000); // Should simulate 2 million years
        expect(analysis.averageTechnologyLevel).toBeGreaterThan(0);
        expect(analysis.averageEcosystemDiversity).toBeGreaterThan(0);
    });

    test('should produce consistent results for the same input', async () => {
        const realTimeSeconds = 1; // Simulate for 1 second
        const { evolutionData: data1, analysis: analysis1 } = await cea.accelerateEvolution(realTimeSeconds);
        const { evolutionData: data2, analysis: analysis2 } = await cea.accelerateEvolution(realTimeSeconds);
        
        expect(data1).toEqual(data2); // Should produce the same evolution data
        expect(analysis1).toEqual(analysis2); // Should produce the same analysis
    });
});
