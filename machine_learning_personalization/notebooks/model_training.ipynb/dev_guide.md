# Model Training Notebook

This notebook is designed for training the recommendation model using user behavior data. We will load the cleaned data, train a K-Nearest Neighbors model, evaluate its performance, and save the trained model.

## 1. Load Libraries

```python
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle
import numpy as np
import os
```

## 2. Load Data

```python
# Load the cleaned user behavior data
df = pd.read_csv('data/cleaned_user_behavior.csv')

# Display the first few rows of the dataframe
df.head()
```

## 3. Prepare Data for Training

```python
# Select features for training
features = df[['temperature', 'humidity']]

# Display the features
features.head()

# Create a target variable (for example, we can use user_id as a target for demonstration)
# In a real scenario, you would define a more meaningful target based on your use case
target = df['user_id']
```

## 4. Split the Data

```python
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")
```

## 5. Train the Recommendation Model

```python
# Initialize the K-Nearest Neighbors model
model = NearestNeighbors(n_neighbors=3)

# Fit the model on the training data
model.fit(X_train)
```

## 6. Evaluate the Model

```python
# Example of making predictions on the test set
# Since KNN does not have a direct prediction method, we will use the distances and indices
distances, indices = model.kneighbors(X_test)

# For demonstration, we can calculate the mean squared error based on the indices
# Here we will assume that the target is user_id and we will just check the indices
# In a real scenario, you would have a more meaningful evaluation metric
predicted_user_ids = y_train.iloc[indices.flatten()].values
mse = mean_squared_error(y_test, predicted_user_ids)

print(f"Mean Squared Error: {mse:.2f}")
```

## 7. Save the Trained Model

```python
# Save the trained model to a file
model_filename = 'models/recommendation_model.pkl'
with open(model_filename, 'wb') as f:
    pickle.dump(model, f)

print(f"Model saved to {model_filename}.")
```

## 8. Example of Making Recommendations

```python
# Example new user data for recommendations
new_user_data = pd.DataFrame({
    'temperature': [22.0],
    'humidity': [60.0]
})

# Get recommendations
distances, indices = model.kneighbors(new_user_data)
print("Recommended indices:", indices)
```

## 9. Conclusion

In this notebook, we trained a K-Nearest Neighbors recommendation model using user behavior data. We evaluated the model's performance using mean squared error and saved the trained model for future use. 

Next steps could include further tuning of the model parameters, exploring different algorithms, or integrating the model into the main application.
```

### Key Enhancements

1. **Data Splitting**: Added a step to split the data into training and testing sets to evaluate the model's performance.

2. **Model Evaluation**: Included a basic evaluation step using mean squared error to demonstrate how to assess the model's performance.

3. **Clearer Structure**: Organized the notebook into sections with clear headings and explanations, making it easier to follow.

4. **Comments and Explanations**: Added comments throughout the notebook to explain each step and its purpose.

### Running the Notebook

1. **Open Jupyter Notebook**:
   Navigate to the `notebooks/` directory in your terminal and start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

2. **Run the Updated Notebook**:
   Open `model_training.ipynb` in Jupyter and run the cells to perform model training and evaluation.
