import numpy as np
import logging
from sklearn.linear_model import LinearRegression

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PatternRecognizer:
    def __init__(self, window_size=5):
        """
        Initialize the PatternRecognizer with a specified window size for moving average.
        
        Parameters:
            window_size (int): The number of data points to consider for the moving average.
        """
        self.window_size = window_size
        self.temperature_data = []
        self.humidity_data = []

    def add_data(self, temperature, humidity):
        """
        Add new sensor data to the recognizer.
        
        Parameters:
            temperature (float): The temperature value.
            humidity (float): The humidity value.
        """
        self.temperature_data.append(temperature)
        self.humidity_data.append(humidity)

        # Keep only the last 'window_size' data points
        if len(self.temperature_data) > self.window_size:
            self.temperature_data.pop(0)
        if len(self.humidity_data) > self.window_size:
            self.humidity_data.pop(0)

    def moving_average(self, data):
        """
        Calculate the moving average of the given data.
        
        Parameters:
            data (list): A list of numerical values.
        
        Returns:
            float: The moving average of the data, or None if not enough data points.
        """
        if len(data) < self.window_size:
            return None
        return np.mean(data)

    def detect_trend(self, data):
        """
        Detect trends in the data using linear regression.
        
        Parameters:
            data (list): A list of numerical values.
        
        Returns:
            str: A string indicating the trend ("increasing", "decreasing", "stable").
        """
        if len(data) < 2:
            return "insufficient data"

        x = np.arange(len(data)).reshape(-1, 1)  # Time steps
        y = np.array(data).reshape(-1, 1)  # Sensor values

        model = LinearRegression()
        model.fit(x, y)
        trend = model.coef_[0][0]

        if trend > 0:
            return "increasing"
        elif trend < 0:
            return "decreasing"
        else:
            return "stable"

    def recognize_patterns(self):
        """
        Recognize patterns in the temperature and humidity data.
        
        Returns:
            dict: A dictionary containing the moving averages and trends of temperature and humidity.
        """
        temp_avg = self.moving_average(self.temperature_data)
        humidity_avg = self.moving_average(self.humidity_data)

        temp_trend = self.detect_trend(self.temperature_data)
        humidity_trend = self.detect_trend(self.humidity_data)

        patterns = {
            'temperature_moving_average': temp_avg,
            'humidity_moving_average': humidity_avg,
            'temperature_trend': temp_trend,
            'humidity_trend': humidity_trend
        }

        if temp_avg is not None:
            logging.info(f"Current Temperature Moving Average: {temp_avg:.2f}, Trend: {temp_trend}")
        if humidity_avg is not None:
            logging.info(f"Current Humidity Moving Average: {humidity_avg:.2f}, Trend: {humidity_trend}")

        return patterns

# Example usage
if __name__ == "__main__":
    recognizer = PatternRecognizer(window_size=5)

    # Simulate adding data
    for i in range(10):
        temperature = 20 + (i % 5)  # Simulated temperature data
        humidity = 50 + (i % 3)      # Simulated humidity data
        recognizer.add_data(temperature, humidity)
        recognizer.recognize_patterns()
