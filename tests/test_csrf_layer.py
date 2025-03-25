import unittest
from flask import Flask, session
from csrf_layer import CSRFProtection
import secrets

class TestCSRFProtection(unittest.TestCase):
    def setUp(self):
        """Set up a Flask application context for testing."""
        self.app = Flask(__name__)
        self.app.secret_key = secrets.token_hex(32)  # Secure session key
        self.csrf_protection = CSRFProtection(token_expiry=5)  # Token expiry set to 5 seconds for testing

        with self.app.test_request_context():
            session['user_id'] = 'test_user'

    def test_generate_token(self):
        """Test token generation."""
        with self.app.test_request_context():
            user_id = session['user_id']
            token = self.csrf_protection.generate_token(user_id)
            self.assertIn('csrf_token', session)
            self.assertIn('csrf_timestamp', session)
            self.assertEqual(token, session['csrf_token'])

    def test_verify_token_success(self):
        """Test successful token verification."""
        with self.app.test_request_context():
            user_id = session['user_id']
            token = self.csrf_protection.generate_token(user_id)
            self.assertTrue(self.csrf_protection.verify_token(user_id, token))

    def test_verify_token_invalid(self):
        """Test verification with an invalid token."""
        with self.app.test_request_context():
            user_id = session['user_id']
            token = self.csrf_protection.generate_token(user_id)
            invalid_token = 'invalid_token'
            with self.assertRaises(Exception) as context:
                self.csrf_protection.verify_token(user_id, invalid_token)
            self.assertEqual(str(context.exception), "Invalid CSRF token.")

    def test_verify_token_expired(self):
        """Test verification with an expired token."""
        with self.app.test_request_context():
            user_id = session['user_id']
            token = self.csrf_protection.generate_token(user_id)
            # Simulate waiting for the token to expire
            import time
            time.sleep(6)  # Wait for 6 seconds to exceed the expiry time
            with self.assertRaises(Exception) as context:
                self.csrf_protection.verify_token(user_id, token)
            self.assertEqual(str(context.exception), "CSRF token expired.")

    def test_verify_token_missing(self):
        """Test verification when token is missing."""
        with self.app.test_request_context():
            user_id = session['user_id']
            with self.assertRaises(Exception) as context:
                self.csrf_protection.verify_token(user_id, None)
            self.assertEqual(str(context.exception), "CSRF token missing or session expired.")

if __name__ == '__main__':
    unittest.main()
