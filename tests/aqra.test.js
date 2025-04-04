// tests/aqra.test.js

import AethericQuantumResonanceAmplifier from '../../src/quantum/aqra';

describe('AethericQuantumResonanceAmplifier', () => {
    let aqra;

    beforeEach(() => {
        aqra = new AethericQuantumResonanceAmplifier();
        aqra.initialize(2); // Set amplification factor for testing
    });

    test('should initialize with a specific amplification factor', () => {
        expect(aqra.amplificationFactor).toBe(2);
    });

    test('should amplify a signal correctly', () => {
        const signal = { strength: 10, energy: 5 };
        const amplifiedSignal = aqra.amplifySignal(signal);
        
        expect(amplifiedSignal.strength).toBe(20); // 10 * 2
        expect(amplifiedSignal.energy).toBe(10); // 5 * 2
        expect(amplifiedSignal).toHaveProperty('timestamp'); // Check for timestamp
    });

    test('should throw an error for invalid signal format', () => {
        expect(() => {
            aqra.amplifySignal({}); // Invalid signal
        }).toThrow('Invalid signal format. Signal must contain numeric strength and energy.');
    });

    test('should process a transaction with amplified signal', () => {
        const transaction = { signalStrength: 10, energy: 5 };
        const result = aqra.processTransaction(transaction);
        
        expect(result.status).toBe('success');
        expect(result).toHaveProperty('transactionId');
    });

    test('should throw an error for invalid transaction format', () => {
        expect(() => {
            aqra.processTransaction({}); // Invalid transaction
        }).toThrow('Invalid transaction format. Transaction must contain numeric signalStrength and energy.');
    });

    test('should retrieve the history of amplified signals', () => {
        const signal1 = { strength: 10, energy: 5 };
        const signal2 = { strength: 20, energy: 10 };
        
        aqra.amplifySignal(signal1);
        aqra.amplifySignal(signal2);
        
        const history = aqra.getSignalHistory();
        expect(history).toHaveLength(2);
        expect(history[0]).toHaveProperty('strength', 20); // First signal amplified
        expect(history[1]).toHaveProperty('strength', 40); // Second signal amplified
    });

    test('should set a new amplification factor', () => {
        aqra.setAmplificationFactor(3);
        expect(aqra.amplificationFactor).toBe(3);
    });

    test('should throw an error when setting an invalid amplification factor', () => {
        expect(() => {
            aqra.setAmplificationFactor(0); // Invalid factor
        }).toThrow('Amplification factor must be greater than zero.');
    });
});
