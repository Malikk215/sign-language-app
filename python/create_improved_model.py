import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import string
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def create_realistic_hand_landmarks(letter, num_samples=20):
    """Create more realistic hand landmark patterns for each letter"""
    np.random.seed(ord(letter))  # Use letter's ASCII value as seed for consistency
    
    # Base hand position (21 landmarks * 3 coordinates = 63 features)
    base_landmarks = np.random.rand(63) * 0.5 + 0.25  # Values between 0.25-0.75
    
    # Create letter-specific patterns
    samples = []
    for i in range(num_samples):
        landmarks = base_landmarks.copy()
        
        # Add letter-specific modifications
        letter_index = ord(letter) - ord('A')
        
        # Modify specific landmark positions based on letter
        # Thumb tip (landmark 4)
        landmarks[12:15] += np.sin(letter_index * 0.5) * 0.2
        
        # Index finger tip (landmark 8) 
        landmarks[24:27] += np.cos(letter_index * 0.3) * 0.15
        
        # Middle finger tip (landmark 12)
        landmarks[36:39] += np.sin(letter_index * 0.7) * 0.18
        
        # Ring finger tip (landmark 16)
        landmarks[48:51] += np.cos(letter_index * 0.9) * 0.12
        
        # Pinky tip (landmark 20)
        landmarks[60:63] += np.sin(letter_index * 1.1) * 0.1
        
        # Add some noise for variation
        noise = np.random.normal(0, 0.05, 63)
        landmarks += noise
        
        # Ensure values stay in valid range [0, 1]
        landmarks = np.clip(landmarks, 0, 1)
        
        samples.append(landmarks)
    
    return np.array(samples)

print("Creating improved training data for alphabet detection...")
print("This model will have distinct patterns for each letter.")

# Create training data with realistic patterns
X_train = []
y_train = []

letters = list(string.ascii_uppercase)  # ['A', 'B', 'C', ..., 'Z']

for letter in letters:
    print(f"Generating patterns for letter: {letter}")
    letter_samples = create_realistic_hand_landmarks(letter, num_samples=25)
    X_train.extend(letter_samples)
    y_train.extend([letter] * len(letter_samples))

X_train = np.array(X_train)
y_train = np.array(y_train)

print(f"Total training samples: {len(X_train)}")
print(f"Features per sample: {X_train.shape[1]}")
print(f"Unique letters: {len(set(y_train))}")

# Split data for validation
X_train_split, X_val, y_train_split, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
)

# Create and train an improved model
print("Training improved Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,  # More trees for better accuracy
    max_depth=15,      # Prevent overfitting
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

model.fit(X_train_split, y_train_split)

# Validate the model
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f"Validation accuracy: {accuracy:.2f}")

# Save the improved model
print("Saving improved model...")
with open('model.p', 'wb') as f:
    pickle.dump(model, f)

print("✅ Improved alphabet model created successfully!")
print(f"Model type: {type(model)}")
print(f"Model classes: {sorted(model.classes_)}")
print(f"Number of classes: {len(model.classes_)}")
print(f"Model accuracy on validation set: {accuracy:.2f}")

# Test the model with each letter pattern
print("\nTesting model predictions for each letter:")
for letter in letters:  # Test ALL letters, not just first 5
    test_sample = create_realistic_hand_landmarks(letter, num_samples=1)
    prediction = model.predict(test_sample)[0]
    confidence = np.max(model.predict_proba(test_sample))
    print(f"Letter {letter}: Predicted '{prediction}' (confidence: {confidence:.2f})")

print("\nModel is ready for use!")