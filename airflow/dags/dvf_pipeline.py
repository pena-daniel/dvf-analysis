"""Pipeline DVF : source -> MinIO (Parquet) -> bronze -> dbt (silver, gold).

Déclenchement manuel, avec l'année en paramètre.
"""

from pathlib import Path

from airflow import DAG
from airflow.models.param import Param
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

from extraction.extract import extract
from extraction.load_to_pg import load_to_pg
from utils.data_columns import DVF_EXPECTED_COLUMNS

PROJECT_DIR = Path("/opt/airflow/project")
RAW_DIR = PROJECT_DIR / "extraction" / "raw"
DBT_DIR = PROJECT_DIR / "dbt"
DBT_BIN = "/home/airflow/dbt-venv/bin/dbt"


def run_extract(year: str) -> None:
    """Lit le fichier annuel et dépose les Parquet dans MinIO."""
    extract(RAW_DIR, int(year), DVF_EXPECTED_COLUMNS)


def run_load(year: str) -> None:
    """Charge les Parquet de l'année dans bronze.dvf."""
    load_to_pg(int(year))


with DAG(
    dag_id="dvf_pipeline",
    description="Ingestion DVF et transformations dbt pour une année",
    schedule=None,
    catchup=False,
    max_active_runs=1,
    tags=["dvf", "ingestion", "dbt"],
    params={
        "year": Param(2025, type="integer", title="Année DVF à traiter"),
    },
    default_args={
        "retries": 1,
    },
) as dag:

    extract_task = PythonOperator(
        task_id="extract_to_minio",
        python_callable=run_extract,
        op_kwargs={"year": "{{ params.year }}"},
    )

    load_task = PythonOperator(
        task_id="load_to_bronze",
        python_callable=run_load,
        op_kwargs={"year": "{{ params.year }}"},
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"cd {DBT_DIR} && "
            f"{DBT_BIN} build --target docker --profiles-dir ."
        ),
    )

    extract_task >> load_task >> dbt_build