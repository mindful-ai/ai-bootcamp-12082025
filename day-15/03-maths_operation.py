"""
We'll define a DAG where the tasks are as follows:

Task 1: Start with an initial number (e.g., 10).
Task 2: Add 5 to the number.
Task 3: Multiply the result by 2.
Task 4: Subtract 3 from the result.
Task 5: Compute the square of the result.    

"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime





## Dependencies
start_task >> add_five_task >> multiply_by_two_task >> subtract_three_task >> square_number_task

