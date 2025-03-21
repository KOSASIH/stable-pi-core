// tests/dataUtils.test.js

import { fetchRealTimeData, processData, validateDataStructure } from '../src/core/dataUtils';
import axios from 'axios';

jest.mock('axios');

describe('Data Utils', () => {
    describe('fetchRealTimeData', () => {
        test('should fetch economic data successfully', async () => {
            const mockData = { value: 100 };
            axios.get.mockResolvedValue({ data: mockData });

            const data = await fetchRealTimeData('economic');
            expect(data).toEqual(mockData);
            expect(axios.get).toHaveBeenCalledWith('https://api.example.com/economic-data');
        });

        test('should fetch cosmic data successfully', async () => {
            const mockData = { value: 200 };
            axios.get.mockResolvedValue({ data: mockData });

            const data = await fetchRealTimeData('cosmic');
            expect(data).toEqual(mockData);
            expect(axios.get).toHaveBeenCalledWith('https://api.example.com/cosmic-data');
        });

        test('should fetch network data successfully', async () => {
            const mockData = { value: 300 };
            axios.get.mockResolvedValue({ data: mockData });

            const data = await fetchRealTimeData('network');
            expect(data).toEqual(mockData);
            expect(axios.get).toHaveBeenCalledWith('https://api.example.com/network-data');
        });

        test('should throw an error for invalid data type', async () => {
            await expect(fetchRealTimeData('invalid')).rejects.toThrow('Invalid data type requested.');
        });

        test('should handle errors during data fetching', async () => {
            axios.get.mockRejectedValue(new Error('Network Error'));
            await expect(fetchRealTimeData('economic')).rejects.toThrow('Failed to fetch economic data.');
        });
    });

    describe('processData', () => {
        test('should process valid data correctly', () => {
            const rawData = { value: 100 };
            const processedData = processData(rawData);
            expect(processedData).toEqual({ value: expect.any(Number) }); // Check that value is normalized
        });

        test('should throw an error for invalid data', () => {
            expect(() => processData(null)).toThrow('Invalid data provided for processing.');
            expect(() => processData('string')).toThrow('Invalid data provided for processing.');
        });
    });

    describe('validateDataStructure', () => {
        test('should return true for valid data structure', () => {
            const validData = { value: 100 };
            expect(validateDataStructure(validData)).toBe(true);
        });

        test('should return false for invalid data structure', () => {
            const invalidData = { notValue: 100 };
            expect(validateDataStructure(invalidData)).toBe(false);
        });

        test('should return false for non-object data', () => {
            expect(validateDataStructure(null)).toBe(false);
            expect(validateDataStructure(123)).toBe(false);
            expect(validateDataStructure('string')).toBe(false);
        });
    });
});
