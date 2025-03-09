# IoT Integration Project

This project demonstrates the integration of various IoT devices (such as Arduino and Raspberry Pi) with an MQTT broker and the Ethereum blockchain. The goal is to create a robust and scalable IoT system that allows devices to communicate, publish sensor data, and execute transactions on the blockchain.

## Table of Contents

- [Project Overview](#project-overview)
- [Components](#components)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Project Overview

The IoT Integration Project consists of the following key features:

- **Device Communication**: IoT devices communicate with each other and with a central MQTT broker.
- **Data Publishing**: Devices publish sensor data (e.g., temperature, humidity) to the MQTT broker.
- **Command Handling**: Devices can receive commands from the MQTT broker to perform specific actions.
- **Blockchain Transactions**: The system can create and send transactions to the Ethereum blockchain based on IoT data.

## Components

The project is organized into the following main components:

- **API**: A RESTful API for managing IoT transactions and data.
- **MQTT Client**: A client for connecting to the MQTT broker and handling communication.
- **Device Integrations**: Code for integrating various IoT devices, including:
  - Arduino
  - Raspberry Pi
- **Protocols**: Communication and transaction protocols for handling data and interactions.
- **Tests**: Unit tests for ensuring the functionality of the components.

## Requirements

- **Hardware**:
  - Arduino board (e.g., Arduino Uno, ESP32)
  - Raspberry Pi (any model with GPIO support)
  - DHT22 or DHT11 temperature and humidity sensor (for Raspberry Pi)
  
- **Software**:
  - Python 3.x
  - Flask (for the API)
  - Paho MQTT (for MQTT communication)
  - Web3.py (for Ethereum blockchain interaction)
  - Adafruit CircuitPython libraries (for sensor integration)

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd iot_integration
   ```

2. **Install Python Dependencies**:
   Create a virtual environment and install the required Python packages:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Set up the necessary environment variables for your MQTT broker and Ethereum node. You can create a `.env` file or export them directly in your terminal:
   ```bash
   export MQTT_BROKER="mqtt.example.com"
   export MQTT_PORT=1883
   export ETHEREUM_NODE="https://your.ethereum.node"
   export CONTRACT_ADDRESS="0xYourContractAddress"
   export PRIVATE_KEY="0xYourPrivateKey"
   ```

4. **Set Up Devices**:
   - Follow the setup instructions for the Arduino and Raspberry Pi integrations as detailed in their respective directories.

## Usage

1. **Start the API**:
   Run the IoT API server:
   ```bash
   python iot_api.py
   ```

2. **Start the MQTT Broker**:
   Ensure your MQTT broker is running. You can use a local broker like Mosquitto or a cloud-based broker.

3. **Run Device Code**:
   - Upload the Arduino code to your Arduino board.
   - Run the Raspberry Pi code to start publishing sensor data.

4. **Monitor Data**:
   Use an MQTT client (e.g., MQTT.fx, MQTT Explorer) to subscribe to the topics and monitor the published data.

## Testing

To run the unit tests for the project, use the following command:
```bash
python -m unittest discover -s tests
```

This will execute all the tests in the `tests` directory and report the results.

## Troubleshooting

- **Connection Issues**: Ensure that your MQTT broker is reachable and that the credentials are correct.
- **Sensor Errors**: Double-check the wiring and configuration of your sensors.
- **API Errors**: Check the API logs for any error messages and ensure that the server is running.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
