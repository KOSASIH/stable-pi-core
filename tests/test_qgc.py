import unittest
import json
from unittest.mock import MagicMock
from qgc.quantum_gravity_sensor import QuantumGravitySensor
from qgc.node_communication import NodeCommunication
from qgc.quantum_gravitational_consensus import QuantumGravitationalConsensus
from qgc.qgc_utils import validate_measurement, calculate_statistics, load_config

class TestQuantumGravitySensor(unittest.TestCase):
    def setUp(self):
        self.sensor = QuantumGravitySensor(sensor_id="TestSensor")

    def test_measure_gravity_within_range(self):
        measurement = self.sensor.measure_gravity()
        self.assertTrue(9.70 <= measurement <= 9.90, "Measurement out of expected range.")

    def test_calibration_effect(self):
        original_measurement = self.sensor.measure_gravity()
        self.sensor.calibrate()
        calibrated_measurement = self.sensor.measure_gravity()
        self.assertNotEqual(original_measurement, calibrated_measurement, "Calibration did not affect measurement.")

class TestNodeCommunication(unittest.TestCase):
    def setUp(self):
        self.node1 = NodeCommunication(node_id="Node1")
        self.node2 = NodeCommunication(node_id="Node2")
        self.node1.connect_to_node(self.node2)

    def test_send_receive_measurement(self):
        measurement = 9.81
        self.node1.send_measurement(measurement, self.node2)
        # Simulate receiving the measurement
        message = json.dumps({"sender": "Node1", "measurement": measurement, "timestamp": 1234567890})
        self.node2.receive_measurement(message)
        self.assertIn(measurement, self.node2.measurements, "Measurement not received correctly.")

    def test_connection_limit(self):
        for i in range(3, 25):  # Exceeding max_connections
            node = NodeCommunication(node_id=f"Node{i}")
            self.node1.connect_to_node(node)
        self.assertEqual(len(self.node1.connected_nodes), 20, "Connection limit not enforced.")

class TestQuantumGravitationalConsensus(unittest.TestCase):
    def setUp(self):
        self.consensus = QuantumGravitationalConsensus(initial_threshold=0.1)

    def test_add_measurement_and_reach_consensus(self):
        measurements = [9.78, 9.81, 9.79, 9.82, 9.75]
        for m in measurements:
            self.consensus.add_measurement(m)
        consensus_value = self.consensus.reach_consensus()
        self.assertIsNotNone(consensus_value, "Consensus value should not be None.")
        self.assertTrue(9.70 <= consensus_value <= 9.90, "Consensus value out of expected range.")

    def test_outlier_detection(self):
        measurements = [9.78, 9.81, 9.79, 9.82, 9.75, 10.5]  # 10.5 is an outlier
        for m in measurements:
            self.consensus.add_measurement(m)
        consensus_value = self.consensus.reach_consensus()
        self.assertNotIn(10.5, self.consensus.measurements, "Outlier should not be included in consensus.")

class TestQGCUtils(unittest.TestCase):
    def test_validate_measurement(self):
        self.assertTrue(validate_measurement(9.81, 9.70, 9.90), "Measurement should be valid.")
        self.assertFalse(validate_measurement(9.95, 9.70, 9.90), "Measurement should be invalid.")

    def test_calculate_statistics(self):
        measurements = [9.78, 9.81, 9.79, 9.82, 9.75]
        stats = calculate_statistics(measurements)
        self.assertAlmostEqual(stats["mean"], 9.79, places=2, msg="Mean calculation is incorrect.")
        self.assertAlmostEqual(stats["std_dev"], 0.025, places=2, msg="Standard deviation calculation is incorrect.")

    def test_load_config(self):
        config = load_config("qgc/qgc_config.yaml")
        self.assertIsNotNone(config, "Config should be loaded successfully.")
        self.assertIn("logging", config, "Logging configuration should be present in the config.")

    def test_load_nonexistent_config(self):
        config = load_config("nonexistent.yaml")
        self.assertIsNone(config, "Loading a nonexistent config should return None.")

if __name__ == "__main__":
    unittest.main()
