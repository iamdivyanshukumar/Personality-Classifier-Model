import joblib
import tensorflow as tf
from tensorflow import keras
import os

def load_models():
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        models_path = os.path.join(base_dir, '..', 'models')
        
        models = {
            'model': keras.models.load_model(os.path.join(models_path, 'personality_model.h5')),
            'scaler': joblib.load(os.path.join(models_path, 'scaler.pkl')),
            'label_encoder': joblib.load(os.path.join(models_path, 'label_encoder.pkl'))
        }
        return models
    except Exception as e:
        print(f"Error loading models: {e}")
        raise