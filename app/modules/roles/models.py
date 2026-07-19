# Importing necessary libraries
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from sqlalchemy import String
from datetime import datetime, timezone

# Model of roles
class Roles(db.Model):
    
    def __repr__(self) -> str:
        return f"<Role {self.name}>"
    
    # Table name
    __tablename__ = "roles"
    
    # Column ID
    id: Mapped[int] = mapped_column(
        comment="Internal database identifier",
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    
    # Column NAME
    name: Mapped[str] = mapped_column(
        String(50),
        comment="Name for role",
        unique=True,
        nullable=False
    )
    
    # Column DESCRIPTION
    description: Mapped[str] = mapped_column(
        String(100),
        comment="Description for role",
        nullable=False
    )
    
    # Column CREATED_AT
    created_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the role was created",
        default=lambda: datetime.now(timezone.utc),
    )

    # Column UPDATED_AT
    updated_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the role was last updated",
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )