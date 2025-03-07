# src/main/config.py

import os
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    uri: str
    username: str
    password: str

@dataclass
class QuantumConfig:
    backend: str
    shots: int

@dataclass
class AIConfig:
    model_path: str
    threshold: float

@dataclass
class AppConfig:
    debug: bool
    database: DatabaseConfig
    quantum: QuantumConfig
    ai: AIConfig

def load_config() -> AppConfig:
    """Load configuration from environment variables or defaults."""
    return AppConfig(
        debug=os.getenv("DEBUG", "True") == "True",
        database=DatabaseConfig(
            uri=os.getenv("DATABASE_URI", "sqlite:///arbitration.db"),
            username=os.getenv("DATABASE_USERNAME", "user"),
            password=os.getenv("DATABASE_PASSWORD", "password")
        ),
        quantum=QuantumConfig(
            backend=os.getenv("QUANTUM_BACKEND", "local"),
            shots=int(os.getenv("QUANTUM_SHOTS", 1024))
        ),
        ai=AIConfig(
            model_path=os.getenv("AI_MODEL_PATH", "./models/predictive_model.pkl"),
            threshold=float(os.getenv("AI_THRESHOLD", 0.5))
        )
    )

# Load the configuration when the module is imported
config = load_config()
