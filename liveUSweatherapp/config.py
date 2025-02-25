import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
