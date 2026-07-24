# Importing necessary libraries

from flask import Blueprint, flash, redirect, request, url_for
from flask_login import current_user, login_required
from app.extensions import db
from app.modules.tickets.priority import TicketPriority
from app.modules.tickets.services import TicketService, TicketServiceError

# Creating blueprint
ticket_bp = Blueprint("ticket", __name__)


# ======= CREATE_TICKET =======
@ticket_bp.route("/ticket/create", methods=["POST"])
@login_required
def create_ticket():
    """Route for create new ticket"""
    if request.method == "POST":

        # Getting data form
        subject: str = request.form["subject"]
        description: str = request.form["description"]
        assigned_id: int = int(request.form["assigned_to"])
        category_id: int = int(request.form["category_id"])
        priority = TicketPriority(
            request.form.get("priority", TicketPriority.NORMAL.value)
        )

        try:

            # Creating object
            new_ticket = TicketService.create_ticket(
                subject=subject,
                description=description,
                assigned_id=assigned_id,
                category_id=category_id,
                priority=priority,
            )

            # Add on database
            db.session.add(new_ticket)

            # Save changes
            db.session.commit()

            # Return feedback user
            flash("Ticket create successfully", "success")
        except TicketServiceError as e:
            flash(f"{e}", "error")

    # Redirect to home
    return redirect(url_for("auth.home"))


@ticket_bp.route("/ticket/delete/<int:id>", methods=["POST"])
@login_required
def ticket_delete(id: int):
    """Route for delete ticket"""
    try:

        # Delete ticket
        TicketService.delete_ticket(id)

        # Return feedback for user
        flash(f"User has ben unassigned", "success")

    except TicketServiceError as e:
        # Return feedback for user
        flash(str(e), "error")

    # Redirect to home
    return redirect(url_for("auth.home"))


@ticket_bp.route("/ticket/close/<int:id>", methods=["POST"])
@login_required
def ticket_close(id: int):
    """Route for closed ticket"""
    try:

        # Close ticket
        TicketService.close_ticket(id)

        # Return feedback for user
        flash(f"Ticket has ben closed", "success")

    except TicketServiceError as e:
        # Return feedback for user
        flash(str(e), "error")

    # Redirect to home
    return redirect(url_for("auth.home"))


@ticket_bp.route("/ticket/comment", methods=["POST"])
@login_required
def ticket_comment():
    """Route for add comment on ticket"""
    if request.method == "POST":

        # Getting data forms
        ticket_id: int = int(request.form["ticket_id"])
        is_internal = request.form.get("is_internal") is not None
        comment: str = str(request.form["comment"]).strip().capitalize()

        try:

            # Creating object
            new_comment = TicketService.add_comment(
                ticket_id=ticket_id,
                user_id=current_user.id,
                comment=comment,
                is_internal=is_internal,
            )

            # Add on database
            db.session.add(new_comment)

            # Save changes
            db.session.commit()

            # Return feedback user
            flash("Comment added successfully", "success")
        except TicketServiceError as e:
            flash(f"{e}", "error")

    # Redirect to home
    return redirect(url_for("auth.home"))
