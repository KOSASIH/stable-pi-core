# src/main/utils/helpers.py

import pandas as pd
import numpy as np
import logging

def preprocess_data(raw_data):
    """
    Preprocess the raw input data for machine learning models.
    
    Args:
        raw_data (dict): A dictionary containing the raw input data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed data.
    """
    logging.info("Starting data preprocessing...")
    
    # Convert raw data to DataFrame
    df = pd.DataFrame(raw_data)
    
    # Handle missing values
    df.fillna(method='ffill', inplace=True)  # Forward fill for simplicity
    logging.info("Missing values handled.")

    # Normalize numerical features
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    df[numerical_cols] = (df[numerical_cols] - df[numerical_cols].mean()) / df[numerical_cols].std()
    logging.info("Numerical features normalized.")

    return df

def validate_data(data, required_columns):
    """
    Validate the input data to ensure it contains the required columns.
    
    Args:
        data (pd.DataFrame): The input data to validate.
        required_columns (list): A list of required column names.

    Returns:
        bool: True if validation passes, False otherwise.
    """
    logging.info("Validating data...")
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        logging.error("Missing required columns: %s", missing_columns)
        return False
    
    logging.info("Data validation passed.")
    return True

def split_data(data, target_column, test_size=0.2, random_state=42):
    """
    Split the data into training and testing sets.
    
    Args:
        data (pd.DataFrame): The input data to split.
        target_column (str): The name of the target column.
        test_size (float): The proportion of the dataset to include in the test split.
        random_state (int): Random seed for reproducibility.

    Returns:
        tuple: Training features, testing features, training labels, testing labels.
    """
    logging.info("Splitting data into training and testing sets...")
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    logging.info("Data split completed: %d training samples, %d testing samples.", len(X_train), len(X_test))
    return X_train, X_test, y_train, y_test

def save_to_csv(data, filename):
    """
    Save a DataFrame to a CSV file.
    
    Args:
        data (pd.DataFrame): The DataFrame to save.
        filename (str): The name of the file to save to.
    """
    logging.info("Saving data to %s...", filename)
    data.to_csv(filename, index=False)
    logging.info("Data saved successfully.")

def load_from_csv(filename):
    """
    Load data from a CSV file into a DataFrame.
    
    Args:
        filename (str): The name of the file to load from.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    logging.info("Loading data from %s...", filename)
    df = pd.read_csv(filename)
    logging.info("Data loaded successfully with %d samples.", len(df))
    return df
