import paho.mqtt.client as mqtt
import time
import random
import yaml
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config/mqtt-config.yaml', 'r') as file:
    mqtt_config = yaml.safe_load(file)

# MQTT settings
broker_host = mqtt_config['mqtt']['broker']['host']
broker_port = mqtt_config['mqtt']['broker']['port']
client_id = mqtt_config['mqtt']['broker']['client_id']
topic = mqtt_config['mqtt']['topics']['data_collection']
data_collection_interval = mqtt_config['mqtt'].get('data_collection_interval', 5)  # Default to 5 seconds

# Callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    logging.info("Connected to MQTT broker with result code: %s", str(rc))

# Create an MQTT client
client = mqtt.Client(client_id)
client.on_connect = on_connect

# Connect to the MQTT broker
try:
    client.connect(broker_host, broker_port, keepalive=60)
except Exception as e:
    logging.error("Failed to connect to MQTT broker: %s", e)
    exit(1)

# Start the loop
client.loop_start()

try:
    while True:
        # Simulate sensor data collection
        sensor_data = {
            'sensor_id': client_id,  # Unique identifier for the sensor
            'temperature': round(random.uniform(20.0, 30.0), 2),  # Simulated temperature
            'humidity': round(random.uniform(30.0, 70.0), 2),      # Simulated humidity
            'timestamp': time.time()  # Current timestamp
        }
        
        # Publish the data to the MQTT broker
        client.publish(topic, json.dumps(sensor_data))
        logging.info("Published data: %s to topic: %s", sensor_data, topic)
        
        # Wait for the specified interval
        time.sleep(data_collection_interval)  # Collect data based on the configured interval

except KeyboardInterrupt:
    logging.info("Data collection stopped by user.")

except Exception as e:
    logging.error("An error occurred: %s", e)

finally:
    client.loop_stop()
    client.disconnect()
    logging.info("Disconnected from MQTT broker.")
