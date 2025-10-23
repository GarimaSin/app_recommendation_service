# Production Real-Time Recommendation Platform - Full Pipeline
This repository adds a full end-to-end production-ready pipeline including:
1. AIOKafka producer/consumer with partitioning and DLQ handling.
2. PyFlink feature aggregation job example.
3. Feast feature repo skeleton with Redis online store.
4. ClickHouse insertion pipeline in the consumer (batching + commit + DLQ).
5. Grafana dashboards for ClickHouse and Prometheus metrics.

This is a scaffold meant for production deployment. Replace connection endpoints, secrets, and tune resources before deploying.


This package includes Dockerfiles and Helm templates for producer, consumer, Flink job, and Feast.
Use `helm install` to deploy the helm chart and configure image repository and secrets in values.yaml.


## Offline training pipeline
1. Run ETL: python etl/extract_clickhouse.py --start '2025-01-01' --end '2025-01-31' --out data/training.parquet
2. Create historical dataset with Feast: python feast/create_historical_dataset.py --in data/training.parquet --out data/training_with_features.parquet
3. Train model from parquet: python model/train_from_parquet.py --parquet data/training_with_features.parquet
4. Orchestrate with Airflow: deploy Dockerfile.airflow image and place DAG in airflow/dags


## Tests

Run `pytest` to execute full test suite. Note: some tests mock external services.
