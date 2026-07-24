# Importing necessary libraries
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.core.config import PageTemplate
from app.modules.auth.services import AuthService, AuthServiceError
from app.modules.categories.services import CategoryService
from app.modules.departments.services import DepartmentService
from app.modules.tickets.services import TicketService
from app.modules.users.services import UserService

# Initialize Blueprint for authentication module
auth_bp = Blueprint("auth", __name__)


# ======== LOGIN ==========
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Route responsible for user authentication."""

    # Post REQUEST
    if request.method == "POST":

        # Get and sanitize credentials submitted via the form
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password", "")

        # Trying make login
        try:

            # User login
            user = AuthService.authenticate(email=email, password=password)

            # Update last_login on database
            AuthService.update_last_login(user=user)

            # Initialization login
            login_user(user)

            # Return message for user
            flash("Logged in successfully!", "success")

            # Redirect to home page
            return redirect(url_for("auth.home"))

        # Except errors
        except AuthServiceError as e:

            # Return message for user
            flash(f"{e}", "error")

    # Render login page for GET requests
    return render_template("auth/login.html", app_config=PageTemplate)


# ======== Route for register disable ===========
# @auth_bp.route("/register", methods=["GET", "POST"])
# def register():
#    """Route responsible for registering new users."""
#    if request.method == "POST":
#        # Take the raw data directly from the form.
#        raw_first = request.form.get("first_name", "")
#        raw_last = request.form.get("last_name", "")
#        raw_email = request.form.get("email", "")
#        password = request.form.get("password", "")
#
#        try:
#            user_register = UserService.create_user(raw_first, raw_last, raw_email, password)
#            login_user(user_register)
#            flash(f"Account successfully created! Welcome,{raw_first}.", "success")
#
#            return redirect(url_for("auth.home"))
#
#        except UserServiceError as e:
#            flash(f"{e}.", "error")
#    return render_template("auth/register.html")


@auth_bp.route("/home")
@login_required
def home():
    """Main dashboard page route (requires authentication)."""

    # Getting all departments
    all_departments = DepartmentService.get_departments()
    all_categories = CategoryService.get_categories_by_department(8)
    all_users = UserService.get_all_users()
    user_tickets = TicketService.get_user_tickets(current_user.id)
    all_tickets = TicketService.get_tickets()
    user_departments = UserService.get_assigned_departments(current_user.id)
    
    return render_template(
        "home.html",
        department_list=all_departments,
        category_list=all_categories,
        user_list=all_users,
        user_departments=user_departments,
        user_tickets=user_tickets,
        ticket_list=all_tickets
    )


@auth_bp.route("/logout")
@login_required
def logout():
    """End current logged-in user session."""

    # Make logout
    logout_user()

    # Feedback message for user
    flash("You have been logged out.", "info")

    # Redirect for login
    return redirect(url_for("auth.login"))
