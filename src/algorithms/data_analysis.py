import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

class DataAnalysis:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.model = IsolationForest(contamination=0.1, random_state=42)

    def preprocess_data(self):
        """
        Preprocess the data by handling missing values and scaling.
        """
        # Fill missing values with the mean of each column
        self.data.fillna(self.data.mean(), inplace=True)

    def detect_anomalies(self) -> pd.DataFrame:
        """
        Detect anomalies in the data using Isolation Forest.
        Returns a DataFrame with anomaly scores and labels.
        """
        self.preprocess_data()
        self.model.fit(self.data)
        self.data['anomaly_score'] = self.model.decision_function(self.data)
        self.data['anomaly'] = self.model.predict(self.data)
        return self.data

    def visualize_anomalies(self):
        """
        Visualize the anomalies in the dataset.
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(self.data.index, self.data['anomaly_score'], c=self.data['anomaly'], cmap='coolwarm', marker='o')
        plt.title('Anomaly Detection using Isolation Forest')
        plt.xlabel('Index')
        plt.ylabel('Anomaly Score')
        plt.axhline(y=0, color='r', linestyle='--')
        plt.show()

# Example usage
if __name__ == "__main__":
    # Generate synthetic data for demonstration
    np.random.seed(42)
    normal_data = np.random.normal(loc=0, scale=1, size=(100, 2))
    anomaly_data = np.random.normal(loc=5, scale=1, size=(10, 2))
    data = np.vstack((normal_data, anomaly_data))
    df = pd.DataFrame(data, columns=['Feature 1', 'Feature 2'])

    # Perform data analysis and anomaly detection
    analysis = DataAnalysis(df)
    results = analysis.detect_anomalies()
    print(results)

    # Visualize the anomalies
    analysis.visualize_anomalies()
