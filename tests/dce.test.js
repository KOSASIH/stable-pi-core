// tests/dce.test.js

import DimensionalCompressionEngine from '../src/core/dce';

describe('DimensionalCompressionEngine', () => {
    let dce;

    beforeEach(() => {
        dce = new DimensionalCompressionEngine();
    });

    test('should compress data and store it', () => {
        const key = 'data1';
        const data = { value: 42 };
        dce.compressData(key, data);
        const storedData = dce.retrieveData(key);
        expect(storedData).toHaveProperty('original', data);
        expect(storedData).toHaveProperty('compressed');
        expect(storedData).toHaveProperty('dimensions', 4);
    });

    test('should throw an error when compressing data with an existing key', () => {
        const key = 'data1';
        const data = { value: 42 };
        dce.compressData(key, data);
        expect(() => dce.compressData(key, { value: 100 })).toThrow(`Data with key ${key} already exists. Use a different key.`);
    });

    test('should retrieve compressed data', () => {
        const key = 'data1';
        const data = { value: 42 };
        dce.compressData(key, data);
        const retrievedData = dce.retrieveData(key);
        expect(retrievedData).toHaveProperty('original', data);
    });

    test('should throw an error when retrieving data with a non-existent key', () => {
        expect(() => dce.retrieveData('nonExistentKey')).toThrow('No data found for key: nonExistentKey');
    });

    test('should entangle data for instant access', () => {
        const key = 'data1';
        const data = { value: 42 };
        dce.compressData(key, data);
        const reference = 'entangledReference';
        dce.entangleData(key, reference);
        expect(dce.entangledData.get(key)).toBe(reference);
    });

    test('should throw an error when entangling data with a non-existent key', () => {
        expect(() => dce.entangleData('nonExistentKey', 'reference')).toThrow('No data found for key: nonExistentKey');
    });

    test('should access entangled data', () => {
        const key = 'data1';
        const data = { value: 42 };
        dce.compressData(key, data);
        const reference = 'entangledReference';
        dce.entangleData(key, reference);
        const accessedData = dce.accessEntangledData(key);
        expect(accessedData).toBe(reference);
    });

    test('should throw an error when accessing entangled data with a non-existent key', () => {
        expect(() => dce.accessEntangledData('nonExistentKey')).toThrow('No entangled data found for key: nonExistentKey');
    });

    test('should reset the DCE storage', () => {
        const key = 'data1';
        const data = { value: 42 };
        dce.compressData(key, data);
        dce.resetStorage();
        expect(() => dce.retrieveData(key)).toThrow('No data found for key: data1');
        expect(dce.entangledData.size).toBe(0);
    });

    test('should list all stored keys', () => {
        dce.compressData('data1', { value: 42 });
        dce.compressData('data2', { value: 100 });
        const keys = dce.listStoredKeys();
        expect(keys).toEqual(expect.arrayContaining(['data1', 'data2']));
    });

    test('should return the correct storage size', () => {
        expect(dce.getStorageSize()).toBe(0);
        dce.compressData('data1', { value: 42 });
        expect(dce.getStorageSize()).toBe(1);
        dce.compressData('data2', { value: 100 });
        expect(dce.getStorageSize()).toBe(2);
    });
});
