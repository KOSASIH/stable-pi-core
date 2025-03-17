from setuptools import setup, find_packages

# Read the contents of your README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define the setup configuration
setup(
    name="stable-pi-core",  # Name of the package
    version="0.1.0",  # Initial version of the package
    author="Your Name",  # Your name
    author_email="your.email@example.com",  # Your email
    description="A project integrating quantum networking with blockchain technology.",  # Short description
    long_description=long_description,  # Long description from README
    long_description_content_type="text/markdown",  # Format of the long description
    url="https://github.com/yourusername/stable-pi-core",  # URL to the project repository
    packages=find_packages(),  # Automatically find packages in the project
    classifiers=[  # Classifiers to categorize the package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",  # Change as needed
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.7',  # Minimum Python version required
    install_requires=[  # List of dependencies
        "numpy==1.25.2",
        "pandas==2.1.0",
        "scikit-learn==1.3.1",
        "joblib==1.3.1",
        "pyyaml==6.0.1",
        "web3==6.1.0",
        "solcx==1.2.0",
        "pytest==7.4.1",
        "ntru==0.1.0",
        "matplotlib==3.7.2",
        "seaborn==0.12.2",
        "python-dotenv==0.21.0",
        "requests==2.32.2",
        "cryptography==39.0.1",
        "dask==2023.7.0",
        "xgboost==1.7.6",
        "loguru==0.6.0",
        "aiohttp==3.8.5",
        "protobuf==4.25.0",
    ],
    entry_points={  # Entry points for command line tools
        'console_scripts': [
            'stable-pi-cli=quantum_network.cli:main',  # Example CLI entry point
        ],
    },
    include_package_data=True,  # Include package data specified in MANIFEST.in
    zip_safe=False,  # Set to False if the package cannot be reliably used if installed as a .egg file
)
