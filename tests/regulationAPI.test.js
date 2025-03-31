// tests/regulationAPI.test.js - Unit tests for Regulation API module

import RegulationAPI from '../src/space/regulationAPI';
import axios from 'axios';

jest.mock('axios'); // Mock axios for testing

describe('RegulationAPI', () => {
    let regulationAPI;
    const apiEndpoints = [
        'https://api.example.com/regulations',
        'https://api.anotherexample.com/regulations'
    ];

    beforeEach(() => {
        regulationAPI = new RegulationAPI(apiEndpoints);
    });

    test('should fetch regulations from multiple APIs', async () => {
        const mockResponse1 = { data: [{ id: 1, title: 'Regulation 1' }] };
        const mockResponse2 = { data: [{ id: 2, title: 'Regulation 2' }] };

        axios.get.mockImplementationOnce(() => Promise.resolve(mockResponse1));
        axios.get.mockImplementationOnce(() => Promise.resolve(mockResponse2));

        const regulations = await regulationAPI.fetchRegulations();
        expect(regulations).toEqual([
            { id: 1, title: 'Regulation 1' },
            { id: 2, title: 'Regulation 2' }
        ]);
        expect(axios.get).toHaveBeenCalledTimes(2);
        expect(axios.get).toHaveBeenCalledWith(apiEndpoints[0]);
        expect(axios.get).toHaveBeenCalledWith(apiEndpoints[1]);
    });

    test('should cache fetched regulations', async () => {
        const mockResponse = { data: [{ id: 1, title: 'Regulation 1' }] };
        axios.get.mockImplementationOnce(() => Promise.resolve(mockResponse));

        const regulationsFirstFetch = await regulationAPI.fetchRegulations();
        const regulationsSecondFetch = await regulationAPI.fetchRegulations();

        expect(regulationsFirstFetch).toEqual(regulationsSecondFetch);
        expect(axios.get).toHaveBeenCalledTimes(1); // Should only call once
    });

    test('should throw an error if fetching regulations fails', async () => {
        axios.get.mockImplementationOnce(() => Promise.reject(new Error('Network Error')));

        await expect(regulationAPI.fetchRegulations()).rejects.toThrow('Failed to fetch regulations');
    });

    test('should fetch regulations from cache if available', async () => {
        const mockResponse = { data: [{ id: 1, title: 'Regulation 1' }] };
        axios.get.mockImplementationOnce(() => Promise.resolve(mockResponse));

        await regulationAPI.fetchRegulations(); // First fetch to populate cache
        const cachedRegulations = await regulationAPI.fetchRegulations(); // Second fetch should hit cache

        expect(cachedRegulations).toEqual([{ id: 1, title: 'Regulation 1' }]);
        expect(axios.get).toHaveBeenCalledTimes(1); // Should only call once
    });

    test('should throw an error when trying to get regulation by ID that does not exist', async () => {
        const mockResponse = { data: [{ id: 1, title: 'Regulation 1' }] };
        axios.get.mockImplementationOnce(() => Promise.resolve(mockResponse));

        await regulationAPI.fetchRegulations(); // Populate cache

        await expect(regulationAPI.getRegulationById(999)).rejects.toThrow('Regulation not found');
    });

    test('should return regulation by ID if it exists', async () => {
        const mockResponse = { data: [{ id: 1, title: 'Regulation 1' }] };
        axios.get.mockImplementationOnce(() => Promise.resolve(mockResponse));

        await regulationAPI.fetchRegulations(); // Populate cache

        const regulation = await regulationAPI.getRegulationById(1);
        expect(regulation).toEqual({ id: 1, title: 'Regulation 1' });
    });
});
