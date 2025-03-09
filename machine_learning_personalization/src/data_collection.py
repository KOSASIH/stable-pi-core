import pandas as pd
import random
import time
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def collect_user_behavior(user_id, num_entries=10):
    """Simulate collecting user behavior data."""
    data = []
    for i in range(num_entries):
        timestamp = datetime.now() - timedelta(minutes=i * 5)  # Simulate timestamps
        activity_type = random.choice(['turn_on', 'turn_off', 'adjust_temperature', 'adjust_humidity'])
        temperature = random.uniform(18.0, 32.0)  # Simulated temperature range
        humidity = random.uniform(25.0, 75.0)      # Simulated humidity range
        
        data.append({
            'user_id': user_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'activity_type': activity_type,
            'temperature': round(temperature, 2),  # Round for better readability
            'humidity': round(humidity, 2)           # Round for better readability
        })
    return data

def save_data_to_csv(data, filename='data/user_behavior.csv'):
    """Save collected data to a CSV file."""
    df = pd.DataFrame(data)
    try:
        df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)
        logging.info(f"Data saved to {filename}.")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")

if __name__ == "__main__":
    user_data = []
    num_users = 3  # Number of users to simulate
    num_entries_per_user = 10  # Number of entries per user

    for user_id in range(1, num_users + 1):  # Simulate data for specified number of users
        user_data.extend(collect_user_behavior(user_id=user_id, num_entries=num_entries_per_user))
    
    save_data_to_csv(user_data)
    logging.info("User  behavior data collection completed.")
