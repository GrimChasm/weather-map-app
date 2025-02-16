from liveUSweatherapp import app  # Import the app instance

@app.route('/')
def home():
    return "Hello, Live US Weather App!"
