import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(filename='data/user_behavior.csv'):
    """Load user behavior data from a CSV file."""
    try:
        df = pd.read_csv(filename)
        logging.info(f"Data loaded successfully from {filename}.")
        return df
    except FileNotFoundError:
        logging.error(f"File {filename} not found.")
        return None
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

def clean_data(df):
    """Clean the user behavior data."""
    if df is None:
        logging.warning("No data to clean.")
        return None

    # Drop duplicates
    initial_shape = df.shape
    df.drop_duplicates(inplace=True)
    logging.info(f"Dropped {initial_shape[0] - df.shape[0]} duplicate rows.")

    # Handle missing values
    missing_values = df.isnull().sum()
    if missing_values.any():
        logging.info("Missing values found:")
        logging.info(missing_values[missing_values > 0])
        df.fillna(method='ffill', inplace=True)  # Forward fill to handle missing values
        logging.info("Missing values have been filled.")

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    if df['timestamp'].isnull().any():
        logging.warning("Some timestamps could not be converted and will be dropped.")
        df.dropna(subset=['timestamp'], inplace=True)

    # Convert activity_type to category
    df['activity_type'] = df['activity_type'].astype('category')

    # Reset index
    df.reset_index(drop=True, inplace=True)

    logging.info("Data cleaning completed.")
    return df

def save_cleaned_data(df, filename='data/cleaned_user_behavior.csv'):
    """Save the cleaned data to a new CSV file."""
    if df is not None:
        try:
            df.to_csv(filename, index=False)
            logging.info(f"Cleaned data saved to {filename}.")
        except Exception as e:
            logging.error(f"Error saving cleaned data: {e}")

if __name__ == "__main__":
    # Load the data
    df = load_data()

    # Clean the data
    cleaned_df = clean_data(df)

    # Save the cleaned data
    save_cleaned_data(cleaned_df)
