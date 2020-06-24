
import os

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.hooks.mysql_hook import MySqlHook

from datetime import datetime, timedelta


class ReturningSingleMySqlOperator(MySqlOperator):
    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = MySqlHook(mysql_conn_id=self.mysql_conn_id, schema=self.database)
        return hook.get_first(self.sql, parameters=self.parameters)


class ReturningMultipleMySqlOperator(MySqlOperator):
    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        hook = MySqlHook(mysql_conn_id=self.mysql_conn_id, schema=self.database)
        return hook.get_records(self.sql, parameters=self.parameters)


class CSVFilesPresentSensor(BaseSensorOperator):
    def __init__(self, *args, local_path="", **kwargs):
        super(CSVFilesPresentSensor, self).__init__(*args, soft_fail=True, **kwargs)
        self.local_path = local_path

    def poke(self, context):
        print("Checking local path " + self.local_path)
        return len(select_files_from_fs(self.local_path)) > 0


def select_files_from_fs(local_path, **kwargs):
    files = [os.path.join(local_path, f) for f in os.listdir(local_path) if f.endswith(".csv")]

    print("Selected files " + str(files))
    return files


def backup_files_on_fs(backup_path, **kwargs):
    selected_files = kwargs['ti'].xcom_pull(task_ids='select_files')
    for selected_file in selected_files:
        filename = os.path.basename(selected_file)
        os.rename(selected_file, os.path.join(backup_path, filename))


def bulk_load_sql(table_name, **kwargs):

    selected_files = kwargs['ti'].xcom_pull(task_ids='select_files')
    conn = MySqlHook(mysql_conn_id='telmetry_mysql')

    import pandas
    for selected_file in selected_files:
        df = pandas.read_csv(selected_file, sep=",", decimal=".", encoding='utf-8')

        df['wheel'] = df['wheel'].str[2:4]
        df['action'] = df['action'].str[2:4]

        connection = conn.get_conn()
        try:
            cursor = connection.cursor()
            sql = "insert into " + table_name + " (" + ",".join([str(f) for f in df]) + ") values (" + ",".join(["%s"] * len(df.columns)) + ")"
            print("SQL statement is " + sql)
            for index, row in df.iterrows():
                values = [row[c] for c in df]
                print("inserting values " + str(values))
                cursor.execute(sql, values)
            connection.commit()
        finally:
            connection.close()

    return table_name


def remove_dull_wheel_data(wheel_name, **kwargs):
    selected_wheel_records = kwargs['ti'].xcom_pull(task_ids='select_new_wheel_' + wheel_name + '_data')
    print(str(selected_wheel_records))
    # and now iterate over records and select those we don't want so we can remove them...


def select_unprocessed_wheel_data(wheel_name):
    return "SELECT * FROM wheel_steer WHERE wheel = '" + wheel_name + "' AND timestamp >= (SELECT IFNULL(MAX(end_timestamp), 0) FROM wheel_steer_interest)"


default_args = {
    'owner': 'daniel',
    'start_date': datetime.combine(datetime.today() - timedelta(1), datetime.min.time()),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('telemtry-csv-to-mysql', default_args=default_args, schedule_interval="@daily") as dag:

    check_files_present = CSVFilesPresentSensor(
        task_id='check_files_present',
        local_path="/home/jovyan/telemetry-logs/"
    )

    select_files = PythonOperator(
        task_id='select_files',
        python_callable=select_files_from_fs,
        provide_context=True,
        op_kwargs={'local_path': "/home/jovyan/telemetry-logs/"}
    )

    process_files = PythonOperator(
        task_id='process_files',
        python_callable=bulk_load_sql,
        provide_context=True,
        op_kwargs={'table_name': "wheel_steer"}
    )

    backup_files = PythonOperator(
        task_id='backup_files',
        python_callable=backup_files_on_fs,
        provide_context=True,
        op_kwargs={'backup_path': "/home/jovyan/telemetry-logs/backup/"}
    )

    check_files_present >> select_files >> process_files >> backup_files

    for wheel_name in ['fl', 'fr', 'br', 'bl']:
        select_new_wheel_data = ReturningMultipleMySqlOperator(
            task_id='select_new_wheel_' + wheel_name + '_data',
            sql=select_unprocessed_wheel_data(wheel_name),
            mysql_conn_id='telmetry_mysql'
        )
        process_files >> select_new_wheel_data

        remove_wheel_data = PythonOperator(
            task_id='remove_dull_wheel_' + wheel_name + '_data',
            python_callable=remove_dull_wheel_data,
            provide_context=True,
            op_kwargs={'wheel_name': wheel_name}
        )
        select_new_wheel_data >> remove_wheel_data
