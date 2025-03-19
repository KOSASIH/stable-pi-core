# Arduino IoT Device Integration

This project demonstrates how to integrate an Arduino device with an MQTT broker for IoT applications. The Arduino will connect to a WiFi network, publish sensor data (temperature and humidity), and subscribe to commands from the MQTT broker.

## Table of Contents

- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Code Overview](#code-overview)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Requirements

- **Hardware:**
  - Arduino board (e.g., Arduino Uno, ESP32, etc.)
  - WiFi module (if using Arduino Uno, e.g., ESP8266)
  
- **Software:**
  - Arduino IDE
  - Libraries:
    - [PubSubClient](https://pubsubclient.knolleary.net/) for MQTT communication
    - [WiFi](https://www.arduino.cc/en/Reference/WiFi) for WiFi connectivity

## Setup Instructions

1. **Install Arduino IDE:**
   - Download and install the Arduino IDE from the [official website](https://www.arduino.cc/en/software).

2. **Install Required Libraries:**
   - Open the Arduino IDE.
   - Go to **Sketch** > **Include Library** > **Manage Libraries**.
   - Search for and install the **PubSubClient** library.

3. **Connect Your Arduino:**
   - Connect your Arduino board to your computer using a USB cable.

4. **Configure WiFi and MQTT Settings:**
   - Open the `arduino_code.ino` file in the Arduino IDE.
   - Replace the following placeholders with your actual credentials:
     - `your_SSID`: Your WiFi network name.
     - `your_PASSWORD`: Your WiFi password.
     - `mqtt.example.com`: Your MQTT broker address.
     - `your_username`: Your MQTT username (if required).
     - `your_password`: Your MQTT password (if required).
     - `device123`: A unique ID for your IoT device.

5. **Upload the Code:**
   - Select the correct board and port in the Arduino IDE.
   - Click the upload button to upload the code to your Arduino board.

## Code Overview

The `arduino_code.ino` file contains the following key components:

- **WiFi Connection:** The Arduino connects to the specified WiFi network.
- **MQTT Client:** The Arduino connects to the MQTT broker and subscribes to a commands topic.
- **Data Publishing:** The Arduino simulates temperature and humidity readings and publishes this data to the MQTT broker every 5 seconds.
- **Command Handling:** The Arduino listens for commands sent to its subscribed topic and can execute actions based on those commands.

## Usage

1. **Monitor Serial Output:**
   - Open the Serial Monitor in the Arduino IDE to view connection status and published data.

2. **Testing the MQTT Integration:**
   - Use an MQTT client (e.g., MQTT.fx, MQTT Explorer) to subscribe to the topics:
     - For published data: `iot/devices/device123/data`
     - For commands: `iot/devices/device123/commands`
   - You can send commands to the Arduino by publishing messages to the commands topic.

## Troubleshooting

- **Connection Issues:**
  - Ensure that your WiFi credentials are correct.
  - Check that the MQTT broker address is reachable from your network.

- **Library Errors:**
  - Make sure the required libraries are installed correctly in the Arduino IDE.

- **Serial Monitor:**
  - If you do not see any output in the Serial Monitor, ensure that the correct baud rate (115200) is set.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
