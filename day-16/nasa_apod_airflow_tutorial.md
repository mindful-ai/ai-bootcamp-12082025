# NASA APOD Airflow Tutorial with Astro CLI

This tutorial demonstrates how to build an **Apache Airflow DAG** that fetches data from the **NASA Astronomy Picture of the Day (APOD) API** and stores it into a PostgreSQL database using **Astro CLI**.

---

## 1. Prerequisites

- **Docker Desktop** installed and running.
- **Astro CLI** installed ([Installation Guide](https://docs.astronomer.io/astro/cli/install-cli)).
- A **NASA API Key** (Get one for free at [NASA API](https://api.nasa.gov/)).

---

## 2. Initialize an Astro Project

```bash
astro dev init
```

This will create a new project with the following structure:

```
.
├── dags/
├── Dockerfile
├── include/
├── packages.txt
├── requirements.txt
└── plugins/
```

---

## 3. Add Dependencies

Edit `requirements.txt` to include:

```
apache-airflow-providers-http
apache-airflow-providers-postgres
psycopg2-binary
```

---

## 4. Start Airflow

```bash
astro dev start
```

This will spin up Airflow with Postgres and other services.

---

## 5. Configure Connections in Airflow

1. Open Airflow UI: [http://localhost:8080](http://localhost:8080)
2. Go to **Admin → Connections**.
3. Create an **HTTP connection** for NASA API:
   - Conn Id: `nasa_api`
   - Conn Type: `HTTP`
   - Host: `https://api.nasa.gov`
   - Extra: `{"api_key":"YOUR_NASA_API_KEY"}`
4. Create a **Postgres connection**:
   - Conn Id: `postgres_default`
   - Conn Type: `Postgres`
   - Host: `postgres`
   - Schema: `airflow`
   - Login: `airflow`
   - Password: `airflow`
   - Port: `5432`

---

## 6. DAG Code: `dags/nasa-apod.py`

```python
from airflow import DAG
from airflow.decorators import task
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import logging

# DAG definition
default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="nasa_apod_v3",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # Step 1: Create Table in Postgres
    @task(task_id="create_table")
    def create_table():
        pg_hook = PostgresHook(postgres_conn_id="postgres_default")
        create_query = """
        CREATE TABLE IF NOT EXISTS nasa_apod (
            date TEXT PRIMARY KEY,
            title TEXT,
            explanation TEXT,
            url TEXT
        );
        """
        pg_hook.run(create_query)
        logging.info("Table nasa_apod ensured.")

    # Step 2: Extract data from NASA APOD API
    @task(task_id="extract_apod")
    def extract_apod():
        hook = HttpHook(method="GET", http_conn_id="nasa_api")
        api_key = hook.get_connection("nasa_api").extra_dejson.get("api_key")
        response = hook.run(
            endpoint="planetary/apod",
            data={"api_key": api_key},  # ✅ Use 'data' instead of 'params'
        )
        return response.json()

    # Step 3: Load data into Postgres
    @task(task_id="load_apod")
    def load_apod(apod_data: dict):
        pg_hook = PostgresHook(postgres_conn_id="postgres_default")
        insert_query = """
        INSERT INTO nasa_apod (date, title, explanation, url)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (date) DO NOTHING;
        """
        pg_hook.run(
            insert_query,
            parameters=(
                apod_data["date"],
                apod_data["title"],
                apod_data["explanation"],
                apod_data["url"],
            ),
        )
        logging.info("APOD data inserted successfully.")

    # DAG Workflow
    table = create_table()
    apod = extract_apod()
    load_apod(apod) >> table
```

---

## 7. Run the DAG

1. Go to **Airflow UI → DAGs**.
2. Trigger the DAG `nasa_apod_v3`.
3. Check logs for tasks:
   - `create_table`
   - `extract_apod`
   - `load_apod`

---

## 8. Validate Data in Postgres

Exec into the Postgres container:

```bash
docker exec -it astro-postgres psql -U airflow -d airflow
```

Run query:

```sql
SELECT * FROM nasa_apod LIMIT 5;
```

You should see NASA APOD records.

---

## ✅ Troubleshooting

- **Error with `params`** → Use `data` instead when calling `hook.run`.
- **Stuck tasks** → Check connection setup in Airflow UI.
- **Windows SSL error with curl** → Use WSL/Linux or add `-k` flag to bypass certificate validation.

---

## 🎯 Outcome

You now have an **Airflow pipeline** that:
1. Ensures a table in Postgres.
2. Fetches data from **NASA APOD API**.
3. Inserts it into Postgres.
4. Runs daily using Airflow scheduler.

---
