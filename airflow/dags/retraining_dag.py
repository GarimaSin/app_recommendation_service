from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
default_args = {
    'owner': 'realtime',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
with DAG('retraining_pipeline', start_date=datetime(2025,1,1), schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    extract = BashOperator(
        task_id='extract_clickhouse',
        bash_command='python /opt/app/etl/extract_clickhouse.py --start {{ ds }} --end {{ next_ds }} --out /opt/app/data/training.parquet'
    )
    create_hist = BashOperator(
        task_id='create_historical_dataset',
        bash_command='python /opt/app/feast/create_historical_dataset.py --in /opt/app/data/training.parquet --out /opt/app/data/training_with_features.parquet'
    )
    train = BashOperator(
        task_id='train_model',
        bash_command='python /opt/app/model/train_from_parquet.py --parquet /opt/app/data/training_with_features.parquet'
    )
    extract >> create_hist >> train
