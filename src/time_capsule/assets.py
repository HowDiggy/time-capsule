# src/time_capsule/assets.py
import os
import pandas as pd
import requests
from dagster import asset
from typing import List, Dict, Any

# A list of major world cities with their lat/lon coordinates
CITIES = {
    "Tokyo": (35.68, 139.69),
    "New York": (40.71, -74.00),
    "London": (51.50, -0.12),
    "Beijing": (39.90, 116.40),
    "Sydney": (-33.86, 151.20),
}

@asset # This decorator registers the function as a Dagster asset
def raw_weather_data() -> pd.DataFrame:
    """
    Fetches the current weather for a predefined list of major world cities
    from the OpenWeatherMap API and returns it as a pandas DataFrame.
    """

    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHERMAP_API_KEY environment variable not set.")

    all_weather_data: List[Dict[str, Any]] = []

    print("Fetching weather data for all cities...")
    for city, (lat, lon) in CITIES.items():
        # The API endpoint for current weather data
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

        response = requests.get(url)
        response.raise_for_status()  # This will raise an error if the request failed

        data = response.json()
        data['city'] = city # Add the city name to the data
        all_weather_data.append(data)

    print("Successfully fetched all weather data.")
    # The returned DataFrame will be saved by Dagster's IOManager
    return pd.DataFrame(all_weather_data)