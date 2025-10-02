# src/time_capsule/weather_assets.py
import os
import pandas as pd
import requests
from dagster import asset
from typing import List, Dict, Any

# Import the shared resource
from .resources import APIResource


# A list of major world cities with their lat/lon coordinates
CITIES = {
    "Tokyo": (35.68, 139.69),
    "New York": (40.71, -74.00),
    "London": (51.50, -0.12),
    "Beijing": (39.90, 116.40),
    "Sydney": (-33.86, 151.20),
}

@asset # This decorator registers the function as a Dagster asset
def raw_weather_data(api: APIResource) -> pd.DataFrame:
    """
    Fetches the current weather for a predefined list of major world cities
    from the OpenWeatherMap API and returns it as a pandas DataFrame.
    """

    # api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    api_key = api.openweathermap_api_key

    if not api_key:
        raise ValueError("OPENWEATHERMAP_API_KEY environment variable not set.")

    processed_data: List[Dict[str, Any]] = []

    print("Fetching weather data for all cities...")
    for city, (lat, lon) in CITIES.items():
        # The API endpoint for current weather data
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

        response = requests.get(url)
        response.raise_for_status()  # This will raise an error if the request failed

        data = response.json()
        
        # Instead of appending the whole JSON, pull out only the fields we want.
        # Use .get() to safely access nested keys that might be missing.
        processed_data.append({
            "city": city,
            "lat": data.get("coord", {}).get("lat"),
            "lon": data.get("coord", {}).get("lon"),
            "timestamp": pd.to_datetime(data.get("dt"), unit="s"),
            "temp": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "temp_min": data.get("main", {}).get("temp_min"),
            "temp_max": data.get("main", {}).get("temp_max"),
            "pressure": data.get("main", {}).get("pressure"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "wind_deg": data.get("wind", {}).get("deg"),
            "weather_main": data.get("weather", [{}])[0].get("main"),
            "weather_description": data.get("weather", [{}])[0].get("description"),
            "country": data.get("sys", {}).get("country"),
        })

    print("Successfully fetched all weather data.")
    # The returned DataFrame will be saved by Dagster's IOManager
    return pd.DataFrame(processed_data)