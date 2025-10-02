# tests/test_weather_assets.py
import os
import pandas as pd
import requests
from unittest.mock import MagicMock

# Import the asset we want to test
from time_capsule.weather_assets import raw_weather_data, CITIES
from time_capsule.weather_assets import APIResource

def test_raw_weather_data(monkeypatch):
    """
    Tests the raw_weather_data asset by mocking the requests.get call.
    """
    # 1. Define the fake data we want the API to return.
    # This mimics the structure of the real OpenWeatherMap API response.
    mock_api_data = {
        "Tokyo": {"main": {"temp": 15.0}, "city": "Tokyo"},
        "New York": {"main": {"temp": 12.0}, "city": "New York"},
    }

    # 2. Create a mock function to replace `requests.get`.
    # This function will be called instead of the real one.
    def mock_get(url):
        # Create a mock response object
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None

        # Return a different fake response depending on the URL
        if "lat=35.68" in url: # Tokyo
            mock_resp.json.return_value = mock_api_data["Tokyo"]
        elif "lat=40.71" in url: # New York
            mock_resp.json.return_value = mock_api_data["New York"]
        else: # Default for any other cities in the real list
            mock_resp.json.return_value = {"main": {"temp": 10.0}}
        
        return mock_resp

    # Patch `requests.get` specifically where it is used: in the weather_assets module.
    monkeypatch.setattr("time_capsule.weather_assets.requests.get", mock_get)

    # 3. Create a mock instance of your APIResource for the test
    mock_api_resource = APIResource(
        openweathermap_api_key="dummy_weather_key",
        alphavantage_api_key="dummy_stock_key"
    )

    # 4. Now, call the asset function. It will use our mock instead of
    # making a real network call.
    result_df = raw_weather_data(api=mock_api_resource)

    # 5. Assert that the output is what we expect.
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == len(CITIES) # The real asset fetches 5 cities
    assert "city" in result_df.columns
    assert result_df.loc[result_df['city'] == 'Tokyo']['temp'].iloc[0] == 15.0
