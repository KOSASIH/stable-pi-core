# tests/test_data_preprocessing.py

import pytest
import pandas as pd
from src.data_preprocessing import load_data, preprocess_data

def test_load_data():
    # Assuming the CSV file exists in the data directory
    df = load_data('../data/historical_data.csv')
    assert isinstance(df, pd.DataFrame), "Loaded data should be a DataFrame"
    assert not df.empty, "DataFrame should not be empty"

def test_preprocess_data():
    # Create a sample DataFrame for testing
    sample_data = {
        'date': ['2021-01-01', '2021-01-02', None],
        'feature1': [1.0, 1.5, 2.0],
        'feature2': [2.0, 2.5, 3.0],
        'target': [10, 15, 20]
    }
    df = pd.DataFrame(sample_data)

    # Preprocess the data
    processed_df = preprocess_data(df)

    # Check that missing values are dropped
    assert processed_df.isnull().sum().sum() == 0, "There should be no missing values"
    assert 'date' in processed_df.columns, "Date column should be present"
