# src/time_capsule/assets.py
from dagster import asset
from typing import Dict, Any

@asset
def my_first_asset() -> Dict[str, Any]:
    """A simple asset that returns a dictionary."""
    return {"hello": "dagster"}