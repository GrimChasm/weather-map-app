from liveUSweatherapp import app  # Import the app instance
from liveUSweatherapp import WeatherMap

@app.route('/')
def home():
    return "Hello, Live US Weather App!"
