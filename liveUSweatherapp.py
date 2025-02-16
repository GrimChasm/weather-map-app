import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import os
from dotenv import load_dotenv
from config import Config  # Import config settings
from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio
from weather_map import WeatherMap  # Import your WeatherMap class

app = Flask(__name__)

@app.route('/')
def home():
    # Fetch weather data
    weather = WeatherMap()
    data = weather.fetch_weather_data()
    fig = weather.create_map(data)

    # Convert Plotly figure to JSON
    graph_json = pio.to_json(fig)

    # Pass JSON to the template
    return render_template('index.html', graph_json=graph_json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)





# Load environment variables
load_dotenv()

class WeatherMap:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("No API key found. Please set OPENWEATHER_API_KEY environment variable.")
        
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Cities remain the same as before...
        self.cities = {
            "New York": {"lat": 40.7128, "lon": -74.0060},
            "Los Angeles": {"lat": 34.0522, "lon": -118.2437},
            "Chicago": {"lat": 41.8781, "lon": -87.6298},
            "Houston": {"lat": 29.7604, "lon": -95.3698},
            "Phoenix": {"lat": 33.4484, "lon": -112.0740},
            "Philadelphia": {"lat": 39.9526, "lon": -75.1652},
            "San Antonio": {"lat": 29.4241, "lon": -98.4936},
            "San Diego": {"lat": 32.7157, "lon": -117.1611},
            "Dallas": {"lat": 32.7767, "lon": -96.7970},
            "San Jose": {"lat": 37.3382, "lon": -121.8863},
            "Miami": {"lat": 25.7617, "lon": -80.1918},
            "Seattle": {"lat": 47.6062, "lon": -122.3321},
            "Denver": {"lat": 39.7392, "lon": -104.9903},
            "Boston": {"lat": 42.3601, "lon": -71.0589},
            "Las Vegas": {"lat": 36.1699, "lon": -115.1398},
            "Portland": {"lat": 45.5155, "lon": -122.6789},
            "Atlanta": {"lat": 33.7490, "lon": -84.3880},
            "New Orleans": {"lat": 29.9511, "lon": -90.0715},
            "Detroit": {"lat": 42.3314, "lon": -83.0458},
            "Minneapolis": {"lat": 44.9778, "lon": -93.2650},
            "Salt Lake City": {"lat": 40.7608, "lon": -111.8910},
            "Austin": {"lat": 30.2672, "lon": -97.7431},
            "Nashville": {"lat": 36.1627, "lon": -86.7816},
            "San Francisco": {"lat": 37.7749, "lon": -122.4194},
            "Kansas City": {"lat": 39.0997, "lon": -94.5786},
            "St. Louis": {"lat": 38.6270, "lon": -90.1994},
            "Sacramento": {"lat": 38.5816, "lon": -121.4944},
            "Orlando": {"lat": 28.5383, "lon": -81.3792},
            "Cleveland": {"lat": 41.4993, "lon": -81.6944},
            "Pittsburgh": {"lat": 40.4406, "lon": -79.9959}
        }

        # Define weather condition colors
        self.condition_colors = {
            'Clear': '#FFD700',      # Gold
            'Clouds': '#A9A9A9',     # Dark Gray
            'Rain': '#4169E1',       # Royal Blue
            'Snow': '#FFFFFF',       # White
            'Thunderstorm': '#4B0082',  # Indigo
            'Drizzle': '#87CEEB',    # Sky Blue
            'Mist': '#D3D3D3',       # Light Gray
            'Fog': '#C0C0C0',        # Silver
            'Haze': '#F0E68C',       # Khaki
            'Smoke': '#696969',      # Dim Gray
        }

    def get_condition_icon(self, condition):
        """Return emoji for weather condition"""
        icons = {
            'Clear': '☀️',
            'Clouds': '☁️',
            'Rain': '🌧️',
            'Snow': '❄️',
            'Thunderstorm': '⛈️',
            'Drizzle': '🌦️',
            'Mist': '🌫️',
            'Fog': '🌫️',
            'Haze': '🌫️',
            'Smoke': '🌫️'
        }
        return icons.get(condition, '❓')

    def fetch_weather_data(self):
        """Fetch real weather data from OpenWeatherMap API"""
        weather_data = []
        
        for city, coords in self.cities.items():
            params = {
                "lat": coords["lat"],
                "lon": coords["lon"],
                "appid": self.api_key,
                "units": "imperial"
            }
            
            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                weather_info = {
                    "city": city,
                    "lat": coords["lat"],
                    "lon": coords["lon"],
                    "temperature": round(data["main"]["temp"], 1),
                    "condition": data["weather"][0]["main"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "feels_like": round(data["main"]["feels_like"], 1),
                    "condition_icon": self.get_condition_icon(data["weather"][0]["main"]),
                    "condition_color": self.condition_colors.get(data["weather"][0]["main"], '#808080')
                }
                
                weather_data.append(weather_info)
                print(f"Successfully fetched data for {city}")
                
                time.sleep(1)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {city}: {e}")
                continue
            
        return pd.DataFrame(weather_data)

    def create_map(self, data):
        """Create an interactive map visualization with improved text layout"""
        fig = go.Figure()

        # Add weather data points with improved text formatting
        fig.add_trace(go.Scattergeo(
            lon=data['lon'],
            lat=data['lat'],
            text=data.apply(
                lambda row: (
                    f"{row['city']}<br>"
                    f"{row['temperature']}°F<br>"
                    f"{row['condition']}<br>"
                    f"{row['wind_speed']} mph"
                ),
                axis=1
            ),
            mode='markers+text',
            marker=dict(
                size=15,
                color=data['temperature'],  # Using temperature for color instead of condition
                colorscale='RdYlBu_r',      # Red-Yellow-Blue color scale (reversed)
                showscale=True,
                colorbar_title="Temperature (°F)",
                symbol='circle',
                line=dict(
                    color='white',
                    width=1
                ),
                opacity=0.8
            ),
            textposition="top center",
            textfont=dict(
                size=10,
                color='black',
                family='Arial'
            ),
            hovertext=data.apply(
                lambda row: (
                    f"<b>{row['city']}</b><br>"
                    f"Temperature: {row['temperature']}°F<br>"
                    f"Feels like: {row['feels_like']}°F<br>"
                    f"Condition: {row['condition']}<br>"
                    f"Humidity: {row['humidity']}%<br>"
                    f"Wind: {row['wind_speed']} mph"
                ),
                axis=1
            ),
            hoverinfo="text"
        ))

        # Update layout with improved text handling
        fig.update_layout(
            title={
                'text': '🌡️ Live US Weather Map 🌤️',
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(
                    size=24,
                    color='#1E88E5',
                    family='Arial'
                )
            },
            geo=dict(
                scope='usa',
                projection_type='albers usa',
                showland=True,
                landcolor='#E8F5E9',
                countrycolor='#81C784',
                showlakes=True,
                lakecolor='#B3E5FC',
                subunitcolor='#C8E6C9',
                showcoastlines=True,
                coastlinecolor='#43A047',
                showocean=True,
                oceancolor='#E3F2FD',
                showrivers=True,
                rivercolor='#42A5F5',
                bgcolor='#F5F5F5',
                center=dict(
                    lat=39.5,
                    lon=-98.35
                ),
                projection=dict(
                    scale=4.5
                )
            ),
            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#FFFFFF',
            height=800,
            margin=dict(l=0, r=0, t=30, b=0),
            annotations=[
                dict(
                    text=f"Last Updated: {datetime.now().strftime('%I:%M %p')}",
                    showarrow=False,
                    x=0.01,
                    y=0.99,
                    xref='paper',
                    yref='paper',
                    font=dict(
                        size=12,
                        color='#666666',
                        family='Arial'
                    )
                )
            ]
        )

        return fig

    def fetch_weather_data(self):
        """Fetch real weather data from OpenWeatherMap API"""
        weather_data = []
        
        for city, coords in self.cities.items():
            params = {
                "lat": coords["lat"],
                "lon": coords["lon"],
                "appid": self.api_key,
                "units": "imperial"
            }
            
            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                weather_info = {
                    "city": city,
                    "lat": coords["lat"],
                    "lon": coords["lon"],
                    "temperature": round(data["main"]["temp"], 1),
                    "condition": data["weather"][0]["main"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "feels_like": round(data["main"]["feels_like"], 1)
                }
                
                weather_data.append(weather_info)
                print(f"Successfully fetched data for {city}")
                
                time.sleep(1)
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for {city}: {e}")
                continue
            
        return pd.DataFrame(weather_data)

    def update_display(self, update_interval=300):
        """Update the weather display at specified interval"""
        while True:
            try:
                data = self.fetch_weather_data()
                fig = self.create_map(data)
                fig.show()
                
                print(f"\nNext update in {update_interval} seconds...")
                time.sleep(update_interval)
                
            except Exception as e:
                print(f"Error updating display: {e}")
                print("Retrying in 60 seconds...")
                time.sleep(60)

def main():
    try:
        weather_map = WeatherMap()
        weather_map.update_display()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set up your API key first.")

if __name__ == "__main__":
    main()
