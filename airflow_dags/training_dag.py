from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
from src.pipeline import main as run_pipeline

default_args = {
    'owner': 'aeolus-ai',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False
}

logger = logging.getLogger("AeolusAI-DAG")

with DAG(
    dag_id='weather_training_pipeline',
    default_args=default_args,
    description='Training pipeline for Aeolus Weather Predictor',
    schedule_interval='@daily',  # or use '@once' for testing
    start_date=datetime(2025, 4, 1),
    catchup=False,
    tags=["aeolus", "ml", "training"]
) as dag:

    def execute_pipeline():
        logger.info("🚀 Starting Aeolus pipeline...")
        run_pipeline()
        logger.info("✅ Aeolus pipeline complete.")

    train_task = PythonOperator(
        task_id='run_training_pipeline',
        python_callable=execute_pipeline
    )

    train_task
