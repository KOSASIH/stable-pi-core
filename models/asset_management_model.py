import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load your dataset
# For demonstration, we will create a synthetic dataset
# In a real scenario, you would load your dataset from a CSV or database
data = {
    'asset_type': ['stock', 'bond', 'stock', 'bond', 'stock', 'real estate', 'real estate', 'bond', 'stock', 'real estate'],
    'risk_level': [1, 0, 1, 0, 1, 2, 2, 0, 1, 2],  # 0: Low, 1: Medium, 2: High
    'return': [10, 5, 12, 3, 15, 8, 9, 4, 11, 7]  # Example feature
}

df = pd.DataFrame(data)

# Encode categorical variables
df['asset_type'] = df['asset_type'].astype('category').cat.codes

# Features and target variable
X = df[['asset_type', 'risk_level', 'return']]
y = df['asset_type']  # Predict asset type

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model selection and hyperparameter tuning using GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10]
}

# Using Random Forest Classifier for better performance
model = RandomForestClassifier(random_state=42)

# Grid search for hyperparameter tuning
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy', verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best model from grid search
best_model = grid_search.best_estimator_

# Evaluate the model
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(report)

# Save the model
joblib.dump(best_model, 'models/asset_management_model.pkl')
print('Asset management model saved as asset_management_model.pkl')
