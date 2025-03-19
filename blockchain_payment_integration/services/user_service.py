from models.user import User  # Assuming you have a User model defined
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, session):
        self.session = session

    def create_user(self, username, email, password):
        """Create a new user account."""
        new_user = User(username=username, email=email, password=password)  # Password should be hashed
        self.session.add(new_user)
        self.session.commit()
        logger.info("User created successfully: %s", username)
        return new_user

    def get_user_by_id(self, user_id):
        """Retrieve a user by their ID."""
        user = self.session.query(User).filter_by(id=user_id).first()
        if user:
            logger.info("User retrieved: %s", user.username)
            return user
        else:
            logger.warning("User not found: %s", user_id)
            return None

    def update_user(self, user_id, **kwargs):
        """Update user information."""
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.session.commit()
            logger.info("User updated successfully: %s", user.username)
            return user
        else:
            logger.warning("User not found for update: %s", user_id)
            return None

    def delete_user(self, user_id):
        """Delete a user account."""
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            logger.info("User deleted successfully: %s", user.username)
            return True
        else:
            logger.warning("User not found for deletion: %s", user_id)
            return False
