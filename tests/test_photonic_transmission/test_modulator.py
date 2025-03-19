import unittest
from photonic_transmission.modulator import Modulator

class TestModulator(unittest.TestCase):
    def setUp(self):
        """Set up a Modulator instance for testing."""
        self.modulator = Modulator(modulation_type='OOK', bitrate=1000)

    def test_initialization(self):
        """Test the initialization of the Modulator."""
        self.assertEqual(self.modulator.modulation_type, 'OOK')
        self.assertEqual(self.modulator.bitrate, 1000)

    def test_ook_modulation(self):
        """Test the On-Off Keying (OOK) modulation."""
        data = '1101001'
        encoded_signal = self.modulator.encode_data(data)
        expected_signal = [1, 1, 0, 1, 0, 0, 1]  # Expected OOK signal
        self.assertTrue((encoded_signal == expected_signal).all())

    def test_psk_modulation(self):
        """Test the Phase Shift Keying (PSK) modulation."""
        self.modulator.modulation_type = 'PSK'
        data = '1101001'
        encoded_signal = self.modulator.encode_data(data)
        expected_signal = [3.14159, 0, 3.14159, 0, 0, 0, 3.14159]  # Expected PSK signal
        self.assertTrue((encoded_signal == expected_signal).all())

    def test_qam_modulation(self):
        """Test the Quadrature Amplitude Modulation (QAM) modulation."""
        self.modulator.modulation_type = 'QAM'
        data = '1101001'
        encoded_signal = self.modulator.encode_data(data)
        expected_signal = [3, 2, 1]  # Expected QAM symbols
        self.assertTrue((encoded_signal == expected_signal).all())

    def test_invalid_modulation_type(self):
        """Test handling of an unsupported modulation type."""
        self.modulator.modulation_type = 'INVALID'
        with self.assertRaises(ValueError):
            self.modulator.encode_data('1101001')

if __name__ == '__main__':
    unittest.main()
