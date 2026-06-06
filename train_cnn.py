import numpy as np
import tensorflow as tf

# 1. Load the freshly saved model
saved_model = tf.keras.models.load_model('p2guard_cnn_model.h5', compile=False)

print("\nBrute-forcing the optimal normal traffic signature...")

# 2. Generate 10,000 completely random network flows (scaled between 0 and 1)
random_traffic = np.random.rand(10000, 20)

# Reshape for the CNN
random_traffic_reshaped = random_traffic.reshape(-1, 20, 1)

# 3. Ask the model to grade all 10,000 flows instantly
predictions = saved_model.predict(random_traffic_reshaped, verbose=0)

# 4. Find the single flow that the model thinks is the absolute safest
safest_index = np.argmin(predictions)
safest_traffic = random_traffic[safest_index]
safest_score = predictions[safest_index][0]

print(f"\n--- FOUND IT! (P2P Probability: {safest_score * 100:.4f}%) ---")
print("COPY AND PASTE THIS EXACT ARRAY INTO APP.JSX:")

golden_array = [round(float(val), 4) for val in safest_traffic.flatten()]
print(golden_array)