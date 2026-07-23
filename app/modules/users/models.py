# Importing necessary libraries
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column, validates
from app.extensions import db
from sqlalchemy import String, text, Enum as SQLEnum
from app.modules.users.roles import UserRole
from flask_login import UserMixin
from sqlalchemy.orm import relationship



# Model of users
class User(UserMixin, db.Model):

    # Table Name
    __tablename__ = "users"
    
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
        comment="UUID for external user identification",
        unique=True,
        nullable=False,
        default=lambda: str(uuid4()),
        server_default=text("(UUID())")
    )
    
    # Column FIRST_NAME (name display on system)
    first_name:Mapped[str] = mapped_column(
        String(50),
        comment="First name user",
        nullable=False
    )
    
    # Column LAST_NAME (last name display on system)
    last_name: Mapped[str] = mapped_column(
        String(100),
        comment="Last name user",
        nullable=False
    )
    
    # Column EMAIL
    email: Mapped[str] = mapped_column(
        String(255),
        comment="Email for login",
        unique=True,
        nullable=False,
        index=True
    )
    
    # Column PASSWORD_HASH
    password_hash: Mapped[str] = mapped_column(
        String(255),
        comment="Password hash for login",
        nullable=False
    )
    
    # Column ACCOUNT_IS_ACTIVE
    account_is_active: Mapped[bool] = mapped_column(
        comment="User can access system",
        default=True,
        nullable=False
    )
    
    # Column ROLE
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        comment="User role in system",
        default=UserRole.USER,
        nullable=False
    )
    
    # Column LAST_LOGIN
    last_login_at: Mapped[datetime | None] = mapped_column(
        comment="Timestamp of the user last successful login",
        nullable=True
    )
    
    # Column CREATED_AT
    created_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the user was created",
        default=lambda: datetime.now(timezone.utc),
    )

    # Column UPDATED_AT
    updated_at: Mapped[datetime] = mapped_column(
        comment="Timestamp when the user was last updated",
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    
    
    # Added relationship on user
    user_departments = relationship(
        "UserDepartment",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    
    
    # Validations
    @validates("email")
    def validate_email(self, key, email):

        # Email is not empty
        if email is None:
            raise ValueError("Email cannot be None.")

        return email
    
    # `__init__` function for better no-code usage
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password_hash: str,
        account_is_active: bool = True,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.account_is_active = account_is_active
        
    # Return for utility
    def __repr__(self) -> str:
        return f"<User {self.email}>"