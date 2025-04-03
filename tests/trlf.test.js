const trlf = require('../src/core/trlf');

describe('Trans-Reality Liquidity Fabric', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        trlf.liquidityPools.clear(); // Clear liquidity pools before each test
        trlf.clearTransactionHistory(); // Clear transaction history before each test
    });

    test('should initialize liquidity pool for a reality', () => {
        trlf.initializeLiquidityPool('Reality1');
        expect(trlf.liquidityPools.has('Reality1')).toBe(true);
    });

    test('should add liquidity to a reality', () => {
        trlf.initializeLiquidityPool('Reality1');
        trlf.addLiquidity('Reality1', 100, 200);
        
        const pool = trlf.getLiquidityStatus('Reality1');
        expect(pool.GTC).toBe(100);
        expect(pool.GU).toBe(200);
    });

    test('should throw error when adding liquidity to a non-existent pool', () => {
        expect(() => trlf.addLiquidity('NonExistentReality', 100, 200)).toThrow("Liquidity pool for reality NonExistentReality does not exist.");
    });

    test('should transfer liquidity between realities', async () => {
        trlf.initializeLiquidityPool('Reality1');
        trlf.initializeLiquidityPool('Reality2');
        trlf.addLiquidity('Reality1', 100, 200);
        
        await trlf.transferLiquidity('Reality1', 'Reality2', 50, 100);
        
        const fromPool = trlf.getLiquidityStatus('Reality1');
        const toPool = trlf.getLiquidityStatus('Reality2');
        
        expect(fromPool.GTC).toBe(50);
        expect(fromPool.GU).toBe(100);
        expect(toPool.GTC).toBe(50);
        expect(toPool.GU).toBe(100);
    });

    test('should throw error when transferring from a non-existent pool', async () => {
        await expect(trlf.transferLiquidity('NonExistentReality', 'Reality2', 50, 100)).rejects.toThrow("One or both liquidity pools do not exist.");
    });

    test('should throw error when insufficient liquidity', async () => {
        trlf.initializeLiquidityPool('Reality1');
        trlf.addLiquidity('Reality1', 50, 100);
        
        await expect(trlf.transferLiquidity('Reality1', 'Reality2', 100, 200)).rejects.toThrow("Insufficient liquidity in the source pool.");
    });

    test('should get liquidity status of a reality', () => {
        trlf.initializeLiquidityPool('Reality1');
        trlf.addLiquidity('Reality1', 100, 200);
        
        const status = trlf.getLiquidityStatus('Reality1');
        expect(status).toEqual({ GTC: 100, GU: 200 });
    });

    test('should throw error when getting status of a non-existent pool', () => {
        expect(() => trlf.getLiquidityStatus('NonExistentReality')).toThrow("Liquidity pool for reality NonExistentReality does not exist.");
    });

    test('should log transactions correctly', async () => {
        trlf.initializeLiquidityPool('Reality1');
        trlf.initializeLiquidityPool('Reality2');
        trlf.addLiquidity('Reality1', 100, 200);
        
        await trlf.transferLiquidity('Reality1', 'Reality2', 50, 100);
        
        const history = trlf.getTransactionHistory();
        expect(history.length).toBe(2); // One transfer out and one transfer in
        expect(history[0]).toMatchObject({
            realityId: 'Reality1',
            type: 'TRANSFER_OUT',
            amountGTC: 50,
            amountGU: 100,
            relatedRealityId: 'Reality2'
        });
        expect(history[1]).toMatchObject({
            realityId: 'Reality2',
            type: 'TRANSFER_IN',
            amountGTC: 50,
            amountGU: 100,
            relatedRealityId: 'Reality1'
        });
    });

    test('should clear transaction history', async () => {
        trlf.initializeLiquidityPool('Reality1');
        trlf.addLiquidity('Reality1', 100, 200);
        
        await trlf.transferLiquidity('Reality1', 'Reality2', 50, 100);
        
        expect(trlf.getTransactionHistory().length).toBe(2); // Two transactions logged
        trlf.clearTransactionHistory();
        expect(trlf.getTransactionHistory().length).toBe(0); // History should be cleared
    });
});
