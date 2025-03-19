"""
transmission_layer - Main class for the photonic data transmission layer.

This module provides a class for managing the photonic data transmission
process, including encoding data, transmitting it through a waveguide,
and receiving it with a photodetector.
"""

import numpy as np
from .waveguide import Waveguide
from .modulator import Modulator
from .photodetector import Photodetector

class TransmissionLayer:
    def __init__(self, waveguide: Waveguide, modulator: Modulator, photodetector: Photodetector):
        """
        Initializes a TransmissionLayer instance.

        Parameters:
            waveguide (Waveguide): The waveguide used for transmission.
            modulator (Modulator): The modulator used for encoding data.
            photodetector (Photodetector): The photodetector used for receiving signals.
        """
        self.waveguide = waveguide
        self.modulator = modulator
        self.photodetector = photodetector

    def transmit_data(self, data: str, wavelength: float) -> float:
        """
        Transmits the input data through the photonic transmission layer.

        Parameters:
            data (str): The input data to be transmitted (binary string).
            wavelength (float): The wavelength of the light in meters.

        Returns:
            float: The output current received by the photodetector in amperes.
        """
        # Step 1: Encode the data using the modulator
        encoded_signal = self.modulator.encode_data(data)

        # Step 2: Calculate the optical power based on the encoded signal
        optical_power = self.calculate_optical_power(encoded_signal)

        # Step 3: Transmit the optical power through the waveguide
        transmitted_power = self.transmit_through_waveguide(optical_power, wavelength)

        # Step 4: Receive the signal with the photodetector
        output_current = self.photodetector.receive_signal(transmitted_power)

        return output_current

    def calculate_optical_power(self, encoded_signal: np.ndarray) -> float:
        """
        Calculates the optical power based on the encoded signal.

        Parameters:
            encoded_signal (np.ndarray): The encoded signal array.

        Returns:
            float: The calculated optical power in watts.
        """
        # Example: Assume each '1' in the encoded signal contributes 1 mW of power
        power_per_bit = 1e-3  # 1 mW
        optical_power = np.sum(encoded_signal) * power_per_bit
        return optical_power

    def transmit_through_waveguide(self, optical_power: float, wavelength: float) -> float:
        """
        Transmits the optical power through the waveguide.

        Parameters:
            optical_power (float): The optical power to be transmitted in watts.
            wavelength (float): The wavelength of the light in meters.

        Returns:
            float: The transmitted optical power after losses in watts.
        """
        # Calculate the transmission loss using the waveguide
        loss = self.waveguide.calculate_transmission_loss(wavelength)
        transmitted_power = optical_power * 10 ** (-loss / 10)  # Convert dB loss to linear scale
        return transmitted_power

    def __str__(self):
        return (f"TransmissionLayer(\n"
                f"  Waveguide: {self.waveguide},\n"
                f"  Modulator: {self.modulator},\n"
                f"  Photodetector: {self.photodetector}\n"
                f")")

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     # Create instances of the components
#     waveguide = Waveguide(core_index=1.5, cladding_index=1.45, length=1.0)
#     modulator = Modulator(modulation_type='OOK', bitrate=1000)
#     photodetector = Photodetector(responsivity=0.8, noise_current=1e-9)
#     
#     # Create the transmission layer
#     transmission_layer = TransmissionLayer(waveguide, modulator, photodetector)
#     print(transmission_layer)
#     
#     # Transmit data
#     data = '1101001'
#     wavelength = 500e-9  # 500 nm
#     output_current = transmission_layer.transmit_data(data, wavelength)
#     print("Output Current:", output_current, "A")
