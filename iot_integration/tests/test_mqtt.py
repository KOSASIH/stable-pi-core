import unittest
from unittest.mock import patch, MagicMock
from mqtt_client import mqtt_client  # Assuming your MQTT client is in mqtt_client.py

class TestMQTTClient(unittest.TestCase):
    @patch('mqtt_client.paho.mqtt.client.Client')
    def test_connect(self, mock_client):
        mqtt_client.connect()
        mock_client.assert_called_once()

    @patch('mqtt_client.paho.mqtt.client.Client.publish')
    def test_publish_data(self, mock_publish):
        mqtt_client.publish_data('iot/devices/device123/data', {'temperature': 22.5})
        mock_publish.assert_called_once_with('iot/devices/device123/data', '{"temperature": 22.5}')

    @patch('mqtt_client.paho.mqtt.client.Client.subscribe')
    def test_subscribe(self, mock_subscribe):
        mqtt_client.subscribe('iot/devices/device123/commands')
        mock_subscribe.assert_called_once_with('iot/devices/device123/commands')

if __name__ == '__main__':
    unittest.main()
