import sys
import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from shared.etl_logic import extract_data, transform_data, load_data

# ---------- FUNCTIONS ----------

def extract_func(input_path, output_path):
    df = extract_data(input_path)
    df.to_parquet(output_path)
    return output_path   # pass path instead of dataframe


def transform_func(**context):
    ti = context["ti"]
    input_path = ti.xcom_pull(task_ids="extract_task")

    import pandas as pd
    df = pd.read_parquet(input_path)

    transformed_df = transform_data(df, ["USA"])

    output_path = "/tmp/transformed.parquet"
    transformed_df.to_parquet(output_path)

    return output_path


def load_func(**context):
    ti = context["ti"]
    input_path = ti.xcom_pull(task_ids="transform_task")

    import pandas as pd
    df = pd.read_parquet(input_path)

    load_data(df, "data/output.parquet")


# ---------- DAG ----------

with DAG(
    dag_id="etl_pipeline_airflow",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract_func,
        op_kwargs={
            "input_path": "data/user_events.csv",
            "output_path": "/tmp/extracted.parquet",
        }
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform_func,
        retries=2,
        retry_delay=timedelta(seconds=10),
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load_func,
    )

    extract_task >> transform_task >> load_task