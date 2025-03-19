# api/__init__.py

"""
API Module

This module provides a RESTful API for interacting with machine learning models
and IoT devices.
"""

from .app import create_app

__all__ = [
    "create_app"  # Function to create the Flask application
]
