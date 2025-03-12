import os
import logging
import json
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_directories(directories):
    """Create necessary directories for the blockchain project."""
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

def create_config_file(config):
    """Create a configuration file for the blockchain project."""
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
    logging.info("Configuration file created: config.json")

def parse_arguments():
    """Parse command-line arguments for setup configuration."""
    parser = argparse.ArgumentParser(description="Setup the blockchain project.")
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Network host address')
    parser.add_argument('--port', type=int, default=5000, help='Network port')
    parser.add_argument('--default_balance', type=float, default=1000.0, help='Default wallet balance')
    parser.add_argument('--difficulty', type=int, default=2, help='Mining difficulty')
    parser.add_argument('--mining_reward', type=float, default=50.0, help='Mining reward')
    return parser.parse_args()

if __name__ == "__main__":
    logging.info("Setting up the blockchain project...")
    args = parse_arguments()

    # Create necessary directories
    create_directories(['keys', 'logs', 'data', 'scripts', 'wallet', 'network', 'tests'])

    # Create configuration file with command-line arguments
    config = {
        "network": {
            "host": args.host,
            "port": args.port
        },
        "wallet": {
            "default_balance": args.default_balance
        },
        "blockchain": {
            "difficulty": args.difficulty,
            "mining_reward": args.mining_reward
        }
    }
    create_config_file(config)

    logging.info("Setup completed.")
