# user_interface/app.py

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize Flask app and extensions
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Database model for users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Database model for data listings
class DataListing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard with data listings."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    listings = DataListing.query.all()
    return render_template('dashboard.html', listings=listings)

@app.route('/submit_data', methods=['POST'])
def submit_data():
    """Submit new data listing."""
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    title = request.form['title']
    description = request.form['description']
    new_listing = DataListing(title=title, description=description, owner_id=session['user_id'])
    db.session.add(new_listing)
    db.session.commit()
    socketio.emit('new_listing', {'title': title, 'description': description}, broadcast=True)
    return jsonify({"message": "Data submitted successfully."}), 201

@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connections."""
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnections."""
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
