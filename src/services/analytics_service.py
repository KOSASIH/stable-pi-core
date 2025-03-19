import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from flask import Flask, render_template
import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.data = None

    async def load_data(self, source: str, source_type: str = 'csv'):
        """
        Load data from a specified source.
        :param source: The source of the data (file path, URL, etc.).
        :param source_type: The type of the source ('csv', 'api', etc.).
        """
        if source_type == 'csv':
            self.data = pd.read_csv(source)
        elif source_type == 'api':
            async with aiohttp.ClientSession() as session:
                async with session.get(source) as response:
                    response.raise_for_status()
                    self.data = pd.DataFrame(await response.json())
        else:
            logger.error("Unsupported source type.")
            return

        logger.info("Data loaded successfully.")

    def analyze_data(self):
        """
        Perform basic analysis on the loaded data.
        """
        if self.data is not None:
            summary = self.data.describe()
            logger.info("Data Analysis Summary:")
            logger.info(summary)
            return summary
        else:
            logger.error("No data loaded for analysis.")
            return None

    def visualize_data(self, column: str):
        """
        Create a visualization for a specified column.
        :param column: The column to visualize.
        """
        if self.data is not None and column in self.data.columns:
            plt.figure(figsize=(10, 5))
            plt.plot(self.data[column])
            plt.title(f"{column} Over Time")
            plt.xlabel("Index")
            plt.ylabel(column)
            plt.grid()
            plt.show()
        else:
            logger.error("Data not loaded or column not found.")

    def create_dashboard(self):
        """
        Create a simple web-based dashboard using Flask.
        """
        app = Flask(__name__)

        @app.route('/')
        def index():
            return render_template('dashboard.html', data=self.data.to_html())

        app.run(debug=True)

# Example usage
async def main():
    analytics_service = AnalyticsService()
    await analytics_service.load_data('https://example.com/data.csv', source_type='csv')
    analytics_service.analyze_data()
    analytics_service.visualize_data('column_name')  # Replace 'column_name' with an actual column name
    analytics_service.create_dashboard()

if __name__ == "__main__":
    asyncio.run(main())
