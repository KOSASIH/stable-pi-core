// tests/marketDataFetcher.test.js

const MarketDataFetcher = require('../api/marketDataFetcher'); // Adjust the path as necessary

describe('MarketDataFetcher', () => {
    let marketDataFetcher;

    beforeAll(() => {
        marketDataFetcher = new MarketDataFetcher('https://api.example.com'); // Replace with your actual API URL
    });

    test('fetchMarketData should return market data', async () => {
        const data = await marketDataFetcher.fetchMarketData();
        expect(data).toBeDefined();
        expect(Array.isArray(data)).toBe(true); // Assuming the data is an array
    });

    test('getMarketItemById should return a specific market item', async () => {
        const itemId = '12345'; // Replace with a valid item ID
        const item = await marketDataFetcher.getMarketItemById(itemId);
        expect(item).toBeDefined();
        expect(item.id).toBe(itemId);
    });

    test('fetchMarketData should throw an error for invalid URL', async () => {
        marketDataFetcher.apiUrl = 'https://invalid-url.com';
        await expect(marketDataFetcher.fetchMarketData()).rejects.toThrow();
    });
});
