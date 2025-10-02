# src/time_capsule/financial_assets.py
import os
import pandas as pd
import requests
from dagster import asset
from typing import List, Dict, Any

# Import the shared resource
from .resources import APIResource

TICKERS = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA"]
@asset
def raw_stock_data(api: APIResource) -> pd.DataFrame:
    """
    Fetches the daily time series for a list of stock tickers from the
    Alpha Vantage API and returns it as a pandas DataFrame.
    """
    # api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    api_key = api.alphavantage_api_key

    if not api_key:
        raise ValueError("ALPHAVANTAGE_API_KEY environment variable not set.")

    all_stock_data: List[Dict[str, Any]] = []

    print("Fetching stock data for all tickers...")
    for ticker in TICKERS:
        # The API endpoint for daily time series data
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # The free API is limited, so check for a note.
        if "Note" in data:
            raise ConnectionError(f"Alpha Vantage API limit reached: {data['Note']}")

        # The actual time series data is nested under this key
        time_series = data.get("Time Series (Daily)", {})

        # Get the most recent day's data
        # The keys are dates, so we take the first one available
        latest_day = next(iter(time_series.keys()), None)
        if latest_day:
            daily_data = time_series[latest_day]
            # Clean up the column names and add ticker/date info
            processed_data = {
                "ticker": ticker,
                "date": latest_day,
                "open": float(daily_data["1. open"]),
                "high": float(daily_data["2. high"]),
                "low": float(daily_data["3. low"]),
                "close": float(daily_data["4. close"]),
                "volume": int(daily_data["5. volume"]),
            }
            all_stock_data.append(processed_data)

    print("Successfully fetched all stock data.")
    return pd.DataFrame(all_stock_data)
