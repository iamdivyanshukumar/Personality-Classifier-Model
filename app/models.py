import joblib
import tensorflow as tf
from tensorflow import keras

def load_models():
    try:
        models = {
            'model': keras.models.load_model('models/personality_model.h5'),
            'scaler': joblib.load('models/scaler.pkl'),
            'label_encoder': joblib.load('models/label_encoder.pkl')
        }
        return models
    except Exception as e:
        print(f"Error loading models: {e}")
        raise