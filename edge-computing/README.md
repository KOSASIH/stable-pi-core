# Edge Computing Project: Stable-Pi-Core

## Overview

The **Stable-Pi-Core** project is an advanced edge computing solution designed for real-time data collection, processing, and analysis from IoT devices. This project leverages MQTT and CoAP protocols for efficient communication, enabling seamless integration with various sensors and devices. The architecture supports anomaly detection, pattern recognition, and data analytics, making it suitable for applications in smart homes, industrial automation, and environmental monitoring.

## Features

- **Data Collection**: Collects data from multiple sensors (temperature, humidity, etc.) using MQTT and CoAP protocols.
- **Data Processing**: Implements real-time data processing with anomaly detection and pattern recognition capabilities.
- **Communication**: Supports MQTT for lightweight messaging and CoAP for constrained environments.
- **Logging**: Comprehensive logging for monitoring and debugging.
- **Configuration Management**: Easy-to-manage configuration files for MQTT and CoAP settings.

## Architecture

```
stable-pi-core/
│
├── edge-computing/
│   ├── config/
│   │   ├── edge-config.yaml
│   │   └── mqtt-config.yaml
│   ├── data-processing/
│   │   ├── analytics/
│   │   │   ├── anomaly-detection.py
│   │   │   └── pattern-recognition.py
│   │   ├── data-collector.py
│   │   └── data-processor.py
│   ├── communication/
│   │   ├── coap-client.py
│   │   └── mqtt-client.py
│   ├── tests/
│   │   ├── test_communication.py
│   │   └── test_data_processing.py
│   └── README.md
└── main.py
```

## Installation

### Prerequisites

- Python 3.7 or higher
- Required Python packages:
  - `paho-mqtt`
  - `aiocoap`
  - `numpy`
  - `scikit-learn`
  - `PyYAML`
  - `unittest` (for testing)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd stable-pi-core/edge-computing
   ```

2. Install the required packages:

   ```bash
   pip install paho-mqtt aiocoap numpy scikit-learn PyYAML
   ```

3. Configure the MQTT and CoAP settings in the `config` directory:
   - Update `mqtt-config.yaml` with your MQTT broker details.
   - Create or update `coap-config.yaml` with your CoAP server details.

## Usage

### Data Collection

To start collecting data from sensors, run the data collector:

```bash
python data-processing/data-collector.py
```

### Data Processing

To process the collected data and detect anomalies, run the data processor:

```bash
python data-processing/data-processor.py
```

### Communication

To communicate with the MQTT broker, run the MQTT client:

```bash
python communication/mqtt-client.py
```

To send requests to a CoAP server, run the CoAP client:

```bash
python communication/coap-client.py
```

### Testing

To run the unit tests for data processing and communication modules, execute:

```bash
python -m unittest discover -s tests
```

## Configuration Files

### `edge-config.yaml`

Contains settings for edge devices, including data collection intervals and processing parameters.

### `mqtt-config.yaml`

Defines the MQTT broker settings, including host, port, topics, and QoS levels.

### `coap-config.yaml`

Specifies the CoAP server address and resource path.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For any inquiries, please contact [KOSASIH](https://github.com/KOSASIH).
