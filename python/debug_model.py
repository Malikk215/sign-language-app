import pickle
import numpy as np

# Load model yang sebenarnya digunakan
with open('model.p', 'rb') as f:
    model = pickle.load(f)

print(f"Model type: {type(model)}")
print(f"Model classes: {getattr(model, 'classes_', 'No classes attribute')}")

# Test dengan data dummy
test_data = np.random.rand(1, 63)  # 63 features seperti di create_dummy_model.py
prediction = model.predict(test_data)
print(f"Sample prediction: {prediction}")

# Jika ada predict_proba
if hasattr(model, 'predict_proba'):
    proba = model.predict_proba(test_data)
    print(f"Prediction probabilities shape: {proba.shape}")
    print(f"Max probability: {np.max(proba)}")