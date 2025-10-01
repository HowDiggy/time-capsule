# tests/test_assets.py
import os
import pandas as pd
import requests
from unittest.mock import MagicMock

# Import the asset we want to test
from time_capsule.assets import raw_weather_data

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

    # 3. Use pytest's `monkeypatch` to replace the real `requests.get`
    # with our mock function for the duration of this test.
    monkeypatch.setattr(requests, "get", mock_get)
    
    # Also set a dummy environment variable for the API key
    monkeypatch.setenv("OPENWEATHERMAP_API_KEY", "dummy_key")

    # 4. Now, call the asset function. It will use our mock instead of
    # making a real network call.
    result_df = raw_weather_data()

    # 5. Assert that the output is what we expect.
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == 5 # The real asset fetches 5 cities
    assert "city" in result_df.columns
    assert result_df.loc[result_df['city'] == 'Tokyo']['main'].iloc[0]['temp'] == 15.0
