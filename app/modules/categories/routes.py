# Importing necessary libraries
from flask import Blueprint, flash, jsonify, redirect, request, url_for
from flask_login import login_required
from app.modules.categories.models import Category
from app.modules.categories.services import CategoryService, CategoryServiceError
from app.extensions import db

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
                name=name, department_id=department_id, color=color
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
@login_required
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


@categories_bp.route("/get_categories/<int:department_id>", methods=["GET"])
@login_required
def get_categories_by_department(department_id):
    """Return categories of a department in JSON"""
    try:
        
        # Getting category by department
        categories = (
            db.session.query(Category).filter_by(department_id=department_id).all()
        )

        # Category list
        categories_list = [
            {"id": category.id, "name": category.name} for category in categories
        ]

        # Return json model
        return jsonify(categories_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
