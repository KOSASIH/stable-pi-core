import numpy as np
import logging

def encode_data(data: bytes) -> np.ndarray:
    """
    Encodes data into a holographic format.

    Args:
        data (bytes): The data to encode.

    Returns:
        np.ndarray: The encoded holographic data as a NumPy array.
    """
    try:
        # Convert bytes to a NumPy array of uint8
        encoded_data = np.frombuffer(data, dtype=np.uint8)

        # Example holographic encoding logic (this should be replaced with actual encoding)
        # For demonstration, we will reshape the data into a 3D array
        side_length = int(np.ceil(len(encoded_data) ** (1/3)))  # Calculate the side length for a cubic shape
        holographic_array = np.zeros((side_length, side_length, side_length), dtype=np.uint8)

        # Fill the holographic array with encoded data
        holographic_array.flat[:len(encoded_data)] = encoded_data

        logging.info("Data encoded into holographic format successfully.")
        return holographic_array
    except Exception as e:
        logging.error(f"Error encoding data: {e}")
        return None

def decode_data(holographic_array: np.ndarray) -> bytes:
    """
    Decodes holographic data back into its original byte format.

    Args:
        holographic_array (np.ndarray): The holographic data to decode.

    Returns:
        bytes: The decoded data in its original format.
    """
    try:
        # Flatten the holographic array and remove any trailing zeros
        flat_data = holographic_array.flatten()
        decoded_data = flat_data[flat_data != 0]  # Remove zeros (if any)

        # Convert the decoded data back to bytes
        return decoded_data.tobytes()
    except Exception as e:
        logging.error(f"Error decoding data: {e}")
        return None
