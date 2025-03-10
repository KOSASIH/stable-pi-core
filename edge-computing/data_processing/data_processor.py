import paho.mqtt.client as mqtt
import yaml
import json
import logging
from data_processing.analytics.anomaly_detection import detect_anomaly

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

# Callback function for when a message is received
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        logging.info("Received data: %s", data)

        # Process the data (e.g., detect anomalies)
        if detect_anomaly(data):
            logging.warning("Anomaly detected in data: %s", data)
            # Here you can add code to handle the anomaly (e.g., send alert)

        # Log the processed data
        log_processed_data(data)

    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from message: %s", msg.payload)
    except Exception as e:
        logging.error("An error occurred while processing data: %s", e)

def log_processed_data(data):
    """
    Log the processed data to a file or database.
    
    Parameters:
        data (dict): The processed sensor data.
    """
    with open('processed_data.log', 'a') as log_file:
        log_file.write(json.dumps(data) + '\n')
    logging.info("Processed data logged: %s", data)

# Create an MQTT client
client = mqtt.Client(client_id)
client.on_message = on_message

# Connect to the MQTT broker
try:
    client.connect(broker_host, broker_port, keepalive=60)
except Exception as e:
    logging.error("Failed to connect to MQTT broker: %s", e)
    exit(1)

# Subscribe to the data collection topic
client.subscribe(topic)

# Start the loop
client.loop_forever()
