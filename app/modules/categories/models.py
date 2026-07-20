# Importing necessary libraries
from sqlalchemy import ForeignKey, String, false, null
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime, timezone

# Model of categories
class Category(db.Model):
    
    # Table name
    __tablename__ = "ticket_categories"
    
    # Column ID
    id: Mapped[int] = mapped_column(
        comment="Internal database identifier",
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    
    # Column NAME
    name: Mapped[str] = mapped_column(
        String(50),
        comment="Name category",
        nullable=False
    )
    
    # Column DEPARTMENT_ID
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        comment="Department ID",
        nullable=False
    )
    
    # Column COLOR
    color: Mapped[str] = mapped_column(
        String(10),
        comment="Color for category",
        nullable=False,
    )
    
    # Column CREATED_AT
    created_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the category was created",
        default=lambda: datetime.now(timezone.utc),
    )

    # Column UPDATED_AT
    updated_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the category was last updated",
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    # `__init__` function for better no-code usage
    def __init__(
        self,
        name: str,
        department_id: int,
        color: str,
        **kwargs
        ) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.department_id = department_id
        self.color = color