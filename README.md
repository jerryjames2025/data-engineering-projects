# Data Engineering Projects

A portfolio of end-to-end data engineering pipelines, automated ELT workflows, data warehouse modeling, and BI dashboards built with modern open-source tools.

---

## Featured Projects

### 1. [Automated Weather Data ELT Pipeline](./weather-data-project)
An end-to-end containerized ELT pipeline that extracts real-time meteorological data from the Weatherstack API, loads raw records into PostgreSQL, runs automated deduplication and analytical transformations with dbt, and serves interactive dashboards in Apache Superset—orchestrated every 5 minutes by Apache Airflow.

* **Orchestration:** Apache Airflow 3 (`PythonOperator` & `DockerOperator`)
* **Storage / Warehouse:** PostgreSQL (Multi-database & multi-schema isolation)
* **Transformation:** dbt (`dbt-postgres` 1.9)
* **BI & Caching:** Apache Superset & Redis
* **Infrastructure:** Docker, Docker Compose, WSL2 (Ubuntu)

---

## Repository Structure

```text
data-engineering-projects/
├── README.md
└── weather-data-project/       # End-to-end Weather API -> Airflow -> Postgres -> dbt -> Superset pipeline
```
