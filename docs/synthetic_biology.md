# Synthetic Biology Interface Documentation

## Overview

The Synthetic Biology Interface is a module within the Stable Pi Core project that facilitates interaction with biological systems through IoT integration and edge computing. It allows for the collection, processing, and logging of biosensor data to a blockchain, ensuring data integrity and traceability.

## Components

The `synthetic_biology` module consists of the following key components:

1. **Biosensor**: Classes and functions for managing biosensors, including data collection and status management.
2. **Edge Computing**: Functions for processing data at the edge, including data aggregation and analysis.
3. **Data Logging**: Functions for logging biosensor data to the blockchain.
4. **Smart Contracts**: Smart contracts for handling biosensor data on the blockchain.
5. **Utilities**: Utility functions for data validation, formatting, and logging.

## Installation

To use the Synthetic Biology Interface, ensure you have the following dependencies installed:

```bash
pip install requests web3 py-solc-x
```

## Usage

### 1. Biosensor Management

#### Creating a Biosensor

```python
from synthetic_biology.biosensor import Biosensor

# Create a new biosensor
biosensor = Biosensor(sensor_id="biosensor_001", sensor_type="DNA")
```

#### Collecting Data

```python
data = biosensor.collect_data()
print(data)
```

#### Activating/Deactivating the Biosensor

```python
biosensor.deactivate()  # Deactivate the biosensor
biosensor.activate()    # Activate the biosensor
```

### 2. Edge Computing

#### Processing Data

```python
from synthetic_biology.edge_computing import EdgeProcessor

# Create an EdgeProcessor instance
edge_processor = EdgeProcessor()

# Receive data from biosensors
edge_processor.receive_data(data)

# Process the data
processed_data = edge_processor.process_data()
print(processed_data)
```

### 3. Data Logging

#### Logging Data to Blockchain

```python
from synthetic_biology.data_logging import log_data_to_blockchain

sensor_id = "biosensor_001"
data = {
    "timestamp": "2025-03-17T12:00:00Z",
    "value": 42.0,
    "unit": "units"
}
blockchain_url = "http://localhost:8545"
api_key = "your_api_key"

response = log_data_to_blockchain(sensor_id, data, blockchain_url, api_key)
print(response)
```

### 4. Smart Contracts

#### Deploying and Interacting with Smart Contracts

```python
from synthetic_biology.smart_contracts import SmartContractManager

# Define your smart contract source code
contract_source = """
pragma solidity ^0.8.0;

contract BiosensorData {
    struct Data {
        string sensorId;
        string timestamp;
        uint value;
        string unit;
    }

    Data[] public dataEntries;

    function logData(string memory sensorId, string memory timestamp, uint value, string memory unit) public {
        dataEntries.push(Data(sensorId, timestamp, value, unit));
    }

    function getData(uint index) public view returns (Data memory) {
        return dataEntries[index];
    }
}
"""

# Create a SmartContractManager instance
manager = SmartContractManager(blockchain_url, contract_source)

# Deploy the smart contract
account = "your_account_address"
private_key = "your_private_key"
contract_address = manager.deploy_contract(account, private_key)
print(f"Contract deployed at: {contract_address}")
```

## API Reference

### Biosensor Class

- **`__init__(sensor_id: str, sensor_type: str)`**: Initializes a new biosensor instance.
- **`collect_data()`**: Collects data from the biosensor.
- **`deactivate()`**: Deactivates the biosensor.
- **`activate()`**: Activates the biosensor.
- **`get_status()`**: Returns the current status of the biosensor.
- **`to_json()`**: Converts the biosensor data to JSON format.

### EdgeProcessor Class

- **`__init__()`**: Initializes a new EdgeProcessor instance.
- **`receive_data(data: Dict[str, Any])`**: Receives data from a biosensor.
- **`aggregate_data()`**: Aggregates data from all received biosensor data.
- **`analyze_data()`**: Analyzes the received biosensor data for anomalies.
- **`clear_data()`**: Clears the stored sensor data after processing.
- **`process_data()`**: Processes the received data by aggregating and analyzing it.

### Data Logging Functions

- **`log_data_to_block chain(sensor_id: str, data: Dict[str, Any], blockchain_url: str, api_key: str) -> Dict[str, Any]**: Logs data from a biosensor to the blockchain and returns the response.

### SmartContractManager Class

- **`__init__(blockchain_url: str, contract_source: str)`**: Initializes a new SmartContractManager instance with the blockchain URL and smart contract source code.
- **`deploy_contract(account: str, private_key: str) -> str`**: Deploys the smart contract to the blockchain and returns the contract address.
- **`interact_with_contract(contract_address: str, method: str, *args)`**: Interacts with a deployed smart contract method.

## Conclusion

The Synthetic Biology Interface provides a robust framework for integrating biosensors with blockchain technology, enabling secure and traceable data logging. This documentation serves as a guide for developers to effectively utilize the module's capabilities in their projects. For further inquiries or contributions, please refer to the project's repository or contact the development team.
