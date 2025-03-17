"""
waveguide - Implementation of waveguide for light transmission.

This module provides a class for modeling a waveguide that can
transmit light signals. It includes methods for calculating the
effective index, transmission loss, and simulating light propagation.
"""

import numpy as np

class Waveguide:
    def __init__(self, core_index: float, cladding_index: float, length: float):
        """
        Initializes a Waveguide instance.

        Parameters:
            core_index (float): The refractive index of the core material.
            cladding_index (float): The refractive index of the cladding material.
            length (float): The length of the waveguide in meters.
        """
        self.core_index = core_index
        self.cladding_index = cladding_index
        self.length = length

        # Calculate the critical angle for total internal reflection
        self.critical_angle = self.calculate_critical_angle()

    def calculate_critical_angle(self) -> float:
        """
        Calculates the critical angle for total internal reflection.

        Returns:
            float: The critical angle in radians.
        """
        if self.core_index <= self.cladding_index:
            raise ValueError("Core index must be greater than cladding index.")
        return np.arcsin(self.cladding_index / self.core_index)

    def calculate_effective_index(self) -> float:
        """
        Calculates the effective index of the waveguide.

        Returns:
            float: The effective index of the waveguide.
        """
        return (self.core_index + self.cladding_index) / 2

    def calculate_transmission_loss(self, wavelength: float) -> float:
        """
        Calculates the transmission loss in dB over the length of the waveguide.

        Parameters:
            wavelength (float): The wavelength of the light in meters.

        Returns:
            float: The transmission loss in dB.
        """
        # Example loss calculation (in dB) based on a simple model
        # This is a placeholder; real loss calculations would be more complex
        loss_coefficient = 0.2  # dB/m, example value
        return loss_coefficient * self.length

    def propagate_light(self, input_power: float, wavelength: float) -> float:
        """
        Simulates the propagation of light through the waveguide.

        Parameters:
            input_power (float): The input power of the light in watts.
            wavelength (float): The wavelength of the light in meters.

        Returns:
            float: The output power after transmission in watts.
        """
        loss = self.calculate_transmission_loss(wavelength)
        output_power = input_power * 10 ** (-loss / 10)  # Convert dB loss to linear scale
        return output_power

    def __str__(self):
        return (f"Waveguide(core_index={self.core_index}, "
                f"cladding_index={self.cladding_index}, "
                f"length={self.length}m, "
                f"critical_angle={np.degrees(self.critical_angle):.2f} degrees)")

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     wg = Waveguide(core_index=1.5, cladding_index=1.45, length=1.0)
#     print(wg)
#     print("Effective Index:", wg.calculate_effective_index())
#     print("Transmission Loss (500 nm):", wg.calculate_transmission_loss(500e-9), "dB")
#     print("Output Power:", wg.propagate_light(input_power=1.0, wavelength=500e-9), "W")
