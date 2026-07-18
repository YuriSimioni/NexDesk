# Importing necessary libraries
from flask import Flask

# Define function for create application
def create_app():
    
    # Instance application
    app = Flask(__name__)
    
    # Route index
    @app.route("/")
    def index():
        return "Hello World" # Return 'Hello World'
        
    
    # Return application
    return app