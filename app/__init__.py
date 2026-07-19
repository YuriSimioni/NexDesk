# Importing necessary libraries
from flask import Flask
from app.core.config import Config
from app.extensions import db, migrate
from rich import print
from sqlalchemy import inspect


# Define function for create application
def create_app():
    
    # Instance application
    app = Flask(__name__)
    
    # Loading configurations from class Config in 'app/core/config.py'
    app.config.from_object(
        Config
    )
    
    # Importing models database
    from app.modules.users.models import User
    from app.modules.roles.models import Roles
    
    # Initialization database
    db.init_app(app)
    
    # Initialization migrate
    migrate.init_app(
        app,
        db
    )
    
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
    
    
    # Route index
    @app.route("/")
    def index():
        return "Hello World" # Return 'Hello World'
        
    
    # Return application
    return app