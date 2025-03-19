"""
data_processing - Functions for processing data at the edge.

This module provides various data processing functions that can be
applied to the data received by edge nodes in an edge computing architecture.
"""

import numpy as np

def process_data(data: np.ndarray, operation: str = 'mean') -> float:
    """
    Processes the input data based on the specified operation.

    Parameters:
        data (np.ndarray): The input data to be processed.
        operation (str): The operation to perform ('mean', 'sum', 'max', 'min').

    Returns:
        float: The result of the processing operation.
    """
    if operation == 'mean':
        return np.mean(data)
    elif operation == 'sum':
        return np.sum(data)
    elif operation == 'max':
        return np.max(data)
    elif operation == 'min':
        return np.min(data)
    else:
        raise ValueError(f"Unsupported operation: {operation}")

def aggregate_data(data_list: list) -> np.ndarray:
    """
    Aggregates a list of data arrays into a single array.

    Parameters:
        data_list (list): A list of numpy arrays to be aggregated.

    Returns:
        np.ndarray: A single aggregated array.
    """
    return np.concatenate(data_list)

def filter_data(data: np.ndarray, threshold: float) -> np.ndarray:
    """
    Filters the input data based on a threshold.

    Parameters:
        data (np.ndarray): The input data to be filtered.
        threshold (float): The threshold value for filtering.

    Returns:
        np.ndarray: The filtered data containing values above the threshold.
    """
    return data[data > threshold]

def normalize_data(data: np.ndarray) -> np.ndarray:
    """
    Normalizes the input data to a range of [0, 1].

    Parameters:
        data (np.ndarray): The input data to be normalized.

    Returns:
        np.ndarray: The normalized data.
    """
    min_val = np.min(data)
    max_val = np.max(data)
    return (data - min_val) / (max_val - min_val) if max_val > min_val else data

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     data = np.array([1, 2, 3, 4, 5])
#     print("Original Data:", data)
#     
#     mean_value = process_data(data, operation='mean')
#     print("Mean:", mean_value)
#     
#     aggregated_data = aggregate_data([data, data * 2])
#     print("Aggregated Data:", aggregated_data)
#     
#     filtered_data = filter_data(data, threshold=3)
#     print("Filtered Data (threshold=3):", filtered_data)
#     
#     normalized_data = normalize_data(data)
#     print("Normalized Data:", normalized_data)
