# Importing necessary libraries
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

# Declarative base for SQLAlchemy
class Base(DeclarativeBase):
    pass

# Database ORM
db = SQLAlchemy(model_class=Base)

# Database migrations
migrate = Migrate()
