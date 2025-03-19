"""
modulator - Implementation of modulator for encoding data.

This module provides a class for modeling a modulator that can
encode data onto a light signal using various modulation techniques.
"""

import numpy as np

class Modulator:
    def __init__(self, modulation_type: str, bitrate: float):
        """
        Initializes a Modulator instance.

        Parameters:
            modulation_type (str): The type of modulation (e.g., 'OOK', 'PSK', 'QAM').
            bitrate (float): The bitrate of the data in bits per second.
        """
        self.modulation_type = modulation_type
        self.bitrate = bitrate

    def encode_data(self, data: str) -> np.ndarray:
        """
        Encodes the input data using the specified modulation technique.

        Parameters:
            data (str): The input data to be encoded (binary string).

        Returns:
            np.ndarray: The encoded signal as a numpy array.
        """
        if self.modulation_type == 'OOK':
            return self._ook_modulation(data)
        elif self.modulation_type == 'PSK':
            return self._psk_modulation(data)
        elif self.modulation_type == 'QAM':
            return self._qam_modulation(data)
        else:
            raise ValueError(f"Unsupported modulation type: {self.modulation_type}")

    def _ook_modulation(self, data: str) -> np.ndarray:
        """On-Off Keying (OOK) modulation."""
        signal = []
        for bit in data:
            if bit == '1':
                signal.append(1)  # Light ON
            else:
                signal.append(0)  # Light OFF
        return np.array(signal)

    def _psk_modulation(self, data: str) -> np.ndarray:
        """Phase Shift Keying (PSK) modulation."""
        signal = []
        for bit in data:
            if bit == '1':
                signal.append(np.pi)  # Phase shift for '1'
            else:
                signal.append(0)  # Phase shift for '0'
        return np.array(signal)

    def _qam_modulation(self, data: str) -> np.ndarray:
        """Quadrature Amplitude Modulation (QAM) modulation."""
        signal = []
        for i in range(0, len(data), 2):
            if i + 1 < len(data):
                # Map pairs of bits to QAM symbols
                symbol = (int(data[i]) * 2) + int(data[i + 1])
                signal.append(symbol)  # QAM symbol
        return np.array(signal)

    def __str__(self):
        return f"Modulator(modulation_type={self.modulation_type}, bitrate={self.bitrate} bps)"

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     modulator = Modulator(modulation_type='OOK', bitrate=1000)
#     print(modulator)
#     encoded_signal = modulator.encode_data('1101001')
#     print("Encoded Signal (OOK):", encoded_signal)
#     
#     modulator_psk = Modulator(modulation_type='PSK', bitrate=1000)
#     encoded_signal_psk = modulator_psk.encode_data('1101001')
#     print("Encoded Signal (PSK):", encoded_signal_psk)
#     
#     modulator_qam = Modulator(modulation_type='QAM', bitrate=1000)
#     encoded_signal_qam = modulator_qam.encode_data('1101001')
#     print("Encoded Signal (QAM):", encoded_signal_qam)
