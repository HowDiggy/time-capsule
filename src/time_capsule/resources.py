# src/time_capsule/resources.py
from dagster import ConfigurableResource

class APIResource(ConfigurableResource):
    openweathermap_api_key: str
    alphavantage_api_key: str