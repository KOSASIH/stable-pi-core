// tests/stabilityManager.test.js

import StabilityManager from '../src/core/stability';
import HyperResonantStabilityMatrix from '../src/core/hrsm'; // Import HRSM for mocking

jest.mock('../src/core/hrsm'); // Mock the HRSM module

describe('StabilityManager', () => {
    let stabilityManager;

    beforeEach(() => {
        stabilityManager = new StabilityManager();
        HyperResonantStabilityMatrix.mockClear(); // Clear previous calls to the mock
    });

    test('should initialize with correct default values', () => {
        expect(stabilityManager.targetValueGTC).toBe(314159);
        expect(stabilityManager.targetValueGU).toBe(1);
        expect(stabilityManager.liquidityPool).toEqual({ gtc: 1000000, gu: 1000000 });
        expect(stabilityManager.marketPredictions).toEqual([]);
    });

    test('should adjust liquidity when demand increases', async () => {
        // Mock the market prediction
        jest.spyOn(stabilityManager, 'getCosmicConditions').mockReturnValue({
            nearBlackHole: false,
            supernovaNearby: false,
            dimensionsShift: false,
        });

        // Mock the HRSM to return a stable matrix
        HyperResonantStabilityMatrix.prototype.calculateStability = jest.fn();
        HyperResonantStabilityMatrix.prototype.getStabilityMatrix.mockReturnValue([[100]]); // Stable condition

        // Mock the market predictor
        jest.spyOn(GravitationalWaveMarketPredictor, 'analyzeData').mockReturnValue("Increase in demand");

        await stabilityManager.stabilize();

        expect(stabilityManager.liquidityPool.gtc).toBe(1001000); // Should increase by 1000
    });

    test('should adjust liquidity when demand is stable or decreasing', async () => {
        // Mock the market prediction
        jest.spyOn(stabilityManager, 'getCosmicConditions').mockReturnValue({
            nearBlackHole: false,
            supernovaNearby: false,
            dimensionsShift: false,
        });

        // Mock the HRSM to return a stable matrix
        HyperResonantStabilityMatrix.prototype.calculateStability = jest.fn();
        HyperResonantStabilityMatrix.prototype.getStabilityMatrix.mockReturnValue([[100]]); // Stable condition

        // Mock the market predictor
        jest.spyOn(GravitationalWaveMarketPredictor, 'analyzeData').mockReturnValue("Stable demand");

        await stabilityManager.stabilize();

        expect(stabilityManager.liquidityPool.gtc).toBe(999000); // Should decrease by 1000
    });

    test('should reset liquidity pool to initial values', () => {
        stabilityManager.liquidityPool.gtc = 500000; // Change liquidity for testing
        stabilityManager.resetLiquidity();
        expect(stabilityManager.liquidityPool).toEqual({ gtc: 1000000, gu: 1000000 });
    });

    test('should simulate market fluctuation', () => {
        const initialTargetValueGTC = stabilityManager.targetValueGTC;
        stabilityManager.simulateMarketFluctuation();
        expect(stabilityManager.targetValueGTC).not.toBe(initialTargetValueGTC); // Should change
    });

    test('should generate a quantum hash for the current state', () => {
        const hash = stabilityManager.generateStateHash();
        expect(hash).toBeDefined(); // Ensure a hash is generated
    });
});
