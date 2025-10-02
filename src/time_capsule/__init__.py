# src/time_capsule/__init__.py
import os
from dagster import Definitions, load_assets_from_modules
from dagster_duckdb_pandas import DuckDBPandasIOManager
from . import cultural_assets, financial_assets, news_assets, weather_assets
from .resources import APIResource


all_assets = load_assets_from_modules([cultural_assets, financial_assets, news_assets, weather_assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "io_manager": DuckDBPandasIOManager(
            database="data/time_capsule.duckdb",
            schema="main",
            use_quotes=False,
        ),
        # Configure the resource using environment variables.
        # This will read from your .env file locally.
        "api": APIResource(
            openweathermap_api_key=os.getenv("OPENWEATHERMAP_API_KEY"),
            alphavantage_api_key=os.getenv("ALPHAVANTAGE_API_KEY"),
        ),
    },
)