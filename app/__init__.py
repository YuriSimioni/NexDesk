# Importing necessary libraries
from flask import Flask, redirect, url_for
from rich import print
from sqlalchemy import inspect
from flask_login import LoginManager
from app.core.config import Config
from app.extensions import db, migrate
from app.modules.departments.roles import DepartmentRole
from app.modules.tickets.priority import TicketPriority
from app.modules.tickets.status import TicketStatus
from app.modules.users.roles import UserRole


# Define function for create application
def create_app():

    # Instance application
    app = Flask(__name__)

    # Secret key flask
    app.config["SECRET_KEY"] = Config.SECRET_KEY

    # Inject enums for using in Jinja
    @app.context_processor
    def inject_enums():
        return {
            "UserRole": UserRole,
            "DepartmentRole": DepartmentRole,
            "TicketPriority": TicketPriority,
            "TicketStatus": TicketStatus,
        }

    # Login manager flask login
    lm = LoginManager(app)
    lm.login_view = "auth.login"  # type: ignore

    # Getting ID from session flask login
    @lm.user_loader
    def user_loader(id: int):
        user = db.session.query(User).filter_by(id=id).first()
        return user

    # Loading configurations from class Config in 'app/core/config.py'
    app.config.from_object(Config)

    # Importing models database
    from app.modules.users.models import User
    from app.modules.departments.models import Department, UserDepartment
    from app.modules.categories.models import Category
    from app.modules.tickets.models import Ticket, TicketComment

    # Initialization database
    db.init_app(app)

    # Initialization migrate
    migrate.init_app(app, db)

    # Initializing database model
    with app.app_context():
        print("\n=> [yellow]Initializing database[/yellow]", flush=True)
        print("  -> [purple]Checking and creating tables[/purple]", flush=True)

        # Create inspector for verify tables exist
        inspector = inspect(db.engine)
        tables_exists = inspector.get_table_names()

        # It preserves the state of each table before running create_all.
        status_table = {}
        for table_name in db.metadata.tables.keys():
            if table_name in tables_exists:
                status_table[table_name] = "[blue]already exists[/blue]"
            else:
                status_table[table_name] = "[green]created[/green]"

        # Create table if not exists
        db.create_all()

        # Show final status in terminal
        for table_name in db.metadata.tables.keys():
            status = status_table[table_name]
            print(f"     - [white][u]{table_name}[/u][/white] {status}", flush=True)

        print("\n[bold][green]-> Database is ready for use[/green][/bold]", flush=True)

    # Importing blueprints
    from app.modules.auth.routes import auth_bp
    from app.modules.departments.routes import department_bp
    from app.modules.categories.routes import categories_bp
    from app.modules.users.routes import user_bp
    from app.modules.tickets.routes import ticket_bp

    # Register blueprints in app
    app.register_blueprint(auth_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(ticket_bp)

    # Route index
    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    # Return application
    return app
