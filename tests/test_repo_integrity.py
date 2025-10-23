import os
def test_files_exist():
    required = ['app/ingest/ingest_gateway.py','app/processing/consumer.py','model/train_from_parquet.py','etl/extract_clickhouse.py','feast/create_historical_dataset.py']
    for f in required:
        assert os.path.exists(f)
