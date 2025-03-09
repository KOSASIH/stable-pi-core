import pandas as pd
import random
import time
from datetime import datetime, timedelta

def collect_user_behavior(user_id, num_entries=10):
    """Simulate collecting user behavior data."""
    data = []
    for i in range(num_entries):
        timestamp = datetime.now() - timedelta(minutes=i * 5)  # Simulate timestamps
        activity_type = random.choice(['turn_on', 'turn_off'])
        temperature = random.uniform(20.0, 30.0)  # Simulated temperature
        humidity = random.uniform(30.0, 70.0)      # Simulated humidity
        
        data.append({
            'user_id': user_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'activity_type': activity_type,
            'temperature': temperature,
            'humidity': humidity
        })
    return data

def save_data_to_csv(data, filename='data/user_behavior.csv'):
    """Save collected data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

if __name__ == "__main__":
    user_data = []
    for user_id in range(1, 4):  # Simulate data for 3 users
        user_data.extend(collect_user_behavior(user_id=user_id, num_entries=5))
    save_data_to_csv(user_data)
    print("User behavior data collected and saved to user_behavior.csv.")
