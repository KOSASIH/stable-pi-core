import os
import json

class Config:
    """Configuration management class."""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from a JSON file."""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file {self.config_file} not found.")
        
        with open(self.config_file, 'r') as file:
            config = json.load(file)
        
        # Override with environment variables
        self.override_with_env(config)
        return config

    def override_with_env(self, config):
        """Override configuration values with environment variables."""
        for key, value in config.items():
            env_value = os.getenv(key.upper())
            if env_value is not None:
                config[key] = env_value

    def get(self, key, default=None):
        """Get a configuration value by key."""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default

    def reload(self):
        """Reload the configuration from the file."""
        self.config = self.load_config()

# Example usage
if __name__ == "__main__":
    config = Config()
    print(config.get('api_key', 'No API key found.'))  # Accessing a top-level key
    print(config.get('database.host', 'No host found.'))  # Accessing a nested key

    # Example of reloading the configuration
    config.reload()
    print("Configuration reloaded.")
