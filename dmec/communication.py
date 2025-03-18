# dmec/communication.py

import paho.mqtt.client as mqtt
from .config import Config

class Communication:
    def __init__(self):
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(Config.MQTT_BROKER_URL)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def start(self):
        self.connect()
        self.client.loop_start()
