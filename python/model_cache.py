import pickle
import os
import time

class ModelCache:
    _instance = None
    _model = None
    _model_path = None
    _load_time = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_model(self, model_path):
        # Check if model needs to be reloaded
        if (self._model is None or 
            self._model_path != model_path or 
            not os.path.exists(model_path)):
            
            print(f"DEBUG: Loading model from {model_path}", file=sys.stderr)
            start_time = time.time()
            
            with open(model_path, 'rb') as f:
                self._model = pickle.load(f)
            
            self._model_path = model_path
            self._load_time = time.time() - start_time
            print(f"DEBUG: Model loaded in {self._load_time:.2f}s", file=sys.stderr)
        else:
            print(f"DEBUG: Using cached model", file=sys.stderr)
            
        return self._model