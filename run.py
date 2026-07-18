# Importing necessary libraries
from app import create_app

# Application initialization
if __name__ == "__main__":
    
    # Instantiating application
    app = create_app()
    
    # Run application
    app.run(
        host="127.0.0.1", # Host
        port=8080,        # Port
        debug=False,      # Debug mode
    )
    