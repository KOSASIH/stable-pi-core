// tests//oteh.test.js

import OmniTemporalEconomicHarmonizer from './oteh';

describe('OmniTemporalEconomicHarmonizer', () => {
    let oteh;

    beforeEach(() => {
        oteh = new OmniTemporalEconomicHarmonizer();
    });

    test('should synchronize economic values for different time points', () => {
        const pastValues = { GTC: 100, GU: 200, priceIndex: 1.0 };
        oteh.synchronizeEconomicValues('past', pastValues);
        expect(oteh.economicValues.past).toEqual(pastValues);
    });

    test('should harmonize economic values across time points', () => {
        oteh.synchronizeEconomicValues('past', { GTC: 100, GU: 200, priceIndex: 1.0 });
        oteh.synchronizeEconomicValues('present', { GTC: 150, GU: 250, priceIndex: 1.5 });
        oteh.synchronizeEconomicValues('future', { GTC: 200, GU: 300, priceIndex: 2.0 });
        
        console.log = jest.fn(); // Mock console.log
        oteh.harmonizeValues();
        expect(console.log).toHaveBeenCalledWith(expect.stringContaining("Harmonized economic value across time:"));
    });

    test('should perform a cross-temporal transaction', async () => {
        oteh.synchronizeEconomicValues('past', { GTC: 100, GU: 200, priceIndex: 1.0 });
        oteh.synchronizeEconomicValues('present', { GTC: 150, GU: 250, priceIndex: 1.5 });
        
        const adjustedAmount = await oteh.performCrossTemporalTransaction('past', 'present', 50);
        expect(adjustedAmount).toBeCloseTo(75); // Adjusted amount based on inflation
    });

    test('should throw an error for invalid time points in transaction', async () => {
        await expect(oteh.performCrossTemporalTransaction('past', 'future', 50)).rejects.toThrow("Invalid time points for transaction.");
    });

    test('should simulate future economic conditions', () => {
        oteh.synchronizeEconomicValues('present', { GTC: 150, GU: 250, priceIndex: 1.5 });
        oteh.simulateFutureEconomicConditions('present', 0.05, 5); // 5% growth over 5 years
        
        const expectedFutureValues = {
            GTC: 150 * Math.pow(1 + 0.05, 5),
            GU: 250 * Math.pow(1 + 0.05, 5),
            priceIndex: 1.5 * Math.pow(1 + 0.05, 5)
        };
        
        expect(oteh.economicValues['simulated_present']).toEqual(expectedFutureValues);
    });

    test('should throw an error if simulating future conditions for non-existent time point', () => {
        expect(() => {
            oteh.simulateFutureEconomicConditions('non-existent', 0.05, 5);
        }).toThrow("No economic values found for time point: non-existent");
    });
});
