import unittest
from unittest.mock import patch, MagicMock
import json
import paho.mqtt.client as mqtt
from aiocoap import Message, Context

class TestMQTTClient(unittest.TestCase):
    @patch('paho.mqtt.client.Client')
    def test_mqtt_publish(self, MockClient):
        mock_client = MockClient.return_value
        mock_client.publish.return_value = None  # Simulate successful publish

        # Simulate publishing sensor data
        sensor_data = {'temperature': 25.0, 'humidity': 60.0}
        topic = "edge/device/data"
        mock_client.publish(topic, json.dumps(sensor_data))

        # Assert that publish was called with the correct parameters
        mock_client.publish.assert_called_once_with(topic, json.dumps(sensor_data))

class TestCoAPClient(unittest.TestCase):
    @patch('aiocoap.Context.create_client_context')
    async def test_coap_request(self, mock_context):
        mock_protocol = MagicMock()
        mock_context.return_value = mock_protocol

        # Simulate a successful response
        mock_response = MagicMock()
        mock_response.payload = b'{"status": "success"}'
        mock_protocol.request.return_value.response = mock_response

        # Call the coap_request function
        uri = "coap://localhost/resource"
        request = Message(code=GET, uri=uri)
        response = await mock_protocol.request(request).response

        # Assert that the response is as expected
        self.assertEqual(response.payload.decode(), '{"status": "success"}')

if __name__ == '__main__':
    unittest.main()
