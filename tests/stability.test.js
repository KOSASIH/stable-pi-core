const StabilityManager = require('../src/tokens/stability');
const AstroNeuralEconomicAmplifier = require('../src/tokens/anea'); // Assuming ANEA is in this file
const OmniTemporalEconomicHarmonizer = require('../src/tokens/oteh'); // Import OTEH
const TransUniversalResonanceLattice = require('../src/core/turl'); // Import TURL

jest.mock('../src/tokens/anea'); // Mock the ANEA class
jest.mock('../src/tokens/oteh'); // Mock the OTEH class
jest.mock('../src/core/turl'); // Mock the TURL class

describe('StabilityManager', () => {
    let stabilityManager;
    let aneaMock;
    let otehMock;
    let turlMock;

    beforeEach(() => {
        stabilityManager = new StabilityManager();
        aneaMock = new AstroNeuralEconomicAmplifier();
        otehMock = new OmniTemporalEconomicHarmonizer();
        turlMock = new TransUniversalResonanceLattice();
        stabilityManager.anea = aneaMock; // Use the mocked ANEA
        stabilityManager.oteh = otehMock; // Use the mocked OTEH
        stabilityManager.turl = turlMock; // Use the mocked TURL
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
        
        expect(otehMock.performCrossTemporalTransaction).toHaveBeenCalled(); // Check if cross-temporal transaction was called
    });

    test('should synchronize transactions across universes using TURL', async () => {
        const transaction = {
            id: 'tx-001',
            fromUniverse: 'MainReality',
            toUniverse: 'ParallelReality1',
            amount: 1000
        };

        await stabilityManager.synchronizeTransaction(transaction);
        expect(turlMock.synchronizeTransaction).toHaveBeenCalledWith(transaction); // Check if TURL was called with the transaction
    });

    test('should get resonance field status from TURL', async () => {
        const universe = 'ParallelReality1';
        const mockStatus = { universe, liquidity: 5000, transactions: [] };
        turlMock.getResonanceFieldStatus.mockReturnValue(mockStatus); // Mock return value

        const status = stabilityManager.getResonanceFieldStatus(universe);
        expect(status).toEqual(mockStatus); // Check if the status matches the mock
        expect(turlMock.getResonanceFieldStatus).toHaveBeenCalledWith(universe); });

    test('should log error when retrieving resonance field status fails', async () => {
        const universe = 'ParallelReality1';
        turlMock.getResonanceFieldStatus.mockImplementation(() => {
            throw new Error("Failed to retrieve status");
        });

        const status = stabilityManager.getResonanceFieldStatus(universe);
        expect(status).toBeUndefined(); // Status should be undefined due to error
        expect(stabilityManager.logger.error).toHaveBeenCalledWith(expect.stringContaining("Error retrieving resonance field status: Failed to retrieve status"));
    });
});
