# Importing necessary libraries
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.core.config import PageTemplate
from app.extensions import db
from app.modules.users.models import User

# Initialize Blueprint for authentication module
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Route responsible for user authentication."""
    if request.method == "POST":
        # Get and sanitize credentials submitted via the form
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password", "")

        # Query the database for the user by email
        user_login = db.session.query(User).filter_by(email=email).first()

        # Validate user existence and check password hash match
        if user_login and check_password_hash(user_login.password_hash, password):
            login_user(user_login)
            flash("Logged in successfully!", "success")
            return redirect(url_for("auth.home"))
        else:
            # Generic message to prevent email/user enumeration
            flash("Invalid email or password.", "error")
            return render_template("auth/login.html", app_config=PageTemplate)

    # Render login page for GET requests
    return render_template("auth/login.html", app_config=PageTemplate)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Route responsible for registering new users."""
    if request.method == "POST":
        # Take the raw data directly from the form.
        raw_first = request.form.get("first_name", "")
        raw_last = request.form.get("last_name", "")
        raw_email = request.form.get("email", "")
        password = request.form.get("password", "")

        # Optional pre-check for duplicate email addresses
        email_normalized = (raw_email or "").strip().lower()
        if db.session.query(User).filter_by(email=email_normalized).first():
            flash("A user with this email address already exists.", "error")
            return render_template("auth/register.html")

        try:
            # AWhen instantiating the User, SQLAlchemy automatically triggers the @validates.
            user_register = User(
                first_name=raw_first,
                last_name=raw_last,
                email=raw_email,
                password_hash=generate_password_hash(password),
            )

            db.session.add(user_register)
            db.session.commit()

            login_user(user_register)
            flash(f"Account successfully created! Welcome, {user_register.first_name}.", "success")
            return redirect(url_for("auth.home"))

        # It catches both @validates errors (ValueError) and database failures.
        except ValueError as ve:
            db.session.rollback()
            flash(str(ve), "error")  # Displays the validator's custom message on the screen.
        except Exception:
            db.session.rollback()
            flash("An error occurred while communicating with the database. Please try again.", "error")

    return render_template("auth/register.html")


@auth_bp.route("/home")
@login_required
def home():
    """Main dashboard page route (requires authentication)."""
    return render_template("home.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """End current logged-in user session."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))