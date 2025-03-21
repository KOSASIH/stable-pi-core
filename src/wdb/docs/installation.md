# Installation Guide for Wormhole Data Bridge (WDB)

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8 or higher**: You can download it from [python.org](https://www.python.org/downloads/).
- **Node.js**: Required for running an Ethereum node. Download it from [nodejs.org](https://nodejs.org/).
- **Brownie**: A Python-based development framework for Ethereum smart contracts. It can be installed via pip.
- **Web3.py**: A Python library for interacting with Ethereum.

## Step 1: Clone the Repository

Clone the WDB repository from GitHub:

```bash
git clone https://github.com/KOSASIH/stable-pi-core.git
cd stable-pi-core/src/wdb
```

## Step 2: Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

## Step 3: Install Required Packages

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### Required Packages

Ensure the following packages are included in your `requirements.txt`:

```
fastapi
uvicorn
web3
brownie
```

## Step 4: Install Brownie

If you haven't installed Brownie yet, you can do so with the following command:

```bash
pip install eth-brownie
```

## Step 5: Start an Ethereum Node

You can use Ganache or any Ethereum node provider. If using Ganache, start it and ensure it runs on `http://127.0.0.1:8545`.

### Using Ganache

1. Download and install Ganache from [trufflesuite.com/ganache](https://www.trufflesuite.com/ganache).
2. Start Ganache and create a new workspace.

## Step 6: Deploy Smart Contracts

Navigate to the directory containing your Brownie project and deploy the smart contracts:

```bash
brownie run scripts/deploy.py
```

Make sure to replace `scripts/deploy.py` with the actual path to your deployment script.

## Step 7: Run the API

You can run the FastAPI application using the following command:

```bash
python -m wdb.api.api
```

The API will be available at `http://127.0.0.1:8000`.

## Step 8: Access the API Documentation

Once the API is running, you can access the interactive API documentation at:

```
http://127.0.0.1:8000/docs
```

## Conclusion

You are now ready to use the Wormhole Data Bridge! Follow the usage guide to learn how to interact with the API and utilize its features.
