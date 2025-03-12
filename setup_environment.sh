#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to print messages
function print_message() {
    echo "========================================"
    echo "$1"
    echo "========================================"
}

# Update package lists
print_message "Updating package lists..."
sudo apt-get update -y

# Install Node.js and npm
print_message "Installing Node.js and npm..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install global npm packages
print_message "Installing global npm packages..."
npm install -g nodemon eslint prettier

# Install Docker (if not installed)
if ! command -v docker &> /dev/null; then
    print_message "Installing Docker..."
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
    sudo apt-get update -y
    sudo apt-get install -y docker-ce
else
    print_message "Docker is already installed."
fi

# Install Docker Compose (if not installed)
if ! command -v docker-compose &> /dev/null; then
    print_message "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    print_message "Docker Compose is already installed."
fi

# Clone the stable-pi-core repository (if not already cloned)
if [ ! -d "stable-pi-core" ]; then
    print_message "Cloning stable-pi-core repository..."
    git clone https://github.com/yourusername/stable-pi-core.git
fi

# Navigate to the project directory
cd stable-pi-core

# Install project dependencies
print_message "Installing project dependencies..."
npm install

# Create a .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_message "Creating .env file..."
    echo "NODE_ENV=development" > .env
    echo "PORT=3000" >> .env
    echo "DB_URI=mongodb://localhost:27017/stable-pi" >> .env
    echo "JWT_SECRET=your_jwt_secret" >> .env
fi

print_message "Development environment setup complete!"
