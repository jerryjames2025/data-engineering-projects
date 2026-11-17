# Automated Weather Data ELT Pipeline

An end-to-end containerized **Extract, Load, Transform (ELT)** data pipeline that ingests meteorological data from the **Weatherstack API** (with mock fallback support for offline/quota-safe testing), loads raw JSON fields into **PostgreSQL**, cleans and aggregates records using **dbt**, and serves interactive visualizations in **Apache Superset**—orchestrated every 5 minutes by **Apache Airflow 3**.

---

## Architecture & Pipeline Flow

```text
┌───────────────────────────────────────────┐
│   Weatherstack API / mock_fetch_data()    │
└─────────────────────┬─────────────────────┘
                      │  1. Extract & Load (Airflow PythonOperator)
                      ▼
┌───────────────────────────────────────────┐
│        PostgreSQL (Database: db)          │
│        Table: dev.raw_weather_data        │
└─────────────────────┬─────────────────────┘
                      │  2. Transform (Airflow DockerOperator -> dbt run)
                      ▼
┌───────────────────────────────────────────┐
│             dbt Core Models               │
│  ├── public.stg_weather_data (Deduplicated)│
│  ├── public.daily_average    (Aggregated) │
│  └── public.weather_report   (Reporting)  │
└─────────────────────┬─────────────────────┘
                      │  3. Visualize
                      ▼
┌─────────────────────┐      ┌──────────────┐
│   Apache Superset   │◀────▶│    Redis     │
└─────────────────────┘      └──────────────┘
```

---

## Tech Stack

* **Orchestration:** Apache Airflow 3.4 (`PythonOperator` & `DockerOperator`)
* **Ingestion:** Python 3, `requests`, `psycopg2`
* **Data Warehouse & Metadata DB:** PostgreSQL (`db`, `airflow_db`, `superset_db`, `examples_db`)
* **Transformations:** dbt (`dbt-postgres:1.9.latest`)
* **BI & Caching:** Apache Superset 3.0 & Redis 7
* **Infrastructure:** Docker & Docker Compose on WSL2 (Ubuntu)

---

## Repository Structure

```text
weather-data-project/
├── airflow/
│   └── dags/
│       └── dbt_orchestrator.py           # DAG chaining ingest_data_task -> transform_data_task
├── api-request/
│   ├── api_request.py                    # Weatherstack API client & mock_fetch_data() payload generator
│   └── insert_records.py                 # Creates dev.raw_weather_data & inserts weather records
├── dbt/
│   ├── profiles.yml                      # dbt PostgreSQL connection profile (target: dev, schema: public)
│   └── my_project/
│       ├── dbt_project.yml               # dbt project configuration
│       ├── analyses/
│       ├── macros/
│       ├── seeds/
│       ├── snapshots/
│       ├── tests/
│       └── models/
│           ├── sources/
│           │   └── sources.yml           # Declares dev.raw_weather_data source
│           ├── staging/
│           │   └── stg_weather_data.sql  # Deduplication & UTC-to-local timestamp conversion
│           └── mart/
│               ├── daily_average.sql     # Daily average temperature & wind speed per city
│               └── weather_report.sql    # Clean reporting table for BI dashboards
├── docker/
│   ├── docker-bootstrap.sh               # Superset web application startup script
│   ├── docker-init.sh                    # Superset DB initialization & admin setup script
│   └── superset_config.py                # Superset SQLAlchemy & Redis cache settings
├── postgres/
│   ├── airflow_init.sql                  # Creates airflow role & airflow_db
│   └── superset_init.sql                 # Creates superset & examples roles and databases
└── docker-compose.yaml                   # Multi-container orchestration config
```

---

## Data Warehouse & dbt Models

### 1. Raw Layer (`dev.raw_weather_data`)
Created automatically by `api-request/insert_records.py` if it does not exist:

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | `SERIAL PRIMARY KEY` | Auto-incrementing record identifier |
| `city` | `TEXT` | Observation location name (e.g., `New York`) |
| `temperature` | `FLOAT` | Current temperature in Celsius |
| `weather_description` | `TEXT` | Condition summary (e.g., `Patchy rain nearby`, `Clear`) |
| `wind_speed` | `FLOAT` | Wind speed (km/h) |
| `time` | `TIMESTAMP` | Local observation timestamp from API (`location.localtime`) |
| `insert_at` | `TIMESTAMP` | UTC ingestion timestamp (`DEFAULT now()`) |
| `utc_offset` | `TEXT` | Timezone offset in hours (e.g., `-5.0`, `-6.0`) |

### 2. Staging Layer (`public.stg_weather_data`)
* **Deduplication:** Uses `ROW_NUMBER() OVER (PARTITION BY time ORDER BY insert_at)` and filters `WHERE rn = 1` so repeated 5-minute DAG runs never produce duplicate observations.
* **Timezone Normalization:** Converts UTC `insert_at` into local time via `(insert_at + (utc_offset || 'hours')::interval) AS insert_at_local` and aliases `time` as `weather_time_local`.

### 3. Analytical Marts
* **`public.daily_average`:** Aggregates `stg_weather_data` by `city` and `DATE(weather_time_local)` to calculate `avg_temperature` and `avg_wind_speed` rounded to 2 decimal places.
* **`public.weather_report`:** Exposes clean, deduplicated observation columns (`city`, `temperature`, `weather_description`, `wind_speed`, `weather_time_local`) for Superset visualizations.

---

## Setup & Execution Guide

### Prerequisites
* **Docker** & **Docker Compose** (v2+)
* **WSL2 (Ubuntu)** if running on Windows (recommended minimum 8 GB RAM in `.wslconfig`)

### 1. Clone the Repository
```bash
git clone https://github.com
cd data-engineering-projects/weather-data-project
```

### 2. Configure Permissions & Environment
1. *(Optional)* To pull live data instead of `mock_fetch_data()`, uncomment `fetch_data()` in `api-request/api_request.py`, insert your Weatherstack API key, and update `insert_records.py` to call `fetch_data()`.
2. Set executable permissions for Superset init scripts and read permissions for Airflow volumes:
   ```bash
   chmod +x docker/*.sh
   chmod -R a+rX airflow/dags api-request
   ```

### 3. Start the Container Stack
Launch PostgreSQL, Redis, Airflow, dbt, and Apache Superset:
```bash
docker compose --env-file docker/.env up -d
```

Grant Docker socket access so Airflow's `DockerOperator` can launch ephemeral dbt containers:
```bash
sudo chmod 666 /var/run/docker.sock
```

### 4. Run the Pipeline in Apache Airflow
1. Retrieve the auto-generated Airflow `admin` password:
   ```bash
   docker exec -it airflow_container cat /opt/airflow/simple_auth_manager_passwords.json.generated
   ```
2. Open **`http://localhost:8000`**, sign in as **`admin`**, unpause **`weather-api-dbt-orchestrator`**, and click **Trigger**.
3. Airflow executes `ingest_data_task` followed by `transform_data_task` (`dbt run` on `superset_my_network`).

### 5. Visualize in Apache Superset
1. Open **`http://localhost:8088`** and log in (`admin` / `admin`).
2. Go to **Settings** → **Database Connections** → **+ Database** → **PostgreSQL** and connect with:
   * **Host:** `db` | **Port:** `5432` | **Database:** `db` | **User:** `db_user` | **Password:** `db_password`
3. Under **Datasets** → **+ Dataset**, select schema **`public`** and import **`weather_report`** and **`daily_average`** to build charts and dashboards.
