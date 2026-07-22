# Importing necessary libraries
from werkzeug.security import check_password_hash
from datetime import datetime, timezone
from app.extensions import db
from app.modules.users.models import User


# Class for exception errors
class AuthServiceError(Exception):
    """Authentication service exception."""
    pass

# Class for Auth logic
class AuthService:

    @staticmethod
    def authenticate(email: str, password: str) -> User:
        """Verify if user is possible authenticate"""
        
        # Verify email and password exists
        if not email or not password:
            raise AuthServiceError("Invalid email or password.")
        
        # Scape string mail
        mail = email.strip().lower()

        # Getting user in database
        user = db.session.query(User).filter_by(email=mail).first()

        # Authenticate credentials
        if not user or not check_password_hash(user.password_hash, password):
            raise AuthServiceError("Invalid email or password.")
        
        # Account is inactive
        if not user.account_is_active:
            raise AuthServiceError("Account is inactive.")
        
        return user


    @staticmethod
    def update_last_login(user: User) -> None:
        """Update the user's last successful login timestamp."""

        # Getting timestamp
        user.last_login_at = datetime.now(timezone.utc)

        try:
            
            # Insert in database
            db.session.commit()
            
        except Exception:
            
            # Rollback
            db.session.rollback()
            raise