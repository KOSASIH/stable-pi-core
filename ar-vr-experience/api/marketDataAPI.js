// api/marketDataAPI.js

class MarketDataAPI {
    constructor(apiUrl) {
        this.apiUrl = apiUrl; // Base URL for the market data API
    }

    // Fetch market data from the API
    async fetchMarketData() {
        try {
            const response = await fetch(`${this.apiUrl}/marketdata`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            console.log("Market data fetched successfully:", data);
            return data;
        } catch (error) {
            console.error("Error fetching market data:", error);
            throw error; // Rethrow the error for further handling
        }
    }

    // Get a specific market item by ID
    async getMarketItemById(itemId) {
        try {
            const response = await fetch(`${this.apiUrl}/marketdata/${itemId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const item = await response.json();
            return item;
        } catch (error) {
            console.error("Error fetching market item:", error);
            throw error; // Rethrow the error for further handling
        }
    }
}

// Example usage
const marketAPI = new MarketDataAPI('https://api.example.com'); // Replace with your actual API URL
marketAPI.fetchMarketData().then(data => {
    console.log("Fetched Market Data:", data);
}).catch(error => {
    console.error("Failed to fetch market data:", error);
});
