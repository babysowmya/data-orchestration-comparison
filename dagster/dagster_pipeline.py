import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dagster import asset, Definitions, RetryPolicy
from shared.etl_logic import extract_data, transform_data, load_data


@asset
def raw_data():
    """Extract: Read user_events.csv into a DataFrame."""
    return extract_data("data/user_events.csv")


@asset(retry_policy=RetryPolicy(max_retries=2, delay=10))
def transformed_data(raw_data):
    """Transform: Filter blocked countries, compute session duration."""
    return transform_data(raw_data, ["USA"])


@asset
def loaded_data(transformed_data):
    """Load: Save final DataFrame as Parquet."""
    load_data(transformed_data, "data/output_dagster.parquet")
    return "data/output_dagster.parquet"


defs = Definitions(
    assets=[raw_data, transformed_data, loaded_data]
)