// tests/stability.test.js

import StabilityManager from '../src/core/stability';
import GravitationalWaveMarketPredictor from '../src/core/gwmp';

jest.mock('../src/core/gwmp'); // Mock the Gravitational Wave Market Predictor module

describe('StabilityManager', () => {
    let stabilityManager;

    beforeEach(() => {
        stabilityManager = new StabilityManager();
    });

    test('should initialize with correct default values', () => {
        expect(stabilityManager.targetValueGTC).toBe(314159);
        expect(stabilityManager.targetValueGU).toBe(1);
        expect(stabilityManager.liquidityPool).toEqual({ gtc: 1000000, gu: 1000000 });
        expect(stabilityManager.marketPredictions).toEqual([]);
    });

    test('should stabilize and adjust liquidity based on market predictions', async () => {
        GravitationalWaveMarketPredictor.analyzeData.mockReturnValue("Increase in demand for GTC/GU expected.");
        
        await stabilityManager.stabilize();
        
        expect(stabilityManager.liquidityPool.gtc).toBe(1001000); // Liquidity should increase
        expect(stabilityManager.marketPredictions).toHaveLength(1);
    });

    test('should decrease liquidity if demand is stable or decreasing', async () => {
        GravitationalWaveMarketPredictor.analyzeData.mockReturnValue("Stable or decreasing demand for GTC/GU expected.");
        
        await stabilityManager.stabilize();
        
        expect(stabilityManager.liquidityPool.gtc).toBe(999000); // Liquidity should decrease
        expect(stabilityManager.marketPredictions).toHaveLength(1);
    });

    test('should throw error if stabilize is called without gravitational data', async () => {
        GravitationalWaveMarketPredictor.analyzeData.mockImplementation(() => {
            throw new Error("No gravitational data available for analysis.");
        });

        await expect(stabilityManager.stabilize()).rejects.toThrow("No gravitational data available for analysis.");
    });

    test('should get current liquidity status', () => {
        const liquidityStatus = stabilityManager.getLiquidityStatus();
        expect(liquidityStatus).toEqual({ gtc: 1000000, gu: 1000000 });
    });

    test('should get market predictions', () => {
        stabilityManager.marketPredictions.push({ prediction: "Increase in demand", timestamp: Date.now() });
        const predictions = stabilityManager.getMarketPredictions();
        expect(predictions).toHaveLength(1);
    });

    test('should reset liquidity pool to initial values', () => {
        stabilityManager.liquidityPool.gtc = 500000; // Change liquidity
        stabilityManager.resetLiquidity();
        expect(stabilityManager.liquidityPool).toEqual({ gtc: 1000000, gu: 1000000 });
    });

    test('should simulate market fluctuation', () => {
        const initialTargetValue = stabilityManager.targetValueGTC;
        stabilityManager.simulateMarketFluctuation();
        expect(stabilityManager.targetValueGTC).not.toBe(initialTargetValue); // Target value should change
    });

    test('should generate a state hash', () => {
        const stateHash = stabilityManager.generateStateHash();
        expect(stateHash).toBeDefined(); // Ensure a hash is generated
    });

    test('should throw error when adding invalid gravitational data', () => {
        expect(() => stabilityManager.addGravitationalData(null)).toThrow("Invalid gravitational data.");
    });
});
