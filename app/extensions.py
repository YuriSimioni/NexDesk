# Importing necessary libraries
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Database ORM
db = SQLAlchemy()

# Database migrations
migrate = Migrate()
