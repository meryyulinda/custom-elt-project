FROM apache/airflow:2.9.2

USER airflow

RUN pip install apache-airflow-providers-docker

USER root
