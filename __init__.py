from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Import configurations if needed
app.config.from_object('config.Config')  # Ensure you have a config.py file

# Import routes at the end to avoid circular imports
from liveUSweatherapp import routes
