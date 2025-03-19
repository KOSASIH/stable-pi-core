# src/neuromorphic_analytics/__init__.py

"""
Neuromorphic Analytics Module for Stable Pi Core
This module implements the Neuromorphic Predictive Analytics Engine (NPAE),
which utilizes neuromorphic computing principles to process data from Market Analysis,
Quantum-AI, and IoT in real-time with maximum efficiency.

Key Components:
- npae.py: Implementation of the Neuromorphic Predictive Analytics Engine.
- data_pipeline.py: Data processing pipeline for NPAE.
- model.py: Spiking neural network model for predictive analytics.
- utils.py: Utility functions for NPAE.
"""

from .npae import NeuromorphicPredictiveAnalyticsEngine
from .data_pipeline import DataPipeline
from .model import SpikingNeuralNetworkModel
from .utils import preprocess_data, evaluate_model
