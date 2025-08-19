from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Load models when app starts
    with app.app_context():
        try:
            from app.model import load_models
            app.models = load_models()
            print("Models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            # Create placeholder models for development
            app.models = {
                'model': None,
                'scaler': None,
                'label_encoder': None
            }
    
    return app