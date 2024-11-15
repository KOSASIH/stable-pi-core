from flask import Flask
from routes import api_routes

app = Flask(__name__)

# Register API routes
app.register_blueprint(api_routes)

@app.route('/')
def home():
    return "Welcome to the Blockchain API!"

if __name__ == '__main__':
    app.run(debug=True)
