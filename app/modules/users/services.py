# Importing necessary libraries
from werkzeug.security import generate_password_hash
from app.extensions import db, regex
from app.modules.users.models import User
from app.modules.users.roles import UserRole
import re

# Class for exception errors
class UserServiceError(Exception):
    """User service exception."""
    pass


# Class for User logic
class UserService:

    @staticmethod
    def create_user(
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        account_is_active: bool = True,
        role: UserRole = UserRole.USER
    ) -> User:
        """Register new user on database"""

        # Scape strings
        first_name = first_name.strip()
        last_name = last_name.strip()
        email = email.strip().lower()

        # Empty first name
        if not first_name:
            raise UserServiceError("First name is required.")

        # Empty last name
        if not last_name:
            raise UserServiceError("Last name is required.")

        # Empty email
        if not email:
            raise UserServiceError("Email is required.")

        # Email more 255 characters
        if len(email) > 255:
            raise UserServiceError("Email is too long.")

        # Email format invalid
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            raise UserServiceError("Invalid email address.")

        # Verify password
        if len(password) < 8:
            raise UserServiceError("Password must contain at least 8 characters.")
        
        # Password verify model
        if not re.search(regex, password):
            raise UserServiceError("The password requires uppercase letters, lowercase letters, numbers, and special characters.")
            
        # Email already registered
        if User.query.filter_by(email=email).first():
            raise UserServiceError("Email already registered.")

        # Creating user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=generate_password_hash(password),
            account_is_active=account_is_active,
            role=role,
        )

        # Insert in database
        db.session.add(user)
        
        # Commit on database
        db.session.commit()
        
        # Return user
        return user