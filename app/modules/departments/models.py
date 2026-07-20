# Importing necessary libraries
from sqlalchemy import Enum, ForeignKey, String, false, null
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from app.modules.departments.roles import DepartmentRole
from app.modules.users.models import User

# Model of departments
class Department(db.Model):

    # Return for utility
    def __repr__(self) -> str:
        return f"<Departments {self.name}>"

    # Table Name
    __tablename__ = "departments"
    
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
        comment="Name of department",
        unique=True,
        nullable=False
    )
    
    # Column DESCRIPTION
    description: Mapped[str] = mapped_column(
        String(100),
        comment="Description of department",
        nullable=False
    )
    
    # Column CREATED_AT
    created_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the department was created",
        default=lambda: datetime.now(timezone.utc),
    )

    # Column UPDATED_AT
    updated_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the department was last updated",
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    
# Model of user assignment on department
class UserDepartment(db.Model):
    # Return for utility
    def __repr__(self) -> str:
        return f"<Departments {self.id}>"
    
    # Table name
    __tablename__ = "user_departments"
    
    # Column ID
    id: Mapped[int] = mapped_column(
        comment="Internal database identifier",
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    
    # Column USER_ID
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        comment="ID from user assignment on department",
        nullable=False,
    )
    
    # Column DEPARTMENT_ID
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID of the department",
    )

    # Column USER_ROLE
    user_role: Mapped[DepartmentRole] = mapped_column(
        Enum(DepartmentRole),
        default=DepartmentRole.USER,
        nullable=False,
        comment="Role of the user in this specific department",
    )
    
    # Column JOINED_AT
    joined_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        comment="Timestamp when the user joined the department",
    )