# tests/test_financial_assets.py
import pandas as pd
import requests
from unittest.mock import MagicMock

# Import the asset and resource to be tested
from time_capsule.financial_assets import raw_stock_data, TICKERS
from time_capsule.resources import APIResource

def test_raw_stock_data(monkeypatch):
    """
    Tests the raw_stock_data asset by mocking the Alpha Vantage API call.
    """
    # 1. Define the fake data we want the mock API to return.
    # This mimics the structure of the Alpha Vantage response.
    mock_api_data = {
        "Time Series (Daily)": {
            "2025-10-01": {
                "1. open": "150.00",
                "2. high": "155.00",
                "3. low": "149.00",
                "4. close": "154.50",
                "5. volume": "1234567"
            }
        }
    }

    # 2. Create a mock function to replace requests.get.
    def mock_get(url):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = mock_api_data
        return mock_resp

    # 3. Patch `requests.get` where it's used: in the financial_assets module.
    monkeypatch.setattr("time_capsule.financial_assets.requests.get", mock_get)

    # 4. Create a mock instance of your APIResource for the test.
    mock_api_resource = APIResource(
        openweathermap_api_key="dummy_weather_key",
        alphavantage_api_key="dummy_stock_key"
    )

    # 5. Call the asset function with the mock resource.
    result_df = raw_stock_data(api=mock_api_resource)

    # 6. Assert that the output is what we expect.
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) == len(TICKERS)
    assert "ticker" in result_df.columns
    assert result_df.iloc[0]["close"] == 154.50