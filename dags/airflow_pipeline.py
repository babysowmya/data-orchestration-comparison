import pandas as pd
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "user_events.csv")

sys.path.append("/opt/airflow")

from etl_logic import extract_data, transform_data, load_data


def extract():
    df = extract_data(DATA_PATH)
    return df.to_json()


def transform(**context):
    df_json = context["ti"].xcom_pull(task_ids="extract_task")
    df = pd.read_json(df_json)
    df = transform_data(df, ["USA"])
    return df.to_json()


def load(**context):
    df_json = context["ti"].xcom_pull(task_ids="transform_task")
    df = pd.read_json(df_json)
    load_data(df, "/opt/airflow/data/output_airflow.parquet")


with DAG(
    dag_id="etl_pipeline_airflow",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load,
    )

    extract_task >> transform_task >> load_task