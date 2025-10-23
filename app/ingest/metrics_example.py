from prometheus_client import Counter, Histogram, start_http_server
REQUESTS = Counter('ingest_requests_total', 'Total ingestion requests')
LATENCY = Histogram('ingest_latency_seconds', 'Latency seconds')
def start(port=9101):
    start_http_server(port)
