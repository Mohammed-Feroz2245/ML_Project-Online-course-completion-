from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

# Tell Airflow where your 'src' folder is
sys.path.append("/opt/project")

# WHAT TO DO:
def run_my_ml_code():
    from src.training.script import train_and_upload
    return train_and_upload()

# WHEN TO DO IT:
with DAG(
    dag_id="ml_training_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    # THE TASK:
    task_1 = PythonOperator(
        task_id="train_model_task",
        python_callable=run_my_ml_code
    )