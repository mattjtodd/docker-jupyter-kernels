FROM jupyter/minimal-notebook

ENV AIRFLOW_GPL_UNIDECODE=yes

RUN pip install apache-airflow

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

RUN airflow initdb

