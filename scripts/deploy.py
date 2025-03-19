import os
import subprocess
import logging
import sys
import time
import json
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Service:
    def __init__(self, name, script, health_check_url=None):
        self.name = name
        self.script = script
        self.health_check_url = health_check_url
        self.process = None

    def start(self):
        """Start the service using subprocess."""
        try:
            logging.info(f"Starting {self.name}...")
            self.process = subprocess.Popen(
                ["python", self.script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(2)  # Wait for the service to start
            logging.info(f"{self.name} started successfully.")
        except Exception as e:
            logging.error(f"Failed to start {self.name}: {e}")

    def check_health(self):
        """Check if the service is healthy."""
        if self.health_check_url:
            try:
                response = requests.get(self.health_check_url)
                if response.status_code == 200:
                    logging.info(f"{self.name} is healthy.")
                    return True
                else:
                    logging.warning(f"{self.name} health check failed with status code: {response.status_code}")
                    return False
            except requests.RequestException as e:
                logging.error(f"Health check for {self.name} failed: {e}")
                return False
        else:
            logging.info(f"No health check URL provided for {self.name}. Assuming healthy.")
            return True

    def stop(self):
        """Stop the service gracefully."""
        if self.process:
            logging.info(f"Stopping {self.name}...")
            self.process.terminate()
            self.process.wait()
            logging.info(f"{self.name} stopped successfully.")

def load_services(config_file='services_config.json'):
    """Load services from a configuration file."""
    if not os.path.exists(config_file):
        logging.error(f"Configuration file {config_file} not found.")
        sys.exit(1)

    with open(config_file, 'r') as file:
        services_config = json.load(file)

    services = []
    for service in services_config:
        services.append(Service(
            name=service['name'],
            script=service['script'],
            health_check_url=service.get('health_check_url')
        ))
    return services

def deploy_blockchain_network():
    """Deploy the blockchain network components."""
    logging.info("Starting deployment of the blockchain network...")

    services = load_services()

    for service in services:
        service.start()

    # Check health of all services
    for service in services:
        if not service.check_health():
            logging.error(f"{service.name} is not healthy!")
        else:
            logging.info(f"{service.name} is running smoothly.")

    logging.info("Deployment of the blockchain network completed.")

    # Graceful shutdown on exit
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down services...")
        for service in services:
            service.stop()
        logging.info("All services have been shut down.")

if __name__ == "__main__":
    deploy_blockchain_network()
