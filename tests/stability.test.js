// tests/stability.test.js

const StabilityManager = require('../src/tokens/stability');
const AstroNeuralEconomicAmplifier = require('../src/tokens/anea'); // Assuming ANEA is in this file
const OmniTemporalEconomicHarmonizer = require('../src/tokens/oteh'); // Import OTEH

jest.mock('../src/tokens/anea'); // Mock the ANEA class
jest.mock('../src/tokens/oteh'); // Mock the OTEH class

describe('StabilityManager', () => {
    let stabilityManager;
    let aneaMock;
    let otehMock;

    beforeEach(() => {
        stabilityManager = new StabilityManager();
        aneaMock = new AstroNeuralEconomicAmplifier();
        otehMock = new OmniTemporalEconomicHarmonizer();
        stabilityManager.anea = aneaMock; // Use the mocked ANEA
        stabilityManager.oteh = otehMock; // Use the mocked OTEH
    });

    test('should stabilize GTC when price is above target', async () => {
        const currentPriceGTC = 315000; // Above target
        await stabilityManager.stabilize(currentPriceGTC);
        
        expect(aneaMock.amplifyLiquidity).toHaveBeenCalled(); // Check if ANEA was called
        expect(stabilityManager.liquidityPool.usd).toBeLessThan(parseFloat(process.env.INITIAL_USD)); // USD should decrease
        expect(otehMock.synchronizeEconomicValues).toHaveBeenCalledWith('present', { GTC: currentPriceGTC, GU: stabilityManager.targetValueGU, priceIndex: 1.0 });
    });

    test('should stabilize GTC when price is below target', async () => {
        const currentPriceGTC = 313000; // Below target
        await stabilityManager.stabilize(currentPriceGTC);
        
        expect(aneaMock.amplifyLiquidity).toHaveBeenCalled(); // Check if ANEA was called
        expect(stabilityManager.liquidityPool.gtc).toBeGreaterThan(parseFloat(process.env.INITIAL_GTC)); // GTC should increase
        expect(otehMock.synchronizeEconomicValues).toHaveBeenCalledWith('present', { GTC: currentPriceGTC, GU: stabilityManager.targetValueGU, priceIndex: 1.0 });
    });

    test('should not adjust liquidity if no adjustment is needed', async () => {
        const currentPriceGTC = stabilityManager.targetValueGTC; // At target
        await stabilityManager.stabilize(currentPriceGTC);
        
        expect(aneaMock.amplifyLiquidity).toHaveBeenCalled(); // Check if ANEA was called
        expect(stabilityManager.liquidityPool.gtc).toBe(parseFloat(process.env.INITIAL_GTC)); // GTC should remain the same
        expect(stabilityManager.liquidityPool.usd).toBe(parseFloat(process.env.INITIAL_USD)); // USD should remain the same
        expect(otehMock.synchronizeEconomicValues).toHaveBeenCalledWith('present', { GTC: currentPriceGTC, GU: stabilityManager.targetValueGU, priceIndex: 1.0 });
    });

    test('should log error when insufficient USD after adjustment', async () => {
        stabilityManager.liquidityPool.usd = 0; // Set USD to 0 to trigger error
        const currentPriceGTC = 315000; // Above target
        await stabilityManager.stabilize(currentPriceGTC);
        
        expect(stabilityManager.logger.error).toHaveBeenCalledWith(expect.stringContaining("Insufficient USD in liquidity pool after adjustment."));
    });

    test('should check current liquidity', async () => {
        const liquidity = await stabilityManager.checkLiquidity();
        expect(liquidity).toEqual({
            gtc: parseFloat(process.env.INITIAL_GTC) || 1000000,
            usd: parseFloat(process.env.INITIAL_USD) || 314159000000
        });
    });

    test('should reset liquidity to initial values', async () => {
        await stabilityManager.resetLiquidity();
        expect(stabilityManager.liquidityPool.gtc).toBe(parseFloat(process.env.INITIAL_GTC) || 1000000);
        expect(stabilityManager.liquidityPool.usd).toBe(parseFloat(process.env.INITIAL_USD) || 314159000000);
    });

    test('should synchronize economic values with OTEH during stabilization', async () => {
        const currentPriceGTC = 315000; // Above target
        await stabilityManager.stabilize(currentPriceGTC);
        
        expect(otehMock.synchronizeEconomicValues).toHaveBeenCalled(); // Check if OTEH was called
    });

    test('should perform cross-temporal transaction using OTEH', async () => {
        const currentPriceGTC = 315000; // Above target
        await stabilityManager.stabilize(currentPriceGTC);
        
        await expect(otehMock.performCrossTemporalTransaction).toHaveBeenCalled(); // Check if cross-temporal transaction was called
    });
});
