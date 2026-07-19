from app.core.database import Database
from app.core.env_loader import EnvLoader
 

database = Database()


class Config:
    """
    Flask application configuration.
    """


    SECRET_KEY = EnvLoader.get(
        "FLASK_SECRET_KEY"
    )


    SQLALCHEMY_DATABASE_URI = database.uri


    SQLALCHEMY_TRACK_MODIFICATIONS = False