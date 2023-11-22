import unittest
from unittest.mock import patch
from weather.app import convert_temperature, get_weather

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

        # Define the expected output
        expected = [
            "US",
            "New York",
            {"weather_date": "01-01 09:00:00", "temperature": 0, "humidity": 50, "icon": "https://openweathermap.org/img/wn/01d@2x.png"},
            {"weather_date": "01-01 21:00:00", "temperature": 0, "humidity": 50, "icon": "https://openweathermap.org/img/wn/01n@2x.png"},
        ]

        # Assert that the function's output matches the expected output
        self.assertEqual(days, expected)

if __name__ == '__main__':
    unittest.main()