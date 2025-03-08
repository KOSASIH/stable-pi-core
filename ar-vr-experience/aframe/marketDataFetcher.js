// marketDataFetcher.js

class MarketDataFetcher {
    constructor(apiUrl) {
        this.apiUrl = apiUrl;
        this.marketData = null;
    }

    // Fetch market data from the API
    async fetchMarketData() {
        try {
            const response = await fetch(this.apiUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.marketData = await response.json();
            console.log("Market data fetched successfully:", this.marketData);
        } catch (error) {
            console.error("Error fetching market data:", error);
        }
    }

    // Get the fetched market data
    getMarketData() {
        if (this.marketData) {
            return this.marketData;
        } else {
            console.warn("Market data has not been fetched yet.");
            return null;
        }
    }

    // Example method to get specific market item by ID
    getMarketItemById(itemId) {
        if (this.marketData) {
            const item = this.marketData.find((marketItem) => marketItem.id === itemId);
            return item || null;
        } else {
            console.warn("Market data has not been fetched yet.");
            return null;
        }
    }

    // Example method to get all market items
    getAllMarketItems() {
        if (this.marketData) {
            return this.marketData;
        } else {
            console.warn("Market data has not been fetched yet.");
            return [];
        }
    }
}

// Example usage
const apiUrl = "https://api.example.com/marketdata"; // Replace with your actual API URL
const marketDataFetcher = new MarketDataFetcher(apiUrl);

// Fetch market data when the script loads
marketDataFetcher.fetchMarketData();

// You can later access the data using the methods provided
// For example, to get all market items after fetching:
setTimeout(() => {
    const allItems = marketDataFetcher.getAllMarketItems();
    console.log("All Market Items:", allItems);
}, 2000); // Adjust the timeout as needed based on your API response time
