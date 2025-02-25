from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Import routes inside function to avoid circular import
    with app.app_context():
        from liveUSweatherapp import routes  
    
    return app
