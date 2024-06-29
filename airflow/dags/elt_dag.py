from datetime import datetime, timedelta
from airflow import DAG
from docker.types import Mount
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2024, 6, 29),
    catchup=False
)

def run_elt_script():
    script_path = "/opt/airflow/elt/elt_script.py"
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)

task1 = PythonOperator(
    task_id="run_elt_script",
    python_callable=run_elt_script,
    dag=dag
)

task2 = DockerOperator(
    task_id="run_dbt",
    image="ghcr.io/dbt-labs/dbt-postgres:1.8.2",
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/dbt"
    ],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
        Mount(source='/Users/Mery Yulinda/Downloads/Mery Data Science/custom-elt-project',
              target='/dbt', type='bind'),
        Mount(source='/Users/Mery Yulinda/.dbt',
              target='/root', type='bind')
    ],
    dag=dag
)

task1 >> task2