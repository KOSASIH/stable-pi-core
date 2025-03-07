import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import numpy as np

# Load your dataset
# For demonstration, we will create a synthetic dataset
# In a real scenario, you would load your dataset from a CSV or database
data = {
    'historical_demand': [100, 150, 200, 250, 300, 350, 400, 450, 500, 550],
    'seasonality': [1, 1, 1, 2, 2, 2, 3, 3, 3, 4],  # Example feature
    'promotion': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]  # Example feature: promotional activity
}

df = pd.DataFrame(data)

# Features and target variable
X = df[['historical_demand', 'seasonality', 'promotion']]
y = df['historical_demand'].shift(-1).dropna()  # Predict next period's demand
X = X[:-1]  # Align X with y

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model selection and hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10]
}

# Using Random Forest Regressor for better performance
model = RandomForestRegressor(random_state=42)

# Grid search for hyperparameter tuning
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best model from grid search
best_model = grid_search.best_estimator_

# Evaluate the model
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Save the model
joblib.dump(best_model, 'models/demand_prediction_model.pkl')
print('Demand prediction model saved as demand_prediction_model.pkl')
