"""
We'll define a DAG where the tasks are as follows:

Task 1: Start with an initial number (e.g., 10).
Task 2: Add 5 to the number.
Task 3: Multiply the result by 2.
Task 4: Subtract 3 from the result.
Task 5: Compute the square of the result.    

"""

from datetime import datetime
from airflow.decorators import dag, task


@dag(
    dag_id="math_sequence_dag",
    start_date=datetime(2023, 1, 1),
    schedule="@once",
    catchup=False,
    tags=["workshop", "taskflow"],
)
def math_sequence_dag():
    @task
    def start_number() -> int:
        value = 10
        print(f"Starting number {value}")
        return value

    @task
    def add_five(current_value: int) -> int:
        new_value = current_value + 5
        print(f"Add 5: {current_value} + 5 = {new_value}")
        return new_value

    @task
    def multiply_by_two(current_value: int) -> int:
        new_value = current_value * 2
        print(f"Multiply by 2: {current_value} * 2 = {new_value}")
        return new_value

    @task
    def subtract_three(current_value: int) -> int:
        new_value = current_value - 3
        print(f"Subtract 3: {current_value} - 3 = {new_value}")
        return new_value

    @task
    def square_number(current_value: int) -> int:
        new_value = current_value**2
        print(f"Square the result: {current_value}^2 = {new_value}")
        return new_value

    # Task dependencies using TaskFlow XCom passing
    value = start_number()
    value = add_five(value)
    value = multiply_by_two(value)
    value = subtract_three(value)
    square_number(value)


dag = math_sequence_dag()
