# Importing necessary libraries
from werkzeug.security import generate_password_hash
from app.extensions import db, regex
from app.modules.departments.models import Department, UserDepartment
from app.modules.departments.roles import DepartmentRole
from app.modules.departments.services import DepartmentService
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
    
    @staticmethod
    def user_exists(id: int) -> User:
        """Verify user exists"""
        
        # Search department
        user = db.session.query(User).filter_by(id=id).first()

        # If not exists
        if not user:
            raise UserServiceError("User not exists.")

        # Return department
        return user
    
    @staticmethod
    def get_all_users() -> list[User]:
        """Return all users"""
        return db.session.query(User).all()
        
    @staticmethod
    def add_department(user_id: int, department_id: int, role: DepartmentRole = DepartmentRole.USER) -> UserDepartment:
        """Add user in department"""
        
        # Verify if instances exists
        department  = DepartmentService.department_exists(department_id)
        user = UserService.user_exists(user_id)
        user_exists_department = db.session.query(UserDepartment).filter_by(user_id=user.id, department_id=department.id).first()
                
        # If user already on department
        if user_exists_department:
            raise UserServiceError("User is already on this department.")
        
        # Creating new instance
        user_department = UserDepartment(
            user_id=user.id,
            department_id=department.id,
            department_role=role
        )
        
        # Add on database
        db.session.add(user_department)
        
        # Save changes
        db.session.commit()
        
        # Return object
        return user_department
    
    @staticmethod
    def get_assigned_departments(user_id: int = 0) -> list[UserDepartment]:
        """Return all departments on user assigned"""
        return db.session.query(UserDepartment).filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_assigned_department(id: int) -> UserDepartment:
        """Return department on user assigned"""
        
        # Get assigned
        assigned = db.session.query(UserDepartment).filter_by(id=id).first()

        # If not assigned
        if assigned is None:
            raise UserServiceError("Department assignment not found.")

        # Return assigned
        return assigned
        
    
    
    @staticmethod
    def delete_department(id: int) -> bool:
        """Delete department"""
        # Getting department
        assigned = UserService.get_assigned_department(id)

        # Deleting from database
        db.session.delete(assigned)
        
        # Save changes
        db.session.commit()
        return True
        