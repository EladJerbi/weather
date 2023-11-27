from flask import Flask, render_template, request, redirect, send_from_directory, abort
from datetime import datetime
import requests
import os
import json
import logging
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from prometheus_flask_exporter import PrometheusMetrics


# Get the value of an environment variable
HISTORY_DIR = os.getenv('HISTORY_DIR', '/home/weather/weather-app/history')
APP_ENV = os.getenv('APP_ENV', 'development')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
LOG_DIRECTORY = os.getenv('LOG_DIR', '/home/weather/weather-app/logs')
DEBUG = APP_ENV == 'development'

# turn this file to flask app.
app = Flask(__name__)
app.config['ENV'] = APP_ENV  # Set your desired environment here

# custom metrics for Prometheus
city_views = Counter('city_views', 'Number of times each city has been looked at', ['city'])
metrics = PrometheusMetrics(app)

# check if LOG_DIRECTORY exists
if not os.path.exists(LOG_DIRECTORY):
    logging.error(f"Required directory {LOG_DIRECTORY} does not exist")
    raise FileNotFoundError(f"Required directory {LOG_DIRECTORY} does not exist")
# log to file
start_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_path = f'{LOG_DIRECTORY}/app_{start_date}.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s : %(message)s')


class Forecast:
    def __init__(self, weather_date, temperature, humidity, icon):
        self.weather_date = weather_date
        self.temperature = temperature
        self.humidity = humidity
        self.icon = icon
        
    def __str__(self):
        # Define the string representation of the object
        return f"Weather Date: {self.weather_date}, Temperature: {self.temperature}, Humidity: {self.humidity}, Icon: {self.icon}"
    
    def to_dict(self):
        return {
            "weather_date": self.weather_date,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "icon": self.icon,
    }

def convert_temperature(temperature_kelvin):
    temperature_celsius = temperature_kelvin - 273.15
    return round(temperature_celsius)

def get_weather(place):
    city_name = place.capitalize()
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={WEATHER_API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        # Request was successful
        weather_data = response.json()
        days = list()
        days.append(weather_data["city"]["country"])
        days.append(weather_data["city"]["name"])
        
        for item in weather_data["list"]:
            string = item["dt_txt"]
            hour = string[11:]
            if "09:00:00" == hour or "21:00:00" == hour:
                day = Forecast(
                    string[5:],
                    convert_temperature(item["main"]["temp"]),
                    item["main"]["humidity"],
                    f"https://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png"
                )
                days.append(day)
        return days
    else:
        logging.error(f"Failed to get weather data for {city_name}. Status code: {response.status_code}")
        raise Exception(f"Failed to get weather data for {city_name}. Status code: {response.status_code}")


if not os.path.exists(HISTORY_DIR):
    logging.error(f"Required directory {HISTORY_DIR} does not exist")
    raise FileNotFoundError(f"Required directory {HISTORY_DIR} does not exist")

# Define a function to save search queries to a JSON file
def save_search_query(days):
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    if len(days) > 2:
        city = days[1]

        # Generate a unique filename based on date and city
        filename = f"{city.replace(' ', '_')}_{now.strftime('%Y%m%d%H%M%S')}.json"

        # Extract forecast data (excluding the first two elements)
        forecast_data = []
        for day in days[2:]:
            forecast_data.append({
                "weather_date": day.weather_date,
                "temperature": day.temperature,
                "humidity": day.humidity,
            })

        # Create the query data with just the forecast data
        query_data = {
            "date": date_string,
            "city": city,
            "forecast": forecast_data,
        }

        # Write the query data to the JSON file
        with open(os.path.join(HISTORY_DIR, filename), "w") as file:
            json.dump(query_data, file, indent=4)


@app.context_processor
def inject_bg_color():
    return dict(bg_color=os.environ.get('BG_COLOR', '#B2ABBF'))


@app.errorhandler(Exception)
def error(e):
    error_message = str(e)
    logging.error(f"Error fetching weather data: {error_message}")
    
    # You can pass the error message to the template
    return render_template("error.html", error_message=error_message)
    
    
@app.route("/")
def home():
    logging.info("Home route accessed")
    return render_template("index.html")


@app.route("/weather")
def weather():
    place = request.args.get("place")

    if not place:
        return redirect("/")

    forecast = get_weather(place.capitalize())

    if forecast:
        try:
            # Save the request in a file
            save_search_query(forecast)
        except Exception as e:
            # Handle the exception, e.g., log the error message
            logging.error(f"Error while saving search query: {e}")
        
        return render_template("weather.html", forecast=forecast)
        
    else:
        error_message = "Unable to retrieve the forecast for {}".format(place)
        return render_template("index.html", error_message=error_message)


@app.route("/history")
def history():
    # Directly get all JSON files
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith('.json')]
    return render_template("history.html", files=files)


@app.route("/history/<filename>")
def download_file(filename):
    file_path = os.path.join(HISTORY_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(directory=HISTORY_DIR, path=filename, as_attachment=True)
    else:
        abort(404)


# custom metrics route
@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(debug=DEBUG)
