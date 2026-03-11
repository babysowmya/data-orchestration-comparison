from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract():
    print("Extract step successful")

def transform():
    print("Transform step successful")

def load():
    print("Load step successful")

with DAG(
    dag_id="simple_success_pipeline",
    start_date=datetime(2024,1,1),
    schedule=None,
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=extract
    )

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=transform
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load
    )

    extract_task >> transform_task >> load_task