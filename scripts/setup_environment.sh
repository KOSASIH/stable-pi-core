#!/bin/bash

# Environment setup script for the project

# Update and install necessary packages
echo "Updating package list..."
sudo apt-get update

echo "Installing Python and pip..."
sudo apt-get install -y python3 python3-pip

echo "Installing Node.js and npm..."
sudo apt-get install -y nodejs npm

# Install Brownie
echo "Installing Brownie..."
pip3 install eth-brownie

# Install Flask
echo "Installing Flask..."
pip3 install Flask

# Install other dependencies
echo "Installing additional dependencies..."
pip3 install web3 pytest

# Create a virtual environment (optional)
echo "Creating a virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Environment setup completed successfully!"
