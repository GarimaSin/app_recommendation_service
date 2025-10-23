from airflow import DAG
import importlib, os
def test_dag_import():
    module = importlib.import_module('airflow.dags.retraining_dag')
    assert hasattr(module, 'dag')
