import json
import logging
import paho.mqtt.client as mqtt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IoTCommunication:
    def __init__(self, broker, port, device_id):
        self.broker = broker
        self.port = port
        self.device_id = device_id
        self.client = mqtt.Client(device_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        """Connect to the MQTT broker."""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()  # Start the loop to process network traffic
            logging.info(f"Connected to MQTT Broker: {self.broker}")
        except Exception as e:
            logging.error(f"Failed to connect to MQTT Broker: {e}")

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        logging.info(f"Connected with result code {rc}")
        # Subscribe to the commands topic for this device
        client.subscribe(f"iot/devices/{self.device_id}/commands")

    def on_message(self, client, userdata, msg):
        """Callback for when a message is received from the broker."""
        logging.info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
        # Handle the received message
        self.handle_message(msg.topic, msg.payload)

    def handle_message(self, topic, payload):
        """Handle incoming messages based on the topic."""
        try:
            data = json.loads(payload)
            # Implement your message handling logic here
            logging.info(f"Handling message: {data}")
            # Example: Execute a command based on the message
            if topic == f"iot/devices/{self.device_id}/commands":
                self.execute_command(data)
        except json.JSONDecodeError:
            logging.error("Failed to decode JSON payload.")

    def execute_command(self, command):
        """Execute a command received from the MQTT broker."""
        # Implement command execution logic here
        logging.info(f"Executing command: {command}")

    def publish_data(self, topic, data):
        """Publish data to the specified MQTT topic."""
        try:
            payload = json.dumps(data)
            self.client.publish(topic, payload)
            logging.info(f"Published data: {data} to topic: {topic}")
        except Exception as e:
            logging.error(f"Error publishing data: {e}")

    def disconnect(self):
        """Disconnect from the MQTT broker."""
        self.client.loop_stop()  # Stop the loop
        self.client.disconnect()  # Disconnect from the broker
        logging.info("Disconnected from MQTT Broker.")

if __name__ == "__main__":
    # Example usage
    broker = "mqtt.example.com"  # Replace with your MQTT broker address
    port = 1883                   # Default MQTT port
    device_id = "device123"       # Unique ID for the IoT device

    communication = IoTCommunication(broker, port, device_id)
    communication.connect()

    try:
        while True:
            # Simulate publishing data
            data = {
                "temperature": 22.5,
                "humidity": 60,
                "device_id": device_id
            }
            communication.publish_data(f"iot/devices/{device_id}/data", data)
            time.sleep(5)  # Publish data every 5 seconds
    except KeyboardInterrupt:
        communication.disconnect()
