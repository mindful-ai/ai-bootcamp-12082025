"""
nasa_apod_postgres.py
ETL DAG: Fetch NASA APOD API -> Transform -> Load into Postgres
Compatible with Astronomer 1.31 / Airflow 2.10+
"""

from datetime import timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.models import Connection
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
import json


# Default args for retries, etc.
default_args = {
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="nasa_apod_postgres_v3",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    tags=["nasa", "apod", "example"],
) as dag:

    # Step 1: Create the table if it doesn't exist
    @task(task_id="create_table")
    def create_table():
        pg = PostgresHook(postgres_conn_id="my_postgres_connection")
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            hdurl TEXT,
            date DATE UNIQUE,
            media_type VARCHAR(50),
            copyright VARCHAR(255),
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        pg.run([create_table_sql])

    # # Step 2: Extract data from NASA APOD API
    # @task(task_id="extract_apod")
    # def extract_apod():
    #     hook = HttpHook(method="GET", http_conn_id="nasa_api")
    #     response = hook.run(
    #         endpoint="planetary/apod",
    #         params={"api_key": "{{ conn.nasa_api.extra_dejson.api_key }}"},
    #     )
    #     return response.json()
    

    # Can test using curl: curl -k "https://api.nasa.gov/planetary/apod?api_key=api_key"
    @task(task_id="extract_apod")
    def extract_apod():
        # Fetch connection object
        conn = Connection.get_connection_from_secrets("nasa_api")
        api_key = json.loads(conn.extra).get("api_key")

        # Make request
        hook = HttpHook(method="GET", http_conn_id="nasa_api")
        response = hook.run(endpoint="planetary/apod", data={"api_key": api_key})
        return response.json()

    # Step 3: Transform API response into clean dict
    @task(task_id="transform_apod_data")
    def transform_apod_data(api_response):
        if not api_response:
            raise ValueError("Empty response from NASA APOD API")

        return {
            "title": api_response.get("title"),
            "explanation": api_response.get("explanation"),
            "url": api_response.get("url"),
            "hdurl": api_response.get("hdurl"),
            "date": api_response.get("date"),
            "media_type": api_response.get("media_type"),
            "copyright": api_response.get("copyright"),
        }

    # Step 4: Load data into Postgres (UPSERT by date)
    @task(task_id="load_data_to_postgres")
    def load_data_to_postgres(apod):
        pg = PostgresHook(postgres_conn_id="my_postgres_connection")
        upsert_sql = """
        INSERT INTO apod_data (title, explanation, url, hdurl, date, media_type, copyright)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO UPDATE SET
            title = EXCLUDED.title,
            explanation = EXCLUDED.explanation,
            url = EXCLUDED.url,
            hdurl = EXCLUDED.hdurl,
            media_type = EXCLUDED.media_type,
            copyright = EXCLUDED.copyright;
        """
        pg.run(
            upsert_sql,
            parameters=(
                apod["title"],
                apod["explanation"],
                apod["url"],
                apod.get("hdurl"),
                apod["date"],
                apod["media_type"],
                apod.get("copyright"),
            ),
        )

    # --- Task dependencies ---
    table = create_table()
    api_response = extract_apod()
    transformed = transform_apod_data(api_response)
    loaded = load_data_to_postgres(transformed)

    table >> api_response >> transformed >> loaded
