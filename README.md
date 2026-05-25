# Data Orchestration Comparison Project

## Overview

This project implements the **same ETL pipeline** in three different orchestration frameworks to compare their developer experience, setup complexity, observability, and retry handling.

### ETL Pipeline Logic
1. **Extract** — Read `user_events.csv`
2. **Transform** — Filter out blocked countries, compute session duration and event counts per user per day
3. **Load** — Save result as a `.parquet` file

---

## Project Structure
data-orchestration-comparison/
├── airflow/
│   └── dags/
│       └── airflow_pipeline.py     # Airflow DAG
├── prefect/
│   └── prefect_pipeline.py         # Prefect flow
├── dagster/
│   ├── dagster_pipeline.py         # Dagster assets
│   └── workspace.yaml
├── shared/
│   └── etl_logic.py                # Shared ETL functions
├── data/
│   └── user_events.csv             # Input data
├── docker-compose.yaml             # Airflow Docker setup
├── requirements.txt
├── COMPARISON.md
└── README.md

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Docker Desktop (for Airflow only)
- Git

### Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running Each Pipeline

### Prefect
```bash
cd prefect
python prefect_pipeline.py
```
Output saved to: `data/output_prefect.parquet`

### Dagster
```bash
cd dagster
dagster dev -f dagster_pipeline.py
```
Open UI at: `http://localhost:3000`
Materialize all assets from the UI.
Output saved to: `data/output_dagster.parquet`

### Apache Airflow
```bash
docker compose up -d
```
Open UI at: `http://localhost:8080`  
Login: `airflow` / `airflow`  
Enable and trigger DAG: `etl_pipeline_airflow`

---

## Key Comparisons

| Feature | Airflow | Prefect | Dagster |
|---|---|---|---|
| Setup | Docker required | pip install | pip install |
| Workflow model | DAG | Flow/Task | Assets |
| Retries | `retries=` in Operator | `@task(retries=)` | `RetryPolicy` |
| UI | Yes (port 8080) | Yes (port 4200) | Yes (port 3000) |
| Learning curve | High | Low | Medium |
| Best for | Enterprise scheduling | Fast prototyping | Data asset tracking |

See [COMPARISON.md](COMPARISON.md) for detailed analysis.

---

## Author
Sowmya Sunkara