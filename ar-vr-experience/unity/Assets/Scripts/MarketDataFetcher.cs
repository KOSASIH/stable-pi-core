using System;
using System.Collections;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class MarketDataFetcher : MonoBehaviour
{
    // URL of the market data API
    [SerializeField] private string apiUrl = "https://api.example.com/marketdata";
    
    // UI elements to display market data
    [SerializeField] private Text marketDataText;
    [SerializeField] private Text errorText;

    // Refresh interval in seconds
    [SerializeField] private float refreshInterval = 60f;

    // Cached market data
    private MarketData cachedMarketData;

    // Start is called before the first frame update
    void Start()
    {
        // Fetch market data when the script starts
        FetchMarketDataAsync();
        // Start a coroutine to refresh data at specified intervals
        StartCoroutine(RefreshMarketData());
    }

    // Coroutine to refresh market data at specified intervals
    private IEnumerator RefreshMarketData()
    {
        while (true)
        {
            yield return new WaitForSeconds(refreshInterval);
            FetchMarketDataAsync();
        }
    }

    // Asynchronous method to fetch market data from the API
    private async void FetchMarketDataAsync()
    {
        try
        {
            MarketData marketData = await GetMarketDataAsync(apiUrl);
            if (marketData != null)
            {
                cachedMarketData = marketData; // Cache the fetched data
                UpdateMarketDataUI(marketData);
            }
        }
        catch (Exception ex)
        {
            Debug.LogError("Error fetching market data: " + ex.Message);
            errorText.text = "Error: " + ex.Message;
        }
    }

    // Method to get market data asynchronously
    private async Task<MarketData> GetMarketDataAsync(string url)
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(url))
        {
            // Send the request and wait for a response
            var operation = webRequest.SendWebRequest();

            while (!operation.isDone)
            {
                await Task.Yield(); // Yield control back to the main thread
            }

            // Check for network errors
            if (webRequest.result != UnityWebRequest.Result.Success)
            {
                throw new Exception(webRequest.error);
            }

            // Parse the JSON response
            string jsonResponse = webRequest.downloadHandler.text;
            return JsonUtility.FromJson<MarketData>(jsonResponse);
        }
    }

    // Method to update the UI with market data
    private void UpdateMarketDataUI(MarketData marketData)
    {
        marketDataText.text = $"Market Price: {marketData.price}\n" +
                              $"Market Volume: {marketData.volume}\n" +
                              $"Market Change: {marketData.change}%";
        errorText.text = ""; // Clear any previous error messages
    }

    // Class to represent the market data structure
    [Serializable]
    public class MarketData
    {
        public float price;
        public float volume;
        public float change;
    }
}
