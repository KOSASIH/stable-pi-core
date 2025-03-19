# tests/test_stsp.py

import unittest
from unittest.mock import patch, MagicMock
from stsp.stsp_protocol import STSPProtocol

class TestSTSPProtocol(unittest.TestCase):
    @patch('stsp.stsp_protocol.EdgeNode')
    @patch('stsp.stsp_protocol.DataProcessor')
    @patch('stsp.stsp_protocol.EdgeCommunication')
    @patch('stsp.stsp_protocol.SatelliteManager')
    @patch('stsp.stsp_protocol.QuantumTimeTransfer')
    @patch('stsp.stsp_protocol.CrossChainBridge')
    def setUp(self, MockCrossChainBridge, MockQuantumTimeTransfer, MockSatelliteManager,
              MockEdgeCommunication, MockDataProcessor, MockEdgeNode):
        # Mock configuration
        self.config = {
            'edge_node': {'id': 'EdgeNode_1', 'processing_power': 5},
            'satellite': {'api_url': 'http://localhost:5000/api/satellite'},
            'cross_chain': {'source_chain_url': 'http://localhost:5001/api/source',
                            'target_chain_url': 'http://localhost:5002/api/target'}
        }
        
        # Initialize the STSPProtocol with mocked components
        self.protocol = STSPProtocol(self.config)
        self.protocol.edge_node = MockEdgeNode.return_value
        self.protocol.data_processor = MockDataProcessor.return_value
        self.protocol.edge_communication = MockEdgeCommunication.return_value
        self.protocol.satellite_manager = MockSatelliteManager.return_value
        self.protocol.quantum_time_transfer = MockQuantumTimeTransfer.return_value
        self.protocol.cross_chain_bridge = MockCrossChainBridge.return_value

    @patch('stsp.stsp_protocol.STSPProtocol.collect_sensor_data')
    def test_run_protocol(self, mock_collect_sensor_data):
        # Mock the return value of collect_sensor_data
        mock_collect_sensor_data.return_value = [10, 20, 30]

        # Mock the processing of data
        self.protocol.data_processor.process_data.return_value = [0.1, 0.2, 0.3]

        # Mock the satellite communication
        self.protocol.edge_communication.send_data_to_satellite.return_value = {"status": "success"}
        self.protocol.edge_communication.receive_data_from_satellite.return_value = {"timestamp": 1234567890}

        # Mock the quantum time transfer
        self.protocol.quantum_time_transfer.transfer_time.return_value = 1234567890
        self.protocol.quantum_time_transfer.synchronize_time.return_value = 1234567890

        # Mock the cross-chain data transfer
        self.protocol.cross_chain_bridge.transfer_data.return_value = {"status": "success"}

        # Run the protocol
        self.protocol.run()

        # Assertions
        self.protocol.edge_communication.send_data_to_satellite.assert_called_once()
        self.protocol.edge_communication.receive_data_from_satellite.assert_called_once()
        self.protocol.quantum_time_transfer.transfer_time.assert_called_once()
        self.protocol.quantum_time_transfer.synchronize_time.assert_called_once()
        self.protocol.cross_chain_bridge.transfer_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()
