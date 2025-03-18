# tests/test_core.py

import unittest
import numpy as np
import os
from core.utils import load_config, save_to_file, generate_random_state, calculate_inner_product, validate_quantum_state, create_directory

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        self.config_file = "core/config.yaml"
        self.test_json_file = "test_output.json"
        self.test_dir = "test_dir"

    def test_load_config(self):
        """Test loading a valid configuration file."""
        config = load_config(self.config_file)
        self.assertIsInstance(config, dict)

    def test_save_to_file(self):
        """Test saving data to a file."""
        data = {"key": "value"}
        save_to_file(data, self.test_json_file)
        loaded_data = load_config(self.test_json_file)
        self.assertEqual(data, loaded_data)

    def test_generate_random_state(self):
        """Test generating a random quantum state."""
        state = generate_random_state(2)
        self.assertEqual(state.shape, (4,))
        self.assertTrue(validate_quantum_state(state))

    def test_calculate_inner_product(self):
        """Test calculating the inner product of two quantum states."""
        state1 = generate_random_state(2)
        state2 = generate_random_state(2)
        inner_product = calculate_inner_product(state1, state2)
        self.assertIsInstance(inner_product, complex)

    def test_validate_quantum_state(self):
        """Test validating a quantum state."""
        state = generate_random_state(2)
        self.assertTrue(validate_quantum_state(state))

    def test_create_directory(self):
        """Test creating a directory."""
        create_directory(self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir))
        os.rmdir(self.test_dir)  # Clean up

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_json_file):
            os.remove(self.test_json_file)

if __name__ == "__main__":
    unittest.main()
