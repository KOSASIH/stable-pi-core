const ogrs = require('../src/space/ogrs');

describe('Omni-Galactic Resource Symbiote', () => {
    beforeEach(() => {
        // Reset resources before each test
        ogrs.ocsi.resetResources();
    });

    test('should harvest resources correctly', () => {
        ogrs.ocsi.harvestResources(5, 3, 2);
        const resources = ogrs.getCurrentResources();
        expect(resources).toEqual({ stars: 5, planets: 3, nebulae: 2 });
    });

    test('should convert harvested resources to energy, data, and liquidity', () => {
        ogrs.ocsi.harvestResources(2, 1, 1);
        const converted = ogrs.qct.convertResources(ogrs.getCurrentResources());
        
        expect(converted.energy).toBe(2000); // 2 stars * 1000 energy
        expect(converted.data).toBe(500);     // 1 planet * 500 data
        expect(converted.liquidity).toBe(2000); // 1 nebula * 2000 liquidity
    });

    test('should dynamically convert harvested resources', () => {
        ogrs.ocsi.harvestResources(3, 2, 1);
        const converted = ogrs.qct.dynamicConversion(ogrs.getCurrentResources());
        
        expect(converted.energy).toBeGreaterThan(0); // Should be a positive value
        expect(converted.data).toBeGreaterThan(0);   // Should be a positive value
        expect(converted.liquidity).toBeGreaterThan(0); // Should be a positive value
    });

    test('should predict future conversion based on current resources', () => {
        ogrs.ocsi.harvestResources(4, 2, 3);
        const predicted = ogrs.predictFutureConversion();
        
        expect(predicted.predictedEnergy).toBe(4400); // 4 stars * 1000 energy * 1.1
        expect(predicted.predictedData).toBe(1100);   // 2 planets * 500 data * 1.1
        expect(predicted.predictedLiquidity).toBe(6600); // 3 nebulae * 2000 liquidity * 1.1
    });

    test('should return current resources', () => {
        ogrs.ocsi.harvestResources(4, 2, 3);
        const resources = ogrs.getCurrentResources();
        expect(resources).toEqual({ stars: 4, planets: 2, nebulae: 3 });
    });

    test('should return resource history', () => {
        ogrs.ocsi.harvestResources(1, 1, 1);
        const history = ogrs.getResourceHistory();
        expect(history.length).toBe(1);
        expect(history[0]).toHaveProperty('stars', 1);
        expect(history[0]).toHaveProperty('planets', 1);
        expect(history[0]).toHaveProperty('nebulae', 1);
    });

    test('should reset resources correctly', () => {
        ogrs.ocsi.harvestResources(5, 3, 2);
        ogrs.resetResources();
        const resources = ogrs.getCurrentResources();
        expect(resources).toEqual({ stars: 0, planets: 0, nebulae: 0 });
    });
});
