#include <WiFi.h>
#include <PubSubClient.h>

// WiFi Configuration
const char* ssid = "your_SSID";          // Replace with your WiFi SSID
const char* password = "your_PASSWORD";  // Replace with your WiFi password

// MQTT Configuration
const char* mqtt_broker = "mqtt.example.com";  // Replace with your MQTT broker address
const int mqtt_port = 1883;                     // Default MQTT port
const char* mqtt_user = "your_username";        // MQTT username (if required)
const char* mqtt_password = "your_password";    // MQTT password (if required)
const char* device_id = "device123";            // Unique ID for the IoT device

// Topics
const char* publish_topic = "iot/devices/device123/data";  // Topic for publishing data
const char* subscribe_topic = "iot/devices/device123/commands";  // Topic for subscribing to commands

// Create WiFi and MQTT client instances
WiFiClient espClient;
PubSubClient mqttClient(espClient);

// Function to connect to WiFi
void connectWiFi() {
    Serial.print("Connecting to WiFi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("Connected to WiFi");
}

// Callback function for handling incoming messages
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived on topic: ");
    Serial.print(topic);
    Serial.print(". Message: ");
    String message;
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    Serial.println(message);
    // Here you can add logic to handle the received message
}

// Function to connect to the MQTT broker
void connectMQTT() {
    while (!mqttClient.connected()) {
        Serial.print("Connecting to MQTT...");
        if (mqttClient.connect(device_id, mqtt_user, mqtt_password)) {
            Serial.println("Connected to MQTT broker");
            mqttClient.subscribe(subscribe_topic);  // Subscribe to commands topic
        } else {
            Serial.print("Failed to connect, return code: ");
            Serial.print(mqttClient.state());
            delay(2000);
        }
    }
}

// Function to publish sensor data
void publishData(float temperature, float humidity) {
    String payload = String("{\"temperature\":") + temperature + ",\"humidity\":" + humidity + "}";
    mqttClient.publish(publish_topic, payload.c_str());
    Serial.print("Published data: ");
    Serial.println(payload);
}

void setup() {
    Serial.begin(115200);
    connectWiFi();
    mqttClient.setServer(mqtt_broker, mqtt_port);
    mqttClient.setCallback(callback);
}

void loop() {
    if (!mqttClient.connected()) {
        connectMQTT();
    }
    mqttClient.loop();

    // Simulate sensor data
    float temperature = random(20, 30);  // Simulated temperature
    float humidity = random(40, 60);      // Simulated humidity

    publishData(temperature, humidity);
    delay(5000);  // Publish data every 5 seconds
}
