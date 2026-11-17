FROM apache/airflow:3.3.1-python3.12

USER airflow

# Dépendances des scripts d'ingestion, dans l'environnement d'Airflow
RUN pip install --no-cache-dir boto3 pandas pyarrow psycopg python-dotenv

# dbt isolé dans son propre venv pour éviter les conflits de dépendances
RUN python -m venv /home/airflow/dbt-venv && \
    /home/airflow/dbt-venv/bin/pip install --no-cache-dir dbt-postgres