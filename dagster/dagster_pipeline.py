import sys
import os
from dagster import op, job

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shared.etl_logic import extract_data, transform_data, load_data


@op
def extract():
    return extract_data("data/user_events.csv")


@op
def transform(df):
    return transform_data(df, ["USA"])


@op
def load(df):
    load_data(df, "data/output_dagster.parquet")


@job
def etl_job():
    load(transform(extract()))