from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration settings
    app.config.from_object('config')

    # Register blueprints
    from .routes import main as main_routes
    app.register_blueprint(main_routes)

    return app