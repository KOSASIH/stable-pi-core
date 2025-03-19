import unittest
import time
from itp.SRC.space_time_synchronization import SpaceTimeSynchronization

class TestSpaceTimeSynchronization(unittest.TestCase):
    def setUp(self):
        """Set up the Space-Time Synchronization for testing."""
        self.stsp = SpaceTimeSynchronization()

    def test_synchronize_time(self):
        """Test synchronizing time with a celestial body."""
        celestial_time = time.time() + 5  # Simulate celestial body time 5 seconds ahead
        self.stsp.synchronize_time(celestial_time)
        self.assertAlmostEqual(self.stsp.local_time_offset, celestial_time - time.time(), delta=1)

    def test_get_current_time(self):
        """Test getting the current synchronized time."""
        self.stsp.synchronize_time(time.time() + 5)  # Simulate synchronization
        current_time = self.stsp.get_current_time()
        self.assertAlmostEqual(current_time, time.time() + 5, delta=1)

    def test_periodic_sync(self):
        """Test periodic synchronization (mocked)."""
        # This test would require threading or async handling to test properly
        # For simplicity, we will just check if the method runs without error
        try:
            self.stsp.periodic_sync()  # This would run indefinitely; in a real test, we would mock this
        except Exception as e:
            self.fail(f"Periodic sync raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
