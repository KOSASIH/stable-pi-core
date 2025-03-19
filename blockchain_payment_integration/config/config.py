import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    """Base configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    API_VERSION = 'v1'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    COINBASE_API_KEY = os.getenv('COINBASE_API_KEY', 'your_coinbase_api_key')
    COINBASE_API_URL = 'https://api.commerce.coinbase.com/charges'
    BITPAY_API_KEY = os.getenv('BITPAY_API_KEY', 'your_bitpay_api_key')
    BITPAY_API_URL = 'https://bitpay.com/api/invoice'
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

class ProductionConfig(Config):
    """Production configuration."""
    COINBASE_API_KEY = os.getenv('COINBASE_API_KEY')
    COINBASE_API_URL = 'https://api.commerce.coinbase.com/charges'
    BITPAY_API_KEY = os.getenv('BITPAY_API_KEY')
    BITPAY_API_URL = 'https://bitpay.com/api/invoice'
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Configuration selection based on environment variable
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

# Set the default configuration
current_config = config[os.getenv('FLASK_ENV', 'development')]

def validate_config():
    """Validate required configuration settings."""
    required_keys = ['COINBASE_API_KEY', 'BITPAY_API_KEY']
    for key in required_keys:
        if not os.getenv(key):
            raise ValueError(f'Missing required environment variable: {key}')

# Validate the configuration on startup
validate_config()
