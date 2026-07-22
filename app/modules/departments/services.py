# Importing necessary libraries
from app.extensions import db
from app.modules.departments.models import Department

# Class for exception errors
class DepartmentServiceError(Exception):
    """Department service exception."""
    pass

# Class for Department logic
class DepartmentService:

    @staticmethod
    def create_department(name: str, description: str) -> Department:
        """Verify if user is possible authenticate"""
        
        # Verify name and description exists
        if not name or not description:
            raise DepartmentServiceError("Invalid name or description.")

        # Getting department from database
        department = db.session.query(Department).filter_by(name=name).first()

        # If department name is already register
        if department:
            raise DepartmentServiceError("There is already a department with this name.")
        
        # Create new department
        new_department = Department(
            name=name,
            description=description
        )
        
        # Insert department in database
        db.session.add(new_department)
        
        # Commit changes
        db.session.commit()
        
        # Return new department object
        return new_department