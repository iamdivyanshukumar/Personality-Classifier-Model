from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # Register blueprints
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    # Load models
    with app.app_context():
        try:
            from app.model import load_models
            app.models = load_models()
            print("Models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            # Create placeholder models
            app.models = {
                'model': None,
                'scaler': None,
                'label_encoder': None
            }
    
    return app