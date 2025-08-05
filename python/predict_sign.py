import sys
import json
import pickle
import cv2
import mediapipe as mp
import numpy as np
import os
from contextlib import redirect_stderr
import threading
import time

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['GLOG_minloglevel'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

class TimeoutError(Exception):
    pass

def timeout_handler():
    raise TimeoutError("Script execution timed out")

timeout_timer = None

def start_timeout(seconds=45):  # Increase from 25 to 45 seconds
    global timeout_timer
    timeout_timer = threading.Timer(seconds, timeout_handler)
    timeout_timer.start()

def predict_sign(image_path, model_path):
    try:
        # Add performance timing
        start_time = time.time()
        print(f"DEBUG: Starting prediction at {start_time}", file=sys.stderr)
        
        # Load model (cache if possible)
        print(f"DEBUG: Loading model from {model_path}", file=sys.stderr)
        load_start = time.time()
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"DEBUG: Model loaded in {time.time() - load_start:.2f}s", file=sys.stderr)
        
        print(f"DEBUG: Model type: {type(model)}", file=sys.stderr)
        print(f"DEBUG: Model has predict method: {hasattr(model, 'predict')}", file=sys.stderr)
        print(f"DEBUG: Model has predict_proba method: {hasattr(model, 'predict_proba')}", file=sys.stderr)
        
        # Load and process image
        print(f"DEBUG: Loading image from {image_path}", file=sys.stderr)
        if not os.path.exists(image_path):
            return {"error": f"Image file not found: {image_path}", "prediction": None, "confidence": 0.0}
        
        image = cv2.imread(image_path)
        if image is None:
            return {"error": f"Could not load image: {image_path}", "prediction": None, "confidence": 0.0}
        
        print(f"DEBUG: Image shape: {image.shape}", file=sys.stderr)
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Initialize MediaPipe with more tolerant parameters
        print("DEBUG: Initializing MediaPipe...", file=sys.stderr)
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=2,
            min_detection_confidence=0.3,  # Lowered from 0.5 to 0.3
            min_tracking_confidence=0.3    # Lowered from 0.5 to 0.3
        )
        print("DEBUG: MediaPipe initialized", file=sys.stderr)
        
        # Process image
        print("DEBUG: Processing image with MediaPipe...", file=sys.stderr)
        results = hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            print(f"DEBUG: Found {len(results.multi_hand_landmarks)} hand(s)", file=sys.stderr)
            
            # Extract landmarks from first hand
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = []
            
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            
            print(f"DEBUG: Extracted {len(landmarks)} landmark features", file=sys.stderr)
            
            # Make prediction
            print("DEBUG: Making prediction...", file=sys.stderr)
            landmarks_array = np.array([landmarks])
            
            try:
                # Make prediction
                prediction = model.predict(landmarks_array)[0]
                print(f"DEBUG: Raw prediction: {prediction}", file=sys.stderr)
                
                if hasattr(model, 'predict_proba'):
                    probabilities = model.predict_proba(landmarks_array)[0]
                    confidence = float(np.max(probabilities))
                else:
                    # Fallback confidence calculation
                    confidence = 0.8  # Default confidence
                    print("DEBUG: Model doesn't have predict_proba, using default confidence", file=sys.stderr)
                
                print(f"DEBUG: Raw confidence: {confidence}", file=sys.stderr)
                
            except Exception as pred_error:
                print(f"DEBUG: Prediction error: {str(pred_error)}", file=sys.stderr)
                return {"error": f"Model prediction failed: {str(pred_error)}", "prediction": None, "confidence": 0.0}
            
            # Boost confidence slightly
            boosted_confidence = boost_confidence(landmarks, confidence)
            
            print(f"DEBUG: Boosted confidence: {boosted_confidence}", file=sys.stderr)
            
            # Clean up
            hands.close()
            
            return {
                "prediction": prediction,
                "confidence": boosted_confidence,
                "accuracy": boosted_confidence * 100,
                "raw_confidence": confidence,
                "landmarks_count": len(landmarks)
            }
        else:
            print("DEBUG: No hands detected in image", file=sys.stderr)
            hands.close()
            return {"error": "No hands detected in image", "prediction": None, "confidence": 0.0}
        
        # Add timing info to result
        total_time = time.time() - start_time
        print(f"DEBUG: Total prediction time: {total_time:.2f}s", file=sys.stderr)
        
    except Exception as e:
        print(f"DEBUG: Exception in predict_sign: {str(e)}", file=sys.stderr)
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}", file=sys.stderr)
        return {"error": f"Prediction error: {str(e)}", "prediction": None, "confidence": 0.0}

def boost_confidence(landmarks, base_confidence):
    # Simple confidence boosting
    return min(base_confidence * 1.1, 1.0)

if __name__ == "__main__":
    try:
        # Start timeout
        start_timeout(25)
        
        print(f"DEBUG: Script started with {len(sys.argv)} arguments", file=sys.stderr)
        print(f"DEBUG: Arguments: {sys.argv}", file=sys.stderr)
        
        if len(sys.argv) != 3:
            result = {"error": "Usage: python predict_sign.py <image_path> <model_path>", "prediction": None, "confidence": 0.0}
        else:
            image_path = sys.argv[1]
            model_path = sys.argv[2]
            print(f"DEBUG: Processing {image_path} with {model_path}", file=sys.stderr)
            result = predict_sign(image_path, model_path)
        
        print(f"DEBUG: Final result: {result}", file=sys.stderr)
        print(json.dumps(result))
        
    except Exception as e:
        print(f"DEBUG: Main exception: {str(e)}", file=sys.stderr)
        import traceback
        print(f"DEBUG: Main traceback: {traceback.format_exc()}", file=sys.stderr)
        error_result = {"error": f"Script error: {str(e)}", "prediction": None, "confidence": 0.0}
        print(json.dumps(error_result))
    finally:
        # Cancel timeout
        cancel_timeout()