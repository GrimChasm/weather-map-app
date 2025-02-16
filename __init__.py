from flask import Flask

app = Flask(__name__)

from liveUSweatherapp import routes  # Import routes after creating app
