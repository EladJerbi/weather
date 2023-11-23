import os
import shutil
import unittest
from unittest.mock import patch

# Define the directories
LOG_DIRECTORY = '/home/weather/weather-app/logs'  
HISTORY_DIR = '/home/weather/weather-app/history' 

# Create the directories before importing the app module
os.makedirs(LOG_DIRECTORY, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)

from app import convert_temperature, get_weather, Forecast

class ConvertTemperatureTestCase(unittest.TestCase):

    def test_convert_temperature(self):
        # Test that the function correctly converts a temperature from Kelvin to Celsius
        self.assertEqual(convert_temperature(273.15), 0)
        self.assertEqual(convert_temperature(300), 27)

@patch('requests.get')
class GetWeatherTestCase(unittest.TestCase):

    def test_get_weather(self, mock_get):
        # Define a mock response object with a status_code property and a json method
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "city": {"country": "US", "name": "New York"},
            "list": [
                {"dt_txt": "2022-01-01 09:00:00", "main": {"temp": 273.15, "humidity": 50}, "weather": [{"icon": "01d"}]},
                {"dt_txt": "2022-01-01 21:00:00", "main": {"temp": 273.15, "humidity": 50}, "weather": [{"icon": "01n"}]},
            ],
        }

        # Set the return value of requests.get
        mock_get.return_value = mock_response

        # Call the function with a sample input
        days = get_weather("new york")

        # Convert the Forecast objects to dictionaries
        days = [day.__dict__ if isinstance(day, Forecast) else day for day in days]

        # Define the expected output
        expected = [
            "US",
            "New York",
            {"weather_date": "01-01 09:00:00", "temperature": 0, "humidity": 50, "icon": "https://openweathermap.org/img/wn/01d@2x.png"},
            {"weather_date": "01-01 21:00:00", "temperature": 0, "humidity": 50, "icon": "https://openweathermap.org/img/wn/01n@2x.png"},
        ]

        # Assert that the function's output matches the expected output
        self.assertEqual(days, expected)


class TestApp(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(LOG_DIRECTORY, ignore_errors=True)
        shutil.rmtree(HISTORY_DIR, ignore_errors=True)

if __name__ == '__main__':
    unittest.main()