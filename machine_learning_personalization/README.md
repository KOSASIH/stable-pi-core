# Machine Learning Personalization for IoT

This project implements a machine learning personalization system for IoT devices. It collects user behavior data, analyzes it, and provides recommendations based on user patterns.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The system collects data from IoT devices, processes it, and uses machine learning algorithms to provide personalized recommendations to users. The project includes data collection, cleaning, storage in a database, and model training.

## Features

- Simulates user behavior data collection from IoT devices.
- Cleans and processes the collected data.
- Stores cleaned data in a SQLite database.
- Trains a K-Nearest Neighbors recommendation model.
- Provides recommendations based on user behavior patterns.

## Technologies Used

- **Python**: The primary programming language for the project.
- **Pandas**: For data manipulation and analysis.
- **Scikit-learn**: For machine learning algorithms.
- **Matplotlib & Seaborn**: For data visualization.
- **SQLite**: For database storage.
- **Jupyter Notebook**: For exploratory data analysis and model training.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/KOSASIH/stable-pi-core.git
   cd machine_learning_personalization
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Data Collection**: Run the `main.py` script to collect user behavior data, clean it, store it in the database, and train the recommendation model.
   ```bash
   python main.py
   ```

2. **Jupyter Notebooks**: Use the provided Jupyter notebooks for data exploration and model training:
   - `notebooks/data_exploration.ipynb`: Explore and visualize the user behavior data.
   - `notebooks/model_training.ipynb`: Train the recommendation model and evaluate its performance.

3. **Database Interaction**: The cleaned data will be stored in a SQLite database named `user_behavior.db`. You can query this database for further analysis.

## Directory Structure

```
machine_learning_personalization/
│
├── data/                          # Directory for storing data files
│   ├── user_behavior.csv          # CSV file for storing user behavior data
│   ├── cleaned_user_behavior.csv   # Cleaned user behavior data
│
├── models/                        # Directory for storing trained models
│   ├── recommendation_model.pkl    # Pickled model file for the recommendation system
│
├── notebooks/                     # Directory for Jupyter notebooks
│   ├── data_exploration.ipynb     # Notebook for data exploration and visualization
│   ├── model_training.ipynb        # Notebook for training the recommendation model
│
├── src/                           # Source code directory
│   ├── __init__.py                # Makes src a package
│   ├── data_collection.py          # Script for collecting user behavior data
│   ├── data_processing.py          # Script for processing and cleaning data
│   ├── recommendation_system.py     # Script for building and using the recommendation system
│   ├── database.py                 # Script for database interactions
│
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── main.py                        # Main entry point for running the application
```

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
