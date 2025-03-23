// tests/anea.test.js

import AstroNeuralEconomicAmplifier from '../src/tokens/anea';

describe('AstroNeuralEconomicAmplifier', () => {
    let anea;

    beforeEach(() => {
        anea = new AstroNeuralEconomicAmplifier();
    });

    test('should initialize with empty liquidity pool', () => {
        expect(anea.getLiquidityPool()).toEqual([]);
    });

    test('should update bio-quantum signals', () => {
        const signals = [
            { amplitude: 1.0, frequency: 10.0 },
            { amplitude: 2.0, frequency: 20.0 },
        ];
        anea.bioQuantumIntegrationLayer.updateSignals(signals);
        expect(anea.bioQuantumIntegrationLayer.getSignals()).toEqual(signals);
    });

    test('should update gravitational wave predictions', () => {
        const predictions = [0.5, 0.8];
        anea.gravitationalWaveMarketPredictor.updatePredictions(predictions);
        expect(anea.gravitationalWaveMarketPredictor.getPredictions()).toEqual(predictions);
    });

    test('should integrate signals and predictions correctly', () => {
        const signals = [
            { amplitude: 1.0, frequency: 10.0 },
            { amplitude: 2.0, frequency: 20.0 },
        ];
        const predictions = [0.5, 0.8];
        
        anea.bioQuantumIntegrationLayer.updateSignals(signals);
        anea.gravitationalWaveMarketPredictor.updatePredictions(predictions);
        
        const integratedSignals = anea.integrateSignals();
        expect(integratedSignals).toEqual([
            { amplitude: 1.0, frequency: 10.0, prediction: 0.5 },
            { amplitude: 2.0, frequency: 20.0, prediction: 0.8 },
        ]);
    });

    test('should amplify liquidity based on integrated signals', () => {
        const signals = [
            { amplitude: 1.0, frequency: 10.0 },
            { amplitude: 2.0, frequency: 20.0 },
        ];
        const predictions = [0.5, 0.8];
        
        anea.bioQuantumIntegrationLayer.updateSignals(signals);
        anea.gravitationalWaveMarketPredictor.updatePredictions(predictions);
        
        const totalAmplifiedLiquidity = anea.amplifyLiquidity();
        expect(totalAmplifiedLiquidity).toBeCloseTo(1.0 * 0.5 + 2.0 * 0.8); // 1.0 * 0.5 + 2.0 * 0.8 = 2.1
        expect(anea.getLiquidityPool()).toHaveLength(2); // Should have two entries in the liquidity pool
    });

    test('should return the current liquidity pool', () => {
        const signals = [
            { amplitude: 1.0, frequency: 10.0 },
            { amplitude: 2.0, frequency: 20.0 },
        ];
        const predictions = [0.5, 0.8];
        
        anea.bioQuantumIntegrationLayer.updateSignals(signals);
        anea.gravitationalWaveMarketPredictor.updatePredictions(predictions);
        anea.amplifyLiquidity(); // Populate the liquidity pool
        
        const liquidityPool = anea.getLiquidityPool();
        expect(liquidityPool).toHaveLength(2); // Should have two entries
    });
});
