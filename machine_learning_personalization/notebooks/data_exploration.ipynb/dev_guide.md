# Data Exploration Notebook

This notebook is designed for exploring the user behavior data collected from IoT devices. We will load the data, perform exploratory data analysis (EDA), and visualize key aspects of the data.

## 1. Load Libraries

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set(style="whitegrid")
```

## 2. Load Data

```python
# Load the user behavior data
df = pd.read_csv('data/user_behavior.csv')

# Display the first few rows of the dataframe
df.head()
```

## 3. Data Overview

```python
# Get a summary of the dataset
df.info()

# Check for missing values
missing_values = df.isnull().sum()
missing_values[missing_values > 0]
```

## 4. Data Distribution

### 4.1 Temperature Distribution

```python
plt.figure(figsize=(10, 6))
sns.histplot(df['temperature'], bins=20, kde=True, color='skyblue')
plt.title('Temperature Distribution')
plt.xlabel('Temperature (°C)')
plt.ylabel('Frequency')
plt.axvline(df['temperature'].mean(), color='red', linestyle='--', label='Mean Temperature')
plt.legend()
plt.show()
```

### 4.2 Humidity Distribution

```python
plt.figure(figsize=(10, 6))
sns.histplot(df['humidity'], bins=20, kde=True, color='lightgreen')
plt.title('Humidity Distribution')
plt.xlabel('Humidity (%)')
plt.ylabel('Frequency')
plt.axvline(df['humidity'].mean(), color='red', linestyle='--', label='Mean Humidity')
plt.legend()
plt.show()
```

## 5. Activity Type Counts

```python
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='activity_type', order=df['activity_type'].value_counts().index, palette='viridis')
plt.title('Activity Type Counts')
plt.xlabel('Activity Type')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()
```

## 6. Time Series Analysis

```python
# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# Plot the number of activities over time
plt.figure(figsize=(12, 6))
df.resample('H').size().plot()
plt.title('Number of Activities Over Time')
plt.xlabel('Time')
plt.ylabel('Number of Activities')
plt.grid()
plt.show()
```

## 7. Correlation Analysis

```python
# Calculate correlation matrix
correlation_matrix = df[['temperature', 'humidity']].corr()

# Create a heatmap for the correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', square=True)
plt.title('Correlation Matrix')
plt.show()
```

## 8. Conclusion

In this notebook, we explored the user behavior data by visualizing the distributions of temperature and humidity, analyzing activity types, and examining trends over time. The correlation analysis provided insights into the relationships between different features.

Next steps could include further feature engineering, model training, or deeper analysis based on specific questions or hypotheses.
```

### Key Components of the Notebook

1. **Load Libraries**: Imports necessary libraries for data manipulation and visualization.

2. **Load Data**: Loads the user behavior data from a CSV file and displays the first few rows.

3. **Data Overview**: Provides a summary of the dataset, including data types and missing values.

4. **Data Distribution**: Visualizes the distributions of temperature and humidity, including mean lines for reference.

5. **Activity Type Counts**: Displays a count of different activity types recorded in the dataset.

6. **Time Series Analysis**: Analyzes the number of activities over time, providing insights into user engagement.

7. **Correlation Analysis**: Calculates and visualizes the correlation between temperature and humidity.

8. **Conclusion**: Summarizes the findings and suggests next steps for further analysis or modeling.

### Running the Notebook

1. **Open Jupyter Notebook**:
   Navigate to the `notebooks/` directory in your terminal and start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

2. **Run the Notebook**:
   Open `data_exploration.ipynb` in Jupyter and run the cells to perform data exploration and visualization.
