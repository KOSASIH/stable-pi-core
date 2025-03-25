import secrets
import time
import hashlib
from flask import session, request, abort

class CSRFProtection:
    def __init__(self, token_expiry=3600):
        self.token_expiry = token_expiry  # Token expiry time in seconds

    def _generate_token(self, user_id):
        """Generate a secure CSRF token using user ID and current timestamp."""
        timestamp = str(int(time.time()))
        token = f"{user_id}:{timestamp}:{secrets.token_hex(16)}"
        return self._hash_token(token)

    def _hash_token(self, token):
        """Hash the token for secure storage."""
        return hashlib.sha256(token.encode()).hexdigest()

    def generate_token(self, user_id):
        """Generate and store a CSRF token for the user."""
        token = self._generate_token(user_id)
        session['csrf_token'] = token
        session['csrf_timestamp'] = int(time.time())
        return token

    def verify_token(self, user_id, token):
        """Verify the CSRF token against the stored token."""
        if 'csrf_token' not in session or 'csrf_timestamp' not in session:
            abort(403, "CSRF token missing or session expired.")

        # Check if the token is expired
        if int(time.time()) - session['csrf_timestamp'] > self.token_expiry:
            abort(403, "CSRF token expired.")

        # Hash the incoming token for comparison
        hashed_token = self._hash_token(f"{user_id}:{session['csrf_timestamp']}:{token}")
        if hashed_token != session['csrf_token']:
            abort(403, "Invalid CSRF token.")

        return True

# Example usage in a Flask application
from flask import Flask, request

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure session key
csrf_protection = CSRFProtection()

@app.route('/generate_csrf', methods=['POST'])
def generate_csrf():
    user_id = request.form.get('user_id')
    token = csrf_protection.generate_token(user_id)
    return {'csrf_token': token}

@app.route('/modify_data', methods=['POST'])
def modify_data():
    user_id = request.form.get('user_id')
    csrf_token = request.form.get('csrf_token')
    csrf_protection.verify_token(user_id, csrf_token)
    # Proceed with data modification
    return {'status': 'success'}

if __name__ == "__main__":
    app.run(debug=True)
