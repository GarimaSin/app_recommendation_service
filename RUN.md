# Quick run notes (local / dev)
1. Start dependencies (Kafka, Zookeeper, Redis, ClickHouse) via docker-compose or k8s.
2. Start the FastAPI gateway (uvicorn app.ingest.ingest_gateway:app --host 0.0.0.0 --port 8000).
3. Start the consumer: python app/processing/run_consumer.py
4. Build and run the PyFlink job using a Flink cluster; the script processing/flink/feature_aggregator.py is a job template.
5. Configure Feast (feast/feature_store.yaml) and apply feature definitions.
6. Use Grafana to import infra/grafana/realtime_dashboard.json.
