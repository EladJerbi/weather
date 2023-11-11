# config.py
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()
# Get the value of an environment variable
HISTORY_DIR = os.getenv('HISTORY_DIR', '/weather-history')
APP_ENV = os.getenv('APP_ENV', 'development')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
LOG_DIRECTORY = os.getenv('LOG_DIRECTORY', '/var/log/weather-app-logs')
DEBUG = APP_ENV == 'development'