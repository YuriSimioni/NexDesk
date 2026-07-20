# Importing necessary libraries
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from sqlalchemy import Enum as SQLEnum, ForeignKey, String, null, text
from uuid import uuid4
from app.modules.tickets.priority import TicketPriority
from app.modules.tickets.status import TicketStatus
from datetime import datetime, timezone
# Model of ticket
class Ticket(db.Model):
    
    # Table name
    __tablename__ = "tickets"
    
    # Column ID
    id: Mapped[int] = mapped_column(
        comment="Internal database identifier",
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    
    # Column UUID
    uuid: Mapped[str] = mapped_column(
        String(36),
        comment="UUID for external ticket identification",
        unique=True,
        nullable=False,
        default=lambda: str(uuid4()),
        server_default=text("(UUID())")
    )
    
    # Column SUBJECT
    subject: Mapped[str] = mapped_column(
        String(50),
        comment="Subject ticket",
        nullable=False
    )
    
    # Column DESCRIPTION
    description: Mapped[str] = mapped_column(
        String(255),
        comment="Description for ticket",
        nullable=False
    )
    
    # Column REQUESTER_ID
    requester_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        comment="Requesting user ID",
        nullable=False
    )
    
    # Column ASSIGNED_TO
    assigned_to: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        comment="Solver user ID",
        nullable=True,
        default=None
    )
    
    # Column DEPARTMENT_ID
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        comment="Department ID",
        nullable=False
    )
    
    # Column CATEGORY_ID
    category_id: Mapped[int] = mapped_column(
        ForeignKey("ticket_categories.id"),
        comment="Category ID for ticket"
    )
    
    # Column PRIORITY
    priority: Mapped[TicketPriority] = mapped_column(
        SQLEnum(TicketPriority),
        comment="Priority of ticket",
        default=TicketPriority.NORMAL,
        nullable=False
    )
    
    # Column STATUS
    status: Mapped[TicketStatus] = mapped_column(
        SQLEnum(TicketStatus),
        comment="Status of ticket",
        default=TicketStatus.OPEN,
        nullable=False
    )
    
    # Column CREATED_AT
    created_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the ticket was created",
        default=lambda: datetime.now(timezone.utc),
    )

    # Column UPDATED_AT
    updated_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the ticket was last updated",
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    # Column CLOSED_AT
    closed_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the ticket was closed",
        nullable=True,
    )
    
    # `__init__` function for better no-code usage
    def __init__(
            self,
            subject: str,
            description: str,
            requester_id: int,
            department_id: int,
            category_id: int,
            assigned_to: int | None = None,
            priority: TicketPriority = TicketPriority.NORMAL,
            status: TicketStatus = TicketStatus.OPEN,
            **kwargs
        ) -> None:
            super().__init__(**kwargs)
            self.subject = subject
            self.description = description
            self.requester_id = requester_id
            self.department_id = department_id
            self.category_id = category_id
            self.assigned_to = assigned_to
            self.priority = priority
            self.status = status