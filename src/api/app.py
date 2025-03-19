# api/app.py

from flask import Flask
from api.routes import api_routes  # Ensure the correct import path for your routes

def create_app():
    """Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)

    # Register API routes
    app.register_blueprint(api_routes, url_prefix='/api')

    @app.route('/')
    def home():
        """Home route for the API."""
        return "Welcome to the Blockchain API!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
