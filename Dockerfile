FROM apache/airflow:2.10.4-python3.12

USER airflow

# Устанавливаем зависимости из requirements.txt
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

