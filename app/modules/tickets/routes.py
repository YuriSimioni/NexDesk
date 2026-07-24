# Importing necessary libraries
from flask import Blueprint, flash, jsonify, redirect, request, url_for
from flask_login import login_required
from app.extensions import db
from app.modules.categories.models import Category
from app.modules.tickets.priority import TicketPriority
from app.modules.tickets.services import TicketService, TicketServiceError

# Creating blueprint
ticket_bp = Blueprint("ticket", __name__)

# ======= CREATE_TICKET =======
@ticket_bp.route("/ticket/create", methods=["POST"])
def create_ticket():
    
    if request.method == "POST":
        
        subject: str = request.form["subject"]
        description: str = request.form["description"]
        assigned_id: int = int(request.form["assigned_to"])
        category_id: int = int(request.form["category_id"])
        priority = TicketPriority(request.form.get("priority", TicketPriority.NORMAL.value))
        
        try:
            
            # Creating object
            new_ticket = TicketService.create_ticket(
                subject=subject,
                description=description,
                assigned_id=assigned_id,
                category_id=category_id,
                priority=priority
            )
            
            # Add on database
            db.session.add(new_ticket)
            
            # Save changes
            db.session.commit()
            
            # Return feedback user
            flash("Ticket create successfully")
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
        flash(f"User has ben unassigned")
     
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
        flash(f"Ticket has ben closed")
     
    except TicketServiceError as e:
        # Return feedback for user
        flash(str(e), "error")
    
    # Redirect to home
    return redirect(url_for("auth.home"))