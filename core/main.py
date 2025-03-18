# core/main.py

import logging
import sys
import time
from pqpn.utils import load_config
from pqpn.pqpn_manager import PQPNManager

# Configure logging for the core application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main entry point for the stable-pi-core project.
    """
    logger.info("Starting the stable-pi-core project...")

    # Load configuration
    config_file = "pqpn/pqpn_config.yaml"
    try:
        config = load_config(config_file)
    except FileNotFoundError:
        logger.error("Configuration file not found: %s", config_file)
        sys.exit(1)
    except Exception as e:
        logger.error("Failed to load configuration: %s", e)
        sys.exit(1)

    # Initialize the PQPN Manager
    try:
        pqpn_manager = PQPNManager(config)
        logger.info("PQPN Manager initialized successfully.")
    except Exception as e:
        logger.error("Failed to initialize PQPN Manager: %s", e)
        sys.exit(1)

    try:
        # Start data transmission
        logger.info("Starting data transmission...")
        pqpn_manager.start_data_transmission()
        logger.info("Data transmission started successfully.")

        # Run quantum AI tasks
        logger.info("Running Quantum AI tasks...")
        pqpn_manager.run_quantum_ai_tasks()
        logger.info("Quantum AI tasks completed successfully.")

    except Exception as e:
        logger.error("An error occurred during execution: %s", e)
    finally:
        # Ensure a graceful shutdown
        logger.info("Shutting down PQPN Manager...")
        pqpn_manager.shutdown()
        logger.info("Shutdown complete. Exiting the stable-pi-core project.")

if __name__ == "__main__":
    main()
