import asyncio
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from .neuromorphic_chip import NeuromorphicChip
from .models.neuromorphic_model import NeuromorphicModel

class EdgeComputing:
    def __init__(self, neuromorphic_chip: NeuromorphicChip):
        self.neuromorphic_chip = neuromorphic_chip
        self.model = NeuromorphicModel()
        self.executor = ThreadPoolExecutor(max_workers=4)  # For concurrent processing

    async def collect_data(self, sensor_data: list):
        """
        Collects and processes sensor data using the neuromorphic chip.

        Args:
            sensor_data (list): A list of sensor data to be processed.

        Returns:
            dict: A dictionary containing processed data and status.
        """
        try:
            # Process data asynchronously
            processed_data = await self.process_data(sensor_data)
            return {
                "status": "success",
                "processed_data": processed_data
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    async def process_data(self, sensor_data: list):
        """
        Processes the sensor data using the neuromorphic chip.

        Args:
            sensor_data (list): A list of sensor data to be processed.

        Returns:
            list: A list of processed data.
        """
        loop = asyncio.get_event_loop()
        # Use ThreadPoolExecutor to run blocking code in a separate thread
        processed_data = await loop.run_in_executor(self.executor, self._process_with_chip, sensor_data)
        return processed_data

    def _process_with_chip(self, sensor_data: list):
        """
        Synchronously processes data with the neuromorphic chip.

        Args:
            sensor_data (list): A list of sensor data to be processed.

        Returns:
            list: A list of processed data.
        """
        # Simulate data preprocessing (e.g., normalization)
        normalized_data = self._normalize_data(sensor_data)
        # Process the normalized data with the neuromorphic chip
        return self.neuromorphic_chip.process(normalized_data)

    def _normalize_data(self, data: list):
        """
        Normalizes the input data for better processing.

        Args:
            data (list): A list of raw sensor data.

        Returns:
            list: A list of normalized data.
        """
        data_array = np.array(data)
        normalized = (data_array - np.mean(data_array)) / np.std(data_array)
        return normalized.tolist()

    async def run_model_simulation(self, duration: float):
        """
        Runs the neuromorphic model simulation asynchronously.

        Args:
            duration (float): Duration for the simulation.

        Returns:
            list: Output from the neuromorphic model.
        """
        loop = asyncio.get_event_loop()
        output = await loop.run_in_executor(self.executor, self.model.run_simulation, duration)
        return output
