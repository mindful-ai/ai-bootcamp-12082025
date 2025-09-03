from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def greet(name: str):
    print(f"Hello, {name}! 👋")

with DAG(
    dag_id="hello_ops",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["workshop", "operators"]
) as dag:
    print_date = BashOperator(
        task_id="print_date",
        bash_command="date"
    )

    say_hello = PythonOperator(
        task_id="say_hello",
        python_callable=greet,
        op_kwargs={"name": "Airflow"},
    )

    print_date >> say_hello