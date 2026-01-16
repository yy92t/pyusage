from flask import Flask
from app.routes import generator

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(generator.bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)