# Importing necessary libraries
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.core.config import PageTemplate
from app.modules.departments.services import DepartmentService, DepartmentServiceError


# Initialize Blueprint for authentication module
department_bp = Blueprint("department", __name__)

# ======== LOGIN ==========
@department_bp.route("/departments/create", methods=["POST"])
@login_required
def department_create():
    """Route responsible for create department."""
    
    # Post REQUEST
    if request.method == "POST":
        
        # Get and sanitize data submitted via the form
        name = (request.form.get("name") or "").strip().title()
        description = request.form.get("description", "").strip().capitalize()

        # Trying create
        try:
            
            # New department
            DepartmentService.create_department(
                name=name,
                description=description
            )
            
            # Feedback for user
            flash("Department is created successfully", "success")

        # Except errors
        except DepartmentServiceError as e:
            
            # Return message for user
            flash(f"{e}", "error")
            
            # Redirect to home
    return redirect(url_for("auth.home"))
            


@department_bp.route("/department/delete/<int:id>", methods=["POST"])
def department_delete(id: int):
    """Route for delete department"""
    try:
        # Getting department
        department_delete = DepartmentService.get_department_by_id(id)
        
        # Delete department
        DepartmentService.delete_department(id)
        
        # Return feedback for user
        flash(f"Department {department_delete.name} has ben exclude")
     
    except DepartmentServiceError as e:
        # Return feedback for user
        flash(str(e), "error")
    
    # Redirect to home
    return redirect(url_for("auth.home"))