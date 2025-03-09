import sqlite3
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Database:
    def __init__(self, db_name='user_behavior.db'):
        """Initialize the database connection."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        logging.info(f"Connected to database: {db_name}")
        self.create_table()

    def create_table(self):
        """Create a table for storing user behavior data if it doesn't exist."""
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS user_behavior (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            activity_type TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL
        )
        '''
        self.cursor.execute(create_table_query)
        self.connection.commit()
        logging.info("User  behavior table created or already exists.")

    def insert_data(self, user_data):
        """Insert user behavior data into the database."""
        insert_query = '''
        INSERT INTO user_behavior (user_id, timestamp, activity_type, temperature, humidity)
        VALUES (?, ?, ?, ?, ?)
        '''
        try:
            self.cursor.executemany(insert_query, user_data)
            self.connection.commit()
            logging.info(f"Inserted {len(user_data)} records into the database.")
        except Exception as e:
            logging.error(f"Error inserting data: {e}")

    def fetch_data(self):
        """Fetch all user behavior data from the database."""
        fetch_query = "SELECT * FROM user_behavior"
        try:
            df = pd.read_sql_query(fetch_query, self.connection)
            logging.info("Data fetched successfully from the database.")
            return df
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        self.connection.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    # Example usage
    db = Database()

    # Simulate inserting data
    sample_data = [
        (1, '2023-10-01 10:00:00', 'turn_on', 22.5, 60),
        (1, '2023-10-01 10:05:00', 'turn_off', 22.5, 60),
        (2, '2023-10-01 11:00:00', 'turn_on', 21.0, 65),
        (3, '2023-10-01 12:00:00', 'adjust_temperature', 24.0, 50)
    ]
    db.insert_data(sample_data)

    # Fetch and display data
    data = db.fetch_data()
    print(data)

    # Close the database connection
    db.close_connection()
