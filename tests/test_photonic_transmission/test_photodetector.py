import unittest
from photonic_transmission.photodetector import Photodetector

class TestPhotodetector(unittest.TestCase):
    def setUp(self):
        """Set up a Photodetector instance for testing."""
        self.photodetector = Photodetector(responsivity=0.8, noise_current=1e-9)

    def test_initialization(self):
        """Test the initialization of the Photodetector."""
        self.assertEqual(self.photodetector.responsivity, 0.8)
        self.assertEqual(self.photodetector.noise_current, 1e-9)

    def test_receive_signal(self):
        """Test the signal reception and conversion to electrical current."""
        optical_power = 1e-3  # 1 mW
        output_current = self.photodetector.receive_signal(optical_power)
        expected_current = self.photodetector.responsivity * optical_power
        self.assertAlmostEqual(output_current, expected_current, places=6)

    def test_signal_to_noise_ratio(self):
        """Test the calculation of the signal-to-noise ratio (SNR)."""
        optical_power = 1e-3  # 1 mW
        snr = self.photodetector.calculate_signal_to_noise_ratio(optical_power)
        expected_snr = 10 * (self.photodetector.responsivity * optical_power / self.photodetector.noise_current)
        self.assertAlmostEqual(snr, expected_snr, places=6)

    def test_zero_noise_current(self):
        """Test handling of zero noise current in SNR calculation."""
        self.photodetector.noise_current = 0
        with self.assertRaises(ValueError):
            self.photodetector.calculate_signal_to_noise_ratio(1e-3)

if __name__ == '__main__':
    unittest.main()
