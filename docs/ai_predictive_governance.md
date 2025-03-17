# AI-Driven Predictive Governance Documentation

## Overview

The AI-Driven Predictive Governance module is part of the Stable Pi Core project, designed to enhance decision-making processes within Decentralized Autonomous Organizations (DAOs) by leveraging artificial intelligence. This module analyzes data from various sources, including on-chain and off-chain data, to provide proactive recommendations before voting begins.

## Features

- **Data Collection**: Collects on-chain and off-chain data relevant to governance decisions.
- **Data Preprocessing**: Cleans and normalizes the collected data to prepare it for analysis.
- **Predictive Modeling**: Utilizes machine learning models (e.g., LSTM) to forecast future trends and outcomes based on historical data.
- **Recommendation Generation**: Provides actionable recommendations based on model predictions.
- **Governance Dashboard**: A user-friendly interface for visualizing insights and recommendations.

## Installation

To use the AI-Driven Predictive Governance module, ensure you have the following dependencies installed:

```bash
pip install Flask pandas numpy tensorflow requests
```

## Usage

### 1. Data Collection

#### Creating a Data Collector

```python
from ai_predictive_governance.data_collection import DataCollector

on_chain_url = "http://localhost:8545/on_chain_data"
off_chain_sources = [
    "http://localhost:3000/off_chain_data_1",
    "http://localhost:3000/off_chain_data_2"
]
data_collector = DataCollector(on_chain_url, off_chain_sources)
```

#### Collecting Data

```python
on_chain_data, off_chain_data = data_collector.collect_data()
```

### 2. Data Preprocessing

#### Creating a Data Preprocessor

```python
from ai_predictive_governance.data_preprocessing import DataPreprocessor

raw_data = {
    "on_chain": on_chain_data,
    "off_chain": off_chain_data
}
data_preprocessor = DataPreprocessor(data=raw_data)
```

#### Preprocessing Data

```python
preprocessed_data = data_preprocessor.preprocess()
```

### 3. Predictive Modeling

#### Creating and Training a Predictive Model

```python
from ai_predictive_governance.model import PredictiveModel

input_shape = (1, 2)  # Example input shape
model = PredictiveModel(input_shape=input_shape)
model.train(preprocessed_data, target_column='target', epochs=50)
```

### 4. Generating Recommendations

#### Generating Recommendations

```python
from ai_predictive_governance.predictions import generate_recommendations

recommendations = generate_recommendations(model, preprocessed_data, target_column='target', num_recommendations=5)
```

### 5. Governance Dashboard

#### Creating and Running the Dashboard

```python
from ai_predictive_governance.governance_dashboard import GovernanceDashboard

dashboard = GovernanceDashboard(model)
dashboard.run()
```

## API Reference

### DataCollector Class

- **`__init__(on_chain_url: str, off_chain_sources: List[str])`**: Initializes a new DataCollector instance.
- **`collect_on_chain_data()`**: Collects on-chain data from the specified blockchain API.
- **`collect_off_chain_data()`**: Collects off-chain data from the specified sources.
- **`collect_data()`**: Collects both on-chain and off-chain data.

### DataPreprocessor Class

- **`__init__(data: Dict[str, Any])`**: Initializes a new DataPreprocessor instance with raw data.
- **`clean_data()`**: Cleans the collected data by removing duplicates and handling missing values.
- **`normalize_data(df: pd.DataFrame)`**: Normalizes numerical features in the DataFrame.
- **`preprocess()`**: Preprocesses the collected data by cleaning and normalizing it.

### PredictiveModel Class

- **`__init__(input_shape: tuple)`**: Initializes a new PredictiveModel instance with the specified input shape.
- **`train(data: pd.DataFrame, target_column: str, epochs: int)`**: Trains the model on the provided data.
- **`prepare_data(data: pd.DataFrame, target_column: str)`**: Prepares the data for LSTM training.
- **`evaluate(data: pd.DataFrame, target_column: str)`**: Evaluates the model on the provided data.

### GovernanceDashboard Class

- **`__init__(model: PredictiveModel)`**: Initializes a new GovernanceDashboard instance with the trained model.
- **`setup_routes()`**: Sets up the routes for the Flask application.
- **`run(host: str, port: int)`**: Runs the Flask application.

## Conclusion

The AI-Driven Predictive Governance module provides a robust framework for integrating AI into governance processes, enabling DAOs to make informed decisions based on predictive analytics. This documentation serves as a guide for developers to effectively utilize the module's capabilities in their projects. For further inquiries or contributions, please refer to the project's repository or contact the development team.
