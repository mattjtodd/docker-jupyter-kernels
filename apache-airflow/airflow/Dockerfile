FROM jupyter/minimal-notebook

ENV AIRFLOW_GPL_UNIDECODE=yes

RUN pip install apache-airflow

# Don;t load the examples!
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Init the DB, this saves steps failing later
RUN airflow initdb

USER root

RUN apt-get update
RUN apt-get install python-dev
RUN apt-get install -y libmysqlclient-dev

USER $NB_UID

RUN pip install mysqlclient
