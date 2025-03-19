import unittest
from unittest.mock import patch, MagicMock
from holographic_data_storage.ipfs_integration import IPFSIntegration

class TestIPFSIntegration(unittest.TestCase):
    def setUp(self):
        """Set up an IPFSIntegration instance for testing."""
        self.ipfs_integration = IPFSIntegration(ipfs_address='http://localhost:5001')

    @patch('holographic_data_storage.ipfs_integration.ipfshttpclient')
    def test_upload_data_success(self, mock_ipfs_client):
        """Test successful upload of data to IPFS."""
        mock_ipfs_client.connect.return_value.add_bytes.return_value = {'cid': 'QmTestCID'}
        
        data = b'Test data for IPFS upload.'
        cid = self.ipfs_integration.upload_data(data)
        
        self.assertEqual(cid, 'QmTestCID')
        mock_ipfs_client.connect.assert_called_once()
        mock_ipfs_client.connect.return_value.add_bytes.assert_called_once_with(data)

    @patch('holographic_data_storage.ipfs_integration.ipfshttpclient')
    def test_upload_data_failure(self, mock_ipfs_client):
        """Test failure of data upload to IPFS."""
        mock_ipfs_client.connect.return_value.add_bytes.side_effect = Exception("Upload failed")
        
        data = b'Test data for IPFS upload.'
        cid = self.ipfs_integration.upload_data(data)
        
        self.assertIsNone(cid)
        mock_ipfs_client.connect.assert_called_once()
        mock_ipfs_client.connect.return_value.add_bytes.assert_called_once_with(data)

    @patch('holographic_data_storage.ipfs_integration.ipfshttpclient')
    def test_retrieve_data_success(self, mock_ipfs_client):
        """Test successful retrieval of data from IPFS."""
        mock_ipfs_client.connect.return_value.cat.return_value = b'Test data from IPFS.'
        
        cid = 'QmTestCID'
        data = self.ipfs_integration.retrieve_data(cid)
        
        self.assertEqual(data, b'Test data from IPFS.')
        mock_ipfs_client.connect.assert_called_once()
        mock_ipfs_client.connect.return_value.cat.assert_called_once_with(cid)

    @patch('holographic_data_storage.ipfs_integration.ipfshttpclient')
    def test_retrieve_data_failure(self, mock_ipfs_client):
        """Test failure of data retrieval from IPFS."""
        mock_ipfs_client.connect.return_value.cat.side_effect = Exception("Retrieval failed")
        
        cid = 'QmTestCID'
        data = self.ipfs_integration.retrieve_data(cid)
        
        self.assertIsNone(data)
        mock_ipfs_client.connect.assert_called_once()
        mock_ipfs_client.connect.return_value.cat.assert_called_once_with(cid)

    @patch('holographic_data_storage.ipfs_integration.ipfshttpclient')
    def test_pin_data_success(self, mock_ipfs_client):
        """Test successful pinning of data to IPFS."""
        mock_ipfs_client.connect.return_value.pin.add.return_value = None
        
        cid = 'QmTestCID'
        success = self.ipfs_integration.pin_data(cid)
        
        self.assertTrue(success)
        mock_ipfs_client.connect.assert_called_once()
        mock_ipfs_client.connect.return_value.pin.add.assert_called_once_with(cid)

    @patch('holographic_data_storage.ipfs_integration.ipfshttpclient')
    def test_unpin_data_success(self, mock_ipfs_client):
        """Test successful unpinning of data from IPFS."""
        mock_ipfs_client.connect.return_value.pin.rm.return_value = None
        
        cid = 'QmTestCID'
        success = self.ipfs_integration.unpin_data(cid)
        
        self.assertTrue(success)
        mock_ipfs_client.connect.assert_called_once()
        mock_ipfs_client.connect.return_value.pin.rm.assert_called_once_with(cid)

if __name__ == "__main__":
    unittest.main()
