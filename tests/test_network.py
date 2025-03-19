import unittest
from unittest.mock import patch, MagicMock
from network.p2p import P2PNetwork

class TestP2PNetwork(unittest.TestCase):
    def setUp(self):
        """Set up a new P2P network for testing."""
        self.p2p_network = P2PNetwork(host='127.0.0.1', port=5000)
        self.p2p_network.start()

    def test_accept_connections(self):
        """Test accepting connections from peers."""
        # Simulate a peer connection
        with patch('socket.socket.accept', return_value=(MagicMock(), ('127.0.0.1', 5001))):
            self.p2p_network.accept_connections()
            self.assertIn(('127.0.0.1', 5001), self.p2p_network.peers)

    def test_send_message(self):
        """Test sending a message to a peer."""
        peer_address = ('127.0.0.1', 5001)
        self.p2p_network.peers.add(peer_address)

        with patch('socket.socket.connect'), patch('socket.socket.sendall') as mock_send:
            self.p2p_network.send_message(peer_address, {"type": "test", "content": "Hello, World!"})
            mock_send.assert_called_once()

    def test_process_message(self):
        """Test processing an incoming message."""
        message = {"type": "test", "content": "Hello, World!"}
        with patch('logging.info') as mock_log:
            self.p2p_network.process_message(message)
            mock_log.assert_called_with(f"Received message: {message}")

    def test_handle_peer(self):
        """Test handling communication with a connected peer."""
        mock_client_socket = MagicMock()
        mock_client_socket.recv.return_value = b'{"type": "test", "content": "Hello, World!"}'
        
        with patch('logging.info') as mock_log:
            self.p2p_network.handle_peer(mock_client_socket)
            mock_log.assert_called_with("Received message: {'type': 'test', 'content': 'Hello, World!'}")

    def test_broadcast(self):
        """Test broadcasting a message to all peers."""
        peer1 = ('127.0.0.1', 5001)
        peer2 = ('127.0.0.1', 5002)
        self.p2p_network.peers.add(peer1)
        self.p2p_network.peers.add(peer2)

        with patch('socket.socket.sendto') as mock_send:
            self.p2p_network.broadcast({"type": "broadcast", "content": "Hello, Peers!"})
            self.assertEqual(mock_send.call_count, 2)  # Should send to both peers

if __name__ == '__main__':
    unittest.main()
