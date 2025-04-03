const aqsc = require('../src/core/aqsc'); // Adjust the path as necessary

describe('Astro-Quantum Sentience Core', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('should add consciousness states', () => {
        aqsc.addConsciousnessState(1);
        aqsc.addConsciousnessState(2);
        aqsc.addConsciousnessState(3);
        
        expect(aqsc.qcc.consciousnessStates.length).toBe(3);
        expect(aqsc.qcc.consciousnessStates).toEqual([1, 2, 3]);
    });

    test('should reach consensus from consciousness states', () => {
        aqsc.addConsciousnessState(1);
        aqsc.addConsciousnessState(2);
        aqsc.addConsciousnessState(3);
        
        const consensus = aqsc.qcc.reachConsensus();
        expect(consensus).toBe(2); // (1 + 2 + 3) / 3 = 2
    });

    test('should return null if no consciousness states are present', () => {
        const consensus = aqsc.qcc.reachConsensus();
        expect(consensus).toBeNull();
    });

    test('should integrate biological data', () => {
        const data = { heartRate: 75, temperature: 36.5 };
        aqsc.integrateBiologicalData(data);
        
        expect(aqsc.bqil.biologicalData).toEqual(data);
    });

    test('should analyze biological data and make decisions', () => {
        aqsc.integrateBiologicalData({ heartRate: 105, temperature: 37.0 });
        
        const decision = aqsc.bqil.analyzeData();
        expect(decision).toBe("Decision: High Alert - Possible Stress");
    });

    test('should simulate cosmic waves and calculate average', () => {
        aqsc.cws.simulateWave();
        aqsc.cws.simulateWave();
        aqsc.cws.simulateWave();
        
        const average = aqsc.cws.getWaveAverage();
        expect(average).toBeGreaterThan(0); // Ensure average is a positive number
    });

    test('should return null if no cosmic waves are simulated', () => {
        const average = aqsc.cws.getWaveAverage();
        expect(average).toBeNull();
    });

    test('should clear consciousness states', () => {
        aqsc.addConsciousnessState(1);
        aqsc.clearConsciousnessStates();
        
        expect(aqsc.qcc.consciousnessStates.length).toBe(0);
    });

    test('should clear cosmic waves', () => {
        aqsc.cws.simulateWave();
        aqsc.clearCosmicWaves();
        
        expect(aqsc.cws.waves.length).toBe(0);
    });
});
