import unittest
from photonic_transmission.waveguide import Waveguide

class TestWaveguide(unittest.TestCase):
    def setUp(self):
        """Set up a Waveguide instance for testing."""
        self.waveguide = Waveguide(core_index=1.5, cladding_index=1.45, length=1.0)

    def test_initialization(self):
        """Test the initialization of the Waveguide."""
        self.assertEqual(self.waveguide.core_index, 1.5)
        self.assertEqual(self.waveguide.cladding_index, 1.45)
        self.assertEqual(self.waveguide.length, 1.0)

    def test_critical_angle(self):
        """Test the calculation of the critical angle."""
        critical_angle = self.waveguide.calculate_critical_angle()
        self.assertAlmostEqual(critical_angle, 0.0867, places=4)  # Expected value in radians

    def test_effective_index(self):
        """Test the calculation of the effective index."""
        effective_index = self.waveguide.calculate_effective_index()
        self.assertAlmostEqual(effective_index, 1.475, places=3)  # Expected value

    def test_transmission_loss(self):
        """Test the calculation of transmission loss."""
        loss = self.waveguide.calculate_transmission_loss(wavelength=500e-9)  # 500 nm
        self.assertGreaterEqual(loss, 0)  # Loss should be non-negative

    def test_propagate_light(self):
        """Test the propagation of light through the waveguide."""
        input_power = 1.0  # 1 W
        output_power = self.waveguide.propagate_light(input_power=input_power, wavelength=500e-9)
        self.assertLess(output_power, input_power)  # Output power should be less than input power due to loss

if __name__ == '__main__':
    unittest.main()
