from flask import render_template
from liveUSweatherapp import app
from liveUSweatherapp.weather import WeatherMap  # Import WeatherMap class
import plotly.io as pio

@app.route('/')
def home():
    # Fetch weather data and create map
    weather = WeatherMap()
    data = weather.fetch_weather_data()
    fig = weather.create_map(data)

    # Convert Plotly figure to JSON
    graph_json = pio.to_json(fig)

    return render_template('index.html', graph_json=graph_json)
