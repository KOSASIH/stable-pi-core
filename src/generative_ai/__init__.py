# src/generative_ai/__init__.py

"""
Generative AI Module for Stable Pi Core
This module contains functionalities for generative AI, including model handling,
data processing, feature generation, RPA integration, and DAO voting mechanisms.

Key Features:
- Text and image generation using OpenAI's models
- Data collection from external APIs
- Automated feature generation based on user input
- Integration with RPA tools for process automation
- DAO voting mechanism for community-driven feature approval
"""

import logging
import os

# Set up logging for the generative AI module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Importing necessary classes from the module
from .model import GenerativeAIModel
from .data_collection import DataCollector
from .feature_generation import FeatureGenerator
from .rpa_integration import RPAIntegration
from .dao_voting import DAOVoting

# Initialize the generative AI model
try:
    logger.info("Initializing Generative AI Model...")
    ai_model = GenerativeAIModel(model_type=os.getenv('AI_MODEL_TYPE', 'gpt-3.5-turbo'))
    logger.info("Generative AI Model initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Generative AI Model: {e}")

# Initialize the data collector
try:
    logger.info("Setting up Data Collector...")
    data_collector = DataCollector(api_url=os.getenv('DATA_API_URL', 'http://localhost:5000/data'))
    logger.info("Data Collector set up successfully.")
except Exception as e:
    logger.error(f"Failed to set up Data Collector: {e}")

# Initialize the feature generator
try:
    logger.info("Creating Feature Generator...")
    feature_generator = FeatureGenerator(ai_model)
    logger.info("Feature Generator created successfully.")
except Exception as e:
    logger.error(f"Failed to create Feature Generator: {e}")

# Initialize the RPA integration
try:
    logger.info("Setting up RPA Integration...")
    rpa_integration = RPAIntegration(rpa_tool=os.getenv('RPA_TOOL', 'dummy_rpa_tool'))
    logger.info("RPA Integration set up successfully.")
except Exception as e:
    logger.error(f"Failed to set up RPA Integration: {e}")

# Initialize the DAO voting system
try:
    logger.info("Initializing DAO Voting...")
    dao_voting = DAOVoting(voting_system=os.getenv('VOTING_SYSTEM', 'dummy_voting_system'))
    logger.info("DAO Voting initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize DAO Voting: {e}")

# Expose the initialized components for external access
__all__ = [
    'ai_model',
    'data_collector',
    'feature_generator',
    'rpa_integration',
    'dao_voting'
  ]
