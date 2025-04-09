import tensorflow as tf
import numpy as np

# Sample data
X = np.array([[1], [2], [3], [4], [5]])  # Input features (amounts)
y = np.array([[1.5], [3.0], [4.5], [6.0], [7.5]])  # Target values (predicted values)

# Define a simple model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(1, input_shape=(1,))
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X, y, epochs=100)

# Save the model
model.save('path/to/your/model')
