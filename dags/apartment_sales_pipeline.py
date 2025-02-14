from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import sys

sys.path.append(r"D:\Phyton_programs\apartment_sales_data\scripts")
from data_pipeline import fetch_new_ads, update_database


load_dotenv(override=True, encoding='utf-8')

# Задаём параметры DAG'а
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': [os.getenv('EMAIL')],  # Укажите ваш email
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Инициализация DAG'а
with DAG(
    dag_id='apartment_sales_pipeline',
    default_args=default_args,
    description='Pipeline for updating apartment sales data',
    schedule_interval='@daily',  # Запускать ежедневно
    start_date=datetime(2025, 1, 1),  # Укажите стартовую дату
    catchup=False,
) as dag:
    start_operator = BashOperator(task_id='Begin_execution', bash_command='echo Hello')
    # Шаг 1: Сбор новых данных
    collect_new_ads_task = PythonOperator(
        task_id='fetch_new_ads',
        python_callable=fetch_new_ads,  # Импортируемая функция из data_pipeline.py
    )

    # Шаг 2: Обновление базы данных
    update_db_task = PythonOperator(
        task_id='update_database',
        python_callable=update_database,  # Импортируемая функция из data_pipeline.py
    )

    # Указываем порядок выполнения задач
    collect_new_ads_task >> update_db_task
