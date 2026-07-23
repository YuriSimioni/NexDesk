# Importing necessary libraries
from app.extensions import db
from app.modules.categories.models import Category


# Class for exception errors
class CategoryServiceError(Exception):
    """category service exception."""
    pass

# Class for category logic
class CategoryService:

    @staticmethod
    def create_category(name: str, department_id: int, color: str) -> Category:
        """Verify if user is possible authenticate"""
        
        # Verify name and description exists
        if not name or not department_id:
            raise CategoryServiceError("Invalid name or department.")

        # Getting category from database
        category = db.session.query(Category).filter_by(name=name, department_id=department_id).first()

        # If category name is already register
        if category:
            raise CategoryServiceError("There is already a category with this name in this department.")
        
        # Create new department
        new_category = Category(
            name=name,
            department_id=department_id,
            color=color
        )
        
        # Insert category in database
        db.session.add(new_category)
        
        # Commit changes
        db.session.commit()
        
        # Return new category object
        return new_category
    
    @staticmethod
    def get_categories_by_department(department_id: int = 0) -> list[Category]:
        """Return all categories registered"""
        
        # Getting all categories
        if department_id != 0:
            return db.session.query(Category).all()
        
        # Getting categories by department
        return db.session.query(Category).filter_by(department_id=department_id).all()
        
    @staticmethod
    def category_exists(id: int) -> Category:
        """Verify category exists"""
        
        # Search category
        category = db.session.query(Category).filter_by(id=id).first()
        # If not exists
        if not category:
            raise CategoryServiceError("Category not exists.")

        # Return category
        return category
        
    @staticmethod
    def get_category_by_id(id: int) -> Category:
        """Return object category"""
        # Getting category by id pass
        category = CategoryService.category_exists(id=id)

        # Return category
        return category
        
    @staticmethod
    def delete_category(id: int) -> bool:
        """Delete category"""
        # Getting category
        category = CategoryService.category_exists(id)

        # Deleting from database
        db.session.delete(category)
        
        # Save changes
        db.session.commit()

        return True
       