# dmec/communication.py

import paho.mqtt.client as mqtt
import logging
from .config import Config

class Communication:
    def __init__(self):
        self.client = mqtt.Client()
        self.broker_url = Config.DEFAULTS["MQTT_BROKER_URL"]
        self.topic = Config.DEFAULTS["MQTT_TOPIC"]
        self.connected = False

        # Set up MQTT callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log

        logging.info("Communication module initialized.")

    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        self.connected = True
        logging.info(f"Connected to MQTT broker: {self.broker_url} with result code: {rc}")
        self.client.subscribe(self.topic)  # Subscribe to the topic

    def on_message(self, client, userdata, msg):
        """Callback for when a message is received from the broker."""
        logging.info(f"Message received on topic {msg.topic}: {msg.payload.decode()}")

    def on_log(self, client, userdata, level, buf):
        """Callback for logging MQTT events."""
        logging.debug(f"MQTT log: {buf}")

    def connect(self):
        """Connect to the MQTT broker."""
        try:
            self.client.connect(self.broker_url)
            self.client.loop_start()  # Start the loop to process network traffic
            logging.info("Attempting to connect to the MQTT broker...")
        except Exception as e:
            logging.error(f"Failed to connect to MQTT broker: {e}")

    def publish(self, topic, message):
        """
        Publish a message to the specified topic.
        :param topic: The topic to publish to.
        :param message: The message to publish.
        """
        if self.connected:
            try:
                self.client.publish(topic, message)
                logging.info(f"Published message to {topic}: {message}")
            except Exception as e:
                logging.error(f"Failed to publish message: {e}")
        else:
            logging.warning("Cannot publish message, not connected to the broker.")

    def start(self):
        """Start the communication process."""
        self.connect()

    def stop(self):
        """Stop the communication process and disconnect from the broker."""
        if self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            logging.info("Disconnected from MQTT broker.")
        else:
            logging.warning("Not connected to any broker.")
