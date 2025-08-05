import pickle
import os

print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir('.'))

try:
    print("\nTrying to load model.p...")
    with open('model.p', 'rb') as f:
        model = pickle.load(f)
    
    print('Model loaded successfully!')
    print('Type:', type(model))
    print('Has predict method:', hasattr(model, 'predict'))
    print('Has predict_proba method:', hasattr(model, 'predict_proba'))
    
    if hasattr(model, 'predict'):
        print('✅ Model is VALID - has predict method')
    else:
        print('❌ Model is INVALID - missing predict method')
        
except FileNotFoundError:
    print('❌ model.p file not found')
    print('Available files:', [f for f in os.listdir('.') if f.endswith('.p')])
except Exception as e:
    print('❌ Error loading model:', e)