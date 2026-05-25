import sys
import os

# add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from prefect import flow, task
from shared.etl_logic import extract_data, transform_data, load_data


@task
def extract(path):
    return extract_data(path)


@task(retries=2, retry_delay_seconds=10)
def transform(df):
    return transform_data(df, ["USA"])


@task
def load(df, path):
    load_data(df, path)


@flow
def etl_flow(input_path, output_path):

    df = extract(input_path)

    df2 = transform(df)

    load(df2, output_path)


if __name__ == "__main__":
    etl_flow(
        input_path="data/user_events.csv",
        output_path="data/output_prefect.parquet"
    )