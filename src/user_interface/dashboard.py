# src/user_interface/dashboard.py

import logging
import random
import time

# Set up logging for the dashboard module
logger = logging.getLogger(__name__)

class Dashboard:
    def __init__(self, user_id):
        """
        Initialize the Dashboard.

        Parameters:
        - user_id (str): The ID of the user associated with the dashboard.
        """
        self.user_id = user_id
        logger.info(f"Dashboard initialized for user: {self.user_id}")

    def display_balance(self, wallet):
        """
        Display the current balance from the wallet.

        Parameters:
        - wallet (Wallet): An instance of the Wallet class.
        """
        balance = wallet.get_balance()
        logger.info(f"Displaying balance for user {self.user_id}: {balance}")
        print(f"Current Balance: ${balance:.2f}")

    def display_market_trends(self):
        """
        Simulate displaying market trends.

        This method simulates fetching and displaying market trends in real-time.
        """
        logger.info("Starting market trends display.")
        try:
            while True:
                # Simulate fetching market data
                market_data = self._fetch_market_data()
                logger.info(f"Market Trends: {market_data}")
                print(f"Market Trends: {market_data}")
                time.sleep(5)  # Update every 5 seconds
        except KeyboardInterrupt:
            logger.info("Market trends display stopped by user.")

    def _fetch_market_data(self):
        """
        Simulate fetching market data.

        Returns:
        - dict: Simulated market data.
        """
        # Simulate market data with random values
        return {
            'BTC': round(random.uniform(30000, 60000), 2),
            'ETH': round(random.uniform(2000, 4000), 2),
            'LTC': round(random.uniform(100, 300), 2),
        }
