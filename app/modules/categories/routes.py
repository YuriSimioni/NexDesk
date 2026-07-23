# Importing necessary libraries
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import true
from app.modules.categories.services import CategoryService, CategoryServiceError
from app.modules.departments.services import DepartmentService, DepartmentServiceError


# Initialize Blueprint for authentication module
categories_bp = Blueprint("categories", __name__)

# ======== LOGIN ==========
@categories_bp.route("/categories/create", methods=["POST"])
@login_required
def category_create():
    """Route responsible for create categories."""
    
    # Post REQUEST
    if request.method == "POST":
        
        # Get and sanitize data submitted via the form
        name = str(request.form.get("name") or "").strip().title()
        department_id = int(request.form["department_id"])
        color = request.form["color"]
        
        
        # Trying create
        try:
            
            # New department
            CategoryService.create_category(
                name=name,
                department_id=department_id,
                color=color
            )
            
            # Feedback for user
            flash(f"Category {name} is created successfully", "success")

        # Except errors
        except CategoryServiceError as e:
            
            # Return message for user
            flash(f"{e}", "error")
            
            # Redirect to home
    return redirect(url_for("auth.home"))
            


@categories_bp.route("/categories/delete/<int:id>", methods=["POST"])
def category_delete(id: int):
    """Route for delete department"""
    try:
        # Getting department
        category_delete = CategoryService.get_category_by_id(id)
        
        # Delete department
        CategoryService.delete_category(id)
        
        # Return feedback for user
        flash(f"Category {category_delete.name} has ben exclude")
     
    except CategoryServiceError as e:
        # Return feedback for user
        flash(str(e), "error")
    
    # Redirect to home
    return redirect(url_for("auth.home"))