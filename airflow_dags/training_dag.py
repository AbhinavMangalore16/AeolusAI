from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def train_model():
    os.system("python /app/pipelines/train_model.py")

with DAG(
    dag_id="weather_model_training",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    train = PythonOperator(
        task_id="train_weather_model",
        python_callable=train_model,
    )
