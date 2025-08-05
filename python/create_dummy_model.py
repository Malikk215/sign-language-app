import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import string

# Create dummy training data (21 landmarks * 3 coordinates = 63 features)
print("Creating dummy training data for alphabet only...")
X_dummy = np.random.rand(260, 63)  # 260 samples (10 per letter), 63 features

# Create labels for A-Z only (26 letters)
letters = list(string.ascii_uppercase)  # ['A', 'B', 'C', ..., 'Z']
y_dummy = np.repeat(letters, 10)  # 10 samples per letter

# Shuffle the data
indices = np.random.permutation(len(X_dummy))
X_dummy = X_dummy[indices]
y_dummy = y_dummy[indices]

# Create and train a simple model
print("Training model for alphabet detection...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_dummy, y_dummy)

# Save the model
print("Saving model...")
with open('model.p', 'wb') as f:
    pickle.dump(model, f)

print("✅ Alphabet-only dummy model created successfully!")
print(f"Model type: {type(model)}")
print(f"Model classes: {sorted(model.classes_)}")
print(f"Number of classes: {len(model.classes_)}")
print(f"Model has predict: {hasattr(model, 'predict')}")
print(f"Model has predict_proba: {hasattr(model, 'predict_proba')}")

# Test the model
test_data = np.random.rand(1, 63)
prediction = model.predict(test_data)
confidence = model.predict_proba(test_data)
print(f"Test prediction: {prediction[0]}")
print(f"Test confidence: {np.max(confidence):.2f}")