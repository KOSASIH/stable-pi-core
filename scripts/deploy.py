import os
import subprocess
import logging
import sys
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_service(service_name):
    """Start a service using subprocess."""
    try:
        logging.info(f"Starting {service_name}...")
        subprocess.Popen(["python", f"{service_name}.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)  # Wait for the service to start
        logging.info(f"{service_name} started successfully.")
    except Exception as e:
        logging.error(f"Failed to start {service_name}: {e}")

def check_service_health(service_name):
    """Check if a service is running."""
    # This is a placeholder for actual health check logic
    logging.info(f"Checking health of {service_name}...")
    # In a real scenario, you might ping the service or check a specific endpoint
    return True  # Assume the service is healthy for this example

def deploy_blockchain_network():
    """Deploy the blockchain network components."""
    logging.info("Starting deployment of the blockchain network...")

    services = ['node', 'network/p2p', 'wallet/wallet']

    for service in services:
        start_service(service)

    # Check health of all services
    for service in services:
        if not check_service_health(service):
            logging.error(f"{service} is not healthy!")
        else:
            logging.info(f"{service} is running smoothly.")

    logging.info("Deployment of the blockchain network completed.")

if __name__ == "__main__":
    deploy_blockchain_network()
