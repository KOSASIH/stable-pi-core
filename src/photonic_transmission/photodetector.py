"""
photodetector - Implementation of photodetector for signal reception.

This module provides a class for modeling a photodetector that can
receive light signals and convert them into electrical signals.
"""

import numpy as np

class Photodetector:
    def __init__(self, responsivity: float, noise_current: float):
        """
        Initializes a Photodetector instance.

        Parameters:
            responsivity (float): The responsivity of the photodetector in A/W.
            noise_current (float): The noise current of the photodetector in A.
        """
        self.responsivity = responsivity
        self.noise_current = noise_current

    def receive_signal(self, optical_power: float) -> float:
        """
        Receives an optical signal and converts it to an electrical signal.

        Parameters:
            optical_power (float): The optical power of the incoming light in watts.

        Returns:
            float: The output electrical current in amperes.
        """
        # Calculate the output current based on the optical power and responsivity
        output_current = self.responsivity * optical_power
        return output_current

    def calculate_signal_to_noise_ratio(self, optical_power: float) -> float:
        """
        Calculates the signal-to-noise ratio (SNR) for the received signal.

        Parameters:
            optical_power (float): The optical power of the incoming light in watts.

        Returns:
            float: The signal-to-noise ratio (SNR) in dB.
        """
        signal_current = self.receive_signal(optical_power)
        noise_current = self.noise_current

        if noise_current == 0:
            raise ValueError("Noise current must be greater than zero to calculate SNR.")

        # SNR in linear scale
        snr_linear = signal_current / noise_current
        # Convert SNR to dB
        snr_db = 10 * np.log10(snr_linear)
        return snr_db

    def __str__(self):
        return (f"Photodetector(responsivity={self.responsivity} A/W, "
                f"noise_current={self.noise_current} A)")

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     photodetector = Photodetector(responsivity=0.8, noise_current=1e-9)
#     print(photodetector)
#     
#     optical_power = 1e-3  # 1 mW
#     output_current = photodetector.receive_signal(optical_power)
#     print("Output Current:", output_current, "A")
#     
#     snr = photodetector.calculate_signal_to_noise_ratio(optical_power)
#     print("Signal-to-Noise Ratio (SNR):", snr, "dB")
