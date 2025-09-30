# src/time_capsule/__init__.py
from dagster import Definitions, load_assets_from_modules
from dagster_duckdb_pandas import DuckDBPandasIOManager
from . import assets

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "io_manager": DuckDBPandasIOManager(
            database="data/time_capsule.duckdb",
            schema="main",
            use_quotes=False,
        )
    },
)