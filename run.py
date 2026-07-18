# Importing necessary libraries
from app import create_app
from app.core.env_loader import EnvLoader

# Application initialization
if __name__ == "__main__":
    
    # Instantiating application
    app = create_app()
    
    # Run application
    app.run(
        host=EnvLoader.get("APP_HOST"),             # Host
        port=EnvLoader.get_int("APP_PORT"),         # Port
        debug=EnvLoader.get_bool("APP_DEBUG"),      # Debug mode
    )
    