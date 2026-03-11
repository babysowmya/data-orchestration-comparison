# Data Orchestration Comparison Project

## Project Overview

This project demonstrates a simple ETL pipeline implemented using different data orchestration tools. The goal is to understand how orchestration frameworks manage data workflows.

The ETL pipeline performs three main steps:

1. **Extract** data from a CSV file (`user_events.csv`)
2. **Transform** the data by filtering user events from specific countries
3. **Load** the processed data into a Parquet file

The project primarily focuses on implementing the pipeline using **Apache Airflow**.

---

## Project Structure

```
data-orchestration-comparison
│
├── dags
│   ├── airflow_pipeline.py
│   ├── etl_logic.py
│   └── user_events.csv
│
├── docker-compose.yaml
├── comparison.md
└── README.md
```

---

## Technologies Used

* Python
* Apache Airflow
* Docker
* Pandas
* Parquet

---

## Running the Project

### 1. Start Docker containers

```
docker compose up -d
```

### 2. Open Airflow UI

Open in browser:

```
http://localhost:8080
```

Login credentials:

```
Username: airflow
Password: airflow
```

### 3. Trigger the DAG

1. Enable the DAG **etl_pipeline_airflow**
2. Click **Trigger DAG**
3. Monitor the pipeline execution in the Graph View

---

## ETL Pipeline Tasks

### Extract Task

Reads data from `user_events.csv`.

### Transform Task

Filters the dataset based on specific country values.

### Load Task

Stores the processed data as a Parquet file.

---

## Output

After successful execution, the processed file is saved as:

```
output_airflow.parquet
```

---

## Learning Outcomes

* Understanding ETL pipeline design
* Using Apache Airflow for workflow orchestration
* Running Airflow using Docker containers
* Monitoring DAG execution using the Airflow UI

---

## Author

Sowmya Sunkara