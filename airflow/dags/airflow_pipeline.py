import sys
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# allow access to shared folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from shared.etl_logic import extract_data, transform_data, load_data


def extract():
    return extract_data("data/user_events.csv")


def transform(**context):
    df = context["ti"].xcom_pull(task_ids="extract_task")
    return transform_data(df, ["USA"])


def load(**context):
    df = context["ti"].xcom_pull(task_ids="transform_task")
    load_data(df, "data/output_airflow.parquet")


with DAG(
    dag_id="etl_pipeline_airflow",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
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