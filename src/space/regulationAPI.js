// src/space/regulationAPI.js - Ultra Advanced Regulation API Module

const axios = require('axios');
const NodeCache = require('node-cache'); // In-memory caching
const { parseRegulationData } = require('./dataParser'); // Import data parser
const { logError, logInfo } = require('./logger'); // Import logger for error handling

class RegulationAPI {
    constructor(apiEndpoints, cacheTTL = 3600) {
        this.apiEndpoints = apiEndpoints; // Array of API endpoints
        this.cache = new NodeCache({ stdTTL: cacheTTL }); // Cache with default TTL
    }

    async fetchRegulations() {
        const regulationPromises = this.apiEndpoints.map(endpoint => this.fetchFromAPI(endpoint));
        try {
            const results = await Promise.all(regulationPromises);
            return results.flat(); // Flatten the array of results
        } catch (error) {
            logError('Error fetching regulations:', error);
            throw new Error('Failed to fetch regulations');
        }
    }

    async fetchFromAPI(endpoint) {
        // Check cache first
        const cachedData = this.cache.get(endpoint);
        if (cachedData) {
            logInfo(`Returning cached data for ${endpoint}`);
            return cachedData;
        }

        try {
            const response = await axios.get(endpoint);
            const parsedData = parseRegulationData(response.data); // Parse the data
            this.cache.set(endpoint, parsedData); // Cache the parsed data
            return parsedData;
        } catch (error) {
            logError(`Error fetching from ${endpoint}:`, error);
            throw new Error(`Failed to fetch from ${endpoint}`);
        }
    }

    async getRegulationById(id) {
        const regulations = await this.fetchRegulations();
        const regulation = regulations.find(reg => reg.id === id);
        if (!regulation) {
            throw new Error('Regulation not found');
        }
        return regulation;
    }

    // Method to refresh cache for a specific endpoint
    async refreshCache(endpoint) {
        try {
            const response = await axios.get(endpoint);
            const parsedData = parseRegulationData(response.data);
            this.cache.set(endpoint, parsedData);
            logInfo(`Cache refreshed for ${endpoint}`);
        } catch (error) {
            logError(`Error refreshing cache for ${endpoint}:`, error);
        }
    }
}

// Example usage
const regulationAPI = new RegulationAPI([
    'https://api.example.com/regulations',
    'https://api.anotherexample.com/regulations'
]);

(async () => {
    try {
        const regulations = await regulationAPI.fetchRegulations();
        console.log('Fetched Regulations:', regulations);
    } catch (error) {
        console.error('Error:', error.message);
    }
})();

module.exports = RegulationAPI;
