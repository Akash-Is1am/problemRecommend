import os
import numpy as np
import tensorflow as tf
from score import get_sum_array, get_score

current_directory = os.path.dirname(__file__)  # Get current script's directory
file_path = os.path.join(current_directory, 'model_version_1.h5')  # Path to the solved set file


# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(64, activation='relu', input_shape=(4,)),  # First hidden layer
#     tf.keras.layers.Dense(64, activation='relu'),  # Second hidden layer
#     tf.keras.layers.Dense(1)  # Output layer
# ])


model = tf.keras.models.load_model(file_path)  # Load the saved model

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])


skill = 7
verbose_mode = 1
number_of_epoch = 70
X_train = []
Y_train = []



X = get_sum_array(skill)
Y = get_score(X)



X_train.append(X)
Y_train.append(Y)


X_train = np.array(X_train)
Y_train = np.array(Y_train)

# model.fit(X_train, Y_train, epochs=number_of_epoch, verbose=verbose_mode)

# model.save(file_path)



predictions = model.predict(X_train)
print("Predictions:", predictions)
print("Ans: ", Y)


loss, mae = model.evaluate(X_train, Y_train, verbose=1)  # Evaluate with the test data
print("Loss:", loss)
print("Mean Absolute Error:", mae)


accuracy = predictions / Y * 100
print("Accuracy: ", accuracy)

