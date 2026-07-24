# Importing necessary libraries
import datetime
from datetime import datetime, timezone
from flask_login import current_user
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.modules.categories.services import CategoryService
from app.modules.tickets.models import Ticket
from app.modules.tickets.priority import TicketPriority
from app.modules.users.models import User
from app.modules.users.services import UserService


# Class for exception errors
class TicketServiceError(Exception):
    """Ticket service exception."""

    pass


# Class for Ticket logic
class TicketService:

    @staticmethod
    def create_ticket(
        subject: str,
        description: str,
        assigned_id: int,
        category_id: int,
        priority: TicketPriority = TicketPriority.NORMAL,
    ) -> Ticket:
        """Register new ticket on database"""

        # Scape strings
        subject = subject.capitalize()
        description = description.capitalize()

        # Getter objects
        requester = UserService.user_exists(current_user.id)
        assigned = UserService.user_exists(assigned_id)
        category = CategoryService.category_exists(category_id)

        # Subject with more than 100 characters
        if len(subject) > 100:
            raise TicketServiceError("Subject exceeds 100 characters.")

        # Creating ticket
        ticket = Ticket(
            subject=subject,
            description=description,
            requester_id=requester.id,
            assigned_to=assigned.id,
            category_id=category.id,
            priority=priority,
        )

        # Insert in database
        db.session.add(ticket)

        # Commit on database
        db.session.commit()

        # Return user
        return ticket

    @staticmethod
    def ticket_exists(id: int) -> Ticket:
        """Verify ticket exists"""

        # Search ticket
        ticket = db.session.query(Ticket).filter_by(id=id).first()

        # If not exists
        if not ticket:
            raise TicketServiceError("Ticket not exists.")

        # Return ticket
        return ticket

    @staticmethod
    def get_tickets(id: int) -> list[Ticket]:
        """Return all tickets"""
        return db.session.query(Ticket).all()

    @staticmethod
    def get_user_tickets(id: int) -> list[Ticket]:
        """Return all tickets where user is requester OR assigned to, with category and department"""

        # Verify user exists
        user: User = UserService.user_exists(id=id)

        # Get ticket relation on user
        user_tickets: list[Ticket] = (
            db.session.query(Ticket)
            .options(joinedload(Ticket.category))
            .filter(or_(Ticket.requester_id == user.id, Ticket.assigned_to == user.id))
            .all()
        )

        # Return list tickets
        return user_tickets

    @staticmethod
    def delete_ticket(id: int) -> bool:
        """Delete ticket"""
        # Getting ticket
        ticket: Ticket = TicketService.ticket_exists(id)

        # Deleting from database
        db.session.delete(ticket)

        # Save changes
        db.session.commit()
        return True

    @staticmethod
    def close_ticket(id: int) -> bool:
        """Close ticket"""

        # Verify if ticket exists
        ticket: Ticket = TicketService.ticket_exists(id=id)

        # Add timestamp ticket close
        ticket.closed_at = datetime.now(timezone.utc)

        # Update ticket on database
        db.session.add(ticket)

        # Save changes
        db.session.commit()
        return True
