# Importing necessary libraries
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.core.config import PageTemplate
from app.modules.departments.roles import DepartmentRole
from app.modules.users.services import UserService, UserServiceError


# Initialize Blueprint for user module
user_bp = Blueprint("user", __name__)

# ======== DEPARTMENT ADD ==========
@user_bp.route("/user/department/add", methods=["POST"])
@login_required
def user_department_add():
    """Route responsible for create department."""
    
    # Post REQUEST
    if request.method == "POST":
        
        # Get and sanitize data submitted via the form
        user_id = int(request.form["user_id"])
        department_id = int(request.form["department_id"])
        role = DepartmentRole(request.form["role"])
        
        # Trying create
        try:
            
            # New assigned
            UserService.add_department(
                user_id=user_id,
                department_id=department_id,
                role=role
            )
            
            # Feedback for user
            flash(f"User add on department successfully", "success")

        # Except errors
        except UserServiceError as e:
            
            # Return message for user
            flash(f"{e}", "error")
            
            # Redirect to home
    return redirect(url_for("auth.home"))


@user_bp.route("/user/department/delete/<int:id>", methods=["POST"])
def department_delete(id: int):
    """Route for delete assigned"""
    try:
        
        # Delete department
        UserService.delete_department(id)
        
        # Return feedback for user
        flash(f"User has ben unassigned")
     
    except UserServiceError as e:
        # Return feedback for user
        flash(str(e), "error")
    
    # Redirect to home
    return redirect(url_for("auth.home"))