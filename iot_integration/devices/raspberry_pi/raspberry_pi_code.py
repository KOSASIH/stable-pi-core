import paho.mqtt.client as mqtt
import logging
import json
import os
import random
import time
import board
import adafruit_dht

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT Configuration
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt.example.com")  # Replace with your MQTT broker address
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))                # Default MQTT port
DEVICE_ID = os.getenv("DEVICE_ID", "raspberry_pi_device")    # Unique ID for the IoT device

# Topics
PUBLISH_TOPIC = f"iot/devices/{DEVICE_ID}/data"               # Topic for publishing data
SUBSCRIBE_TOPIC = f"iot/devices/{DEVICE_ID}/commands"        # Topic for subscribing to commands

# Initialize DHT sensor (using GPIO pin 4)
dht_device = adafruit_dht.DHT22(board.D4)

# Create MQTT client instance
mqtt_client = mqtt.Client()

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected to MQTT Broker: {MQTT_BROKER} with result code {rc}")
    client.subscribe(SUBSCRIBE_TOPIC)  # Subscribe to commands topic

# Callback when a message is received from the server
def on_message(client, userdata, msg):
    logging.info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    # Here you can add logic to handle the received message

# Function to connect to the MQTT broker
def connect_mqtt():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()  # Start the loop to process network traffic

# Function to publish sensor data
def publish_data(temperature, humidity):
    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "device_id": DEVICE_ID
    }
    mqtt_client.publish(PUBLISH_TOPIC, json.dumps(payload))
    logging.info(f"Published data: {payload}")

def main():
    connect_mqtt()
    try:
        while True:
            try:
                # Read temperature and humidity from the DHT sensor
                temperature = dht_device.temperature
                humidity = dht_device.humidity

                if temperature is not None and humidity is not None:
                    publish_data(temperature, humidity)
                else:
                    logging.warning("Failed to retrieve data from the sensor.")

            except Exception as e:
                logging.error(f"Error reading from DHT sensor: {e}")

            time.sleep(5)  # Publish data every 5 seconds

    except KeyboardInterrupt:
        logging.info("Disconnecting from MQTT Broker...")
        mqtt_client.loop_stop()  # Stop the loop
        mqtt_client.disconnect()  # Disconnect from the broker
        logging.info("Disconnected from MQTT Broker.")

if __name__ == "__main__":
    main()
