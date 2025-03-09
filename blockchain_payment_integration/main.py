from flask import Flask, jsonify
from controllers.payment_controller import payment_bp
from controllers.webhook_controller import webhook_bp
from logging_config import setup_logging
from werkzeug.exceptions import HTTPException
import os

def create_app(config_name='development'):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configuration from environment variables or a config file
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    # Register blueprints
    app.register_blueprint(payment_bp)
    app.register_blueprint(webhook_bp)

    # Middleware for security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app

def handle_error(e):
    """Custom error handler for exceptions."""
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({"error": e.description, "status": "error"}).get_data()
        response.content_type = "application/json"
        return response
    else:
        response = {
            "error": str(e),
            "status": "error"
        }
        return jsonify(response), 500

if __name__ == '__main__':
    # Set up logging
    setup_logging()

    # Create the Flask app
    app = create_app(os.getenv('FLASK_ENV', 'development'))

    # Register error handler
    app.register_error_handler(Exception, handle_error)

    # Run the application
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=app.config['DEBUG'])
