# Raspberry Pi IoT Device Integration

This project demonstrates how to integrate a Raspberry Pi device with an MQTT broker for IoT applications. The Raspberry Pi will connect to a WiFi network, publish sensor data (temperature and humidity), and subscribe to commands.

## Table of Contents

- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Code Overview](#code-overview)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Requirements

- **Hardware:**
  - Raspberry Pi (any model with GPIO support)
  - DHT22 or DHT11 temperature and humidity sensor
  - Jumper wires for connections

- **Software:**
  - Raspbian OS or any compatible Linux distribution
  - Python 3.x
  - Libraries:
    - [paho-mqtt](https://pypi.org/project/paho-mqtt/) for MQTT communication
    - [adafruit-circuitpython-dht](https://pypi.org/project/adafruit-circuitpython-dht/) for reading DHT sensor data

## Setup Instructions

1. **Install Raspbian OS:**
   - Download and install Raspbian OS on your Raspberry Pi. Follow the instructions on the [official Raspberry Pi website](https://www.raspberrypi.org/software/).

2. **Update and Upgrade Packages:**
   - Open a terminal and run the following commands to update and upgrade your system:
     ```bash
     sudo apt update
     sudo apt upgrade
     ```

3. **Install Required Libraries:**
   - Install the required Python libraries using pip:
     ```bash
     sudo apt install python3-pip
     pip3 install paho-mqtt adafruit-circuitpython-dht
     ```

4. **Connect the DHT Sensor:**
   - Connect the DHT sensor to the Raspberry Pi:
     - **DHT22/DHT11 Pinout:**
       - VCC to 3.3V or 5V pin on Raspberry Pi
       - GND to Ground pin on Raspberry Pi
       - Data to GPIO pin (e.g., GPIO4)

5. **Configure MQTT Settings:**
   - Open the `raspberry_pi_code.py` file in a text editor.
   - Replace the following placeholders with your actual credentials:
     - `mqtt.example.com`: Your MQTT broker address.
     - `your_username`: Your MQTT username (if required).
     - `your_password`: Your MQTT password (if required).
     - `raspberry_pi_device`: A unique ID for your IoT device.

6. **Run the Code:**
   - Execute the `raspberry_pi_code.py` script to start the MQTT client:
     ```bash
     python3 raspberry_pi_code.py
     ```

## Code Overview

The `raspberry_pi_code.py` file contains the following key components:

- **WiFi Connection:** The Raspberry Pi connects to the specified WiFi network.
- **MQTT Client:** The Raspberry Pi connects to the MQTT broker and subscribes to a commands topic.
- **Data Publishing:** The Raspberry Pi reads temperature and humidity from the DHT sensor and publishes this data to the MQTT broker every 5 seconds.
- **Command Handling:** The Raspberry Pi listens for commands sent to its subscribed topic and can execute actions based on those commands.

## Usage

1. **Monitor Output:**
   - Open a terminal to view the output of the script, which will show connection status and published data.

2. **Testing the MQTT Integration:**
   - Use an MQTT client (e.g., MQTT.fx, MQTT Explorer) to subscribe to the topics:
     - For published data: `iot/devices/raspberry_pi_device/data`
     - For commands: `iot/devices/raspberry_pi_device/commands`
   - You can send commands to the Raspberry Pi by publishing messages to the commands topic.

## Troubleshooting

- **Connection Issues:**
  - Ensure that your WiFi credentials are correct.
  - Check that the MQTT broker address is reachable from your network.

- **Library Errors:**
  - Make sure the required libraries are installed correctly.

- **Sensor Wiring:**
  - Double-check the wiring of the DHT sensor to ensure it is connected properly.

- **Serial Output:**
  - If you do not see any output in the terminal, ensure that the correct Python version is being used (Python 3.x).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
