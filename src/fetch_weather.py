import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from .logger import get_logger
logger = get_logger(__name__)

load_dotenv()
API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

def get_weather_data(api_key, city = "Delhi", days=7):
    """
    Fetch weather data for the next 'days' days for a given city using OpenWeatherMap API.
    
    Parameters:
    api_key (str): Your OpenWeatherMap API key.
    city (str): The city for which to fetch the weather data.
    days (int): Number of days to fetch the weather data for (default is 7).
    
    Returns:
    list: A list of dictionaries containing weather data for each day.
    """
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        print(f"Error fetching data: {data['message']}")
        logger.error(f"Error fetching weather: {data}")
    logger.info(f"Fetched weather data for {city}")
    print(f"Fetched weather data for {city}")
    return {
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "wind_direction": data["wind"].get("deg", None),
        "precipitation": data.get("rain", {}).get("1h", 0.0),  # can be "snow" for snowfall
        "cloud_coverage": data["clouds"]["all"],
        "weather_condition": data["weather"][0]["main"]
    }
    

