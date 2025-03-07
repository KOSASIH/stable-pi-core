# scripts/setup.py

import os
import subprocess
import sys

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    """Main setup function."""
    print("Setting up the environment for the Quantum and AI Arbitration project...")

    # List of required packages
    required_packages = [
        'numpy',
        'pandas',
        'scikit-learn',
        'qiskit',
        'matplotlib',
        'joblib',
        'pytest'  # For testing
    ]

    # Install each package
    for package in required_packages:
        print(f"Installing {package}...")
        install(package)

    print("All packages installed successfully.")
    print("Setup complete! You can now run the project.")

if __name__ == "__main__":
    main()
