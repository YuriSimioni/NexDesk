# Importing necessary libraries
from flask import Blueprint, flash, render_template, request
from sqlalchemy import desc
from app.core.config import PageTemplate
from app.modules.departments.services import DepartmentService, DepartmentServiceError

# Initialize Blueprint for authentication module
department_bp = Blueprint("department", __name__)

# ======== LOGIN ==========
@department_bp.route("/departments/create", methods=["GET", "POST"])
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
            
    # Render login page for GET requests
    return render_template("home.html", app_config=PageTemplate)