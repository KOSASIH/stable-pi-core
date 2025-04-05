// tests/tcrb.test.js
const TransCosmicRealityBridge = require('./tcrb');

describe('TransCosmicRealityBridge Tests', () => {
  beforeEach(() => {
    // Reset the instance before each test
    TransCosmicRealityBridge.transactionLog = [];
    TransCosmicRealityBridge.exchangeRates = {
      CNC: 1,
      GTC: 0.01,
      GU: 0.001,
    };
  });

  test('should set exchange rate for a currency', () => {
    TransCosmicRealityBridge.setExchangeRate('GTC', 0.02);
    expect(TransCosmicRealityBridge.getExchangeRate('GTC')).toBe(0.02);
  });

  test('should throw error for invalid exchange rate', () => {
    expect(() => TransCosmicRealityBridge.setExchangeRate('GTC', 0)).toThrow('Exchange rate must be greater than zero.');
  });

  test('should transfer currency to a parallel universe', async () => {
    await TransCosmicRealityBridge.transferToParallelUniverse(1000, 'CNC', 'Parallel Universe Alpha');
    const log = TransCosmicRealityBridge.getTransactionLog();
    expect(log.length).toBe(1);
    expect(log[0]).toEqual({
      amount: 1000,
      currency: 'CNC',
      targetUniverse: 'Parallel Universe Alpha',
      timestamp: expect.any(String),
    });
  });

  test('should convert currency correctly during transfer', async () => {
    await TransCosmicRealityBridge.transferToParallelUniverse(1000, 'GTC', 'Parallel Universe Beta');
    const log = TransCosmicRealityBridge.getTransactionLog();
    expect(log.length).toBe(1);
    expect(log[0].amount).toBe(1000);
    expect(log[0].currency).toBe('GTC');
    expect(log[0].targetUniverse).toBe('Parallel Universe Beta');
  });

  test('should throw error for unsupported currency', async () => {
    await expect(TransCosmicRealityBridge.transferToParallelUniverse(1000, 'XYZ', 'Parallel Universe Gamma')).rejects.toThrow('Currency XYZ is not supported for transfer.');
  });

  test('should throw error for zero or negative transfer amount', async () => {
    await expect(TransCosmicRealityBridge.transferToParallelUniverse(0, 'CNC', 'Parallel Universe Delta')).rejects.toThrow('Transfer amount must be greater than zero.');
    await expect(TransCosmicRealityBridge.transferToParallelUniverse(-100, 'CNC', 'Parallel Universe Delta')).rejects.toThrow('Transfer amount must be greater than zero.');
  });

  test('should log multiple transactions correctly', async () => {
    await TransCosmicRealityBridge.transferToParallelUniverse(1000, 'CNC', 'Parallel Universe Alpha');
    await TransCosmicRealityBridge.transferToParallelUniverse(500, 'GTC', 'Parallel Universe Beta');
    await TransCosmicRealityBridge.transferToParallelUniverse(200, 'GU', 'Parallel Universe Gamma');

    const log = TransCosmicRealityBridge.getTransactionLog();
    expect(log.length).toBe(3);
    expect(log[0].currency).toBe('CNC');
    expect(log[1].currency).toBe('GTC');
    expect(log[2].currency).toBe('GU');
  });
});
