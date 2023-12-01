from flask import Flask, render_template, request, redirect, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
import requests
import logging
import os


APP_ENV = os.getenv('APP_ENV', 'development')
DEBUG = APP_ENV

def create_app():
    app = Flask(__name__)
    app.config['ENV'] = APP_ENV  

    # Set up logging
    logging.basicConfig(level=logging.DEBUG if app.config['ENV'] == 'development' else logging.INFO)

    # Construct the MongoDB connection string
                             # "mongodb://weather-app:16042002@mongo-mongodb.mongo.svc.cluster.local:27017/weatherdb"
    print(f"mongodb://{os.getenv('MONGODB_USERNAME')}:{os.getenv('MONGODB_PASSWORD')}@mongo-mongodb.mongo.svc.cluster.local:27017/{os.getenv('MONGODB_DATABASE')}")
    app.config["MONGO_URI"] = f"mongodb://{os.getenv('MONGODB_USERNAME')}:{os.getenv('MONGODB_PASSWORD')}@mongo-mongodb.mongo.svc.cluster.local:27017/{os.getenv('MONGODB_DATABASE')}"

    # MongoDB Setup
    mongo = PyMongo(app)
    app.mongo = mongo

    # Health Check Route
    @app.route('/mongohealth')
    def health_check():
        try:
            # Attempt to connect to MongoDB
            app.mongo.db.command('ping')
            return jsonify({"status": "ok"})
        except Exception as e:
            app.logger.error(f"Health check failed: {str(e)}")
            return jsonify({"status": "error", "message": str(e)}), 500

    return app


app = create_app()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

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
        return render_template("weather.html", forecast=forecast) 
    else:
        error_message = "Unable to retrieve the forecast for {}".format(place)
        return render_template("index.html", error_message=error_message)


if __name__ == '__main__':
    app.run(debug=DEBUG)
