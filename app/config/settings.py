from pydantic import BaseSettings, Field
class Settings(BaseSettings):
    kafka_bootstrap: str = Field('kafka:9092', env='KAFKA_BOOTSTRAP')
    kafka_topic: str = Field('events', env='KAFKA_TOPIC')
    kafka_dlq_topic: str = Field('events-dlq', env='KAFKA_DLQ_TOPIC')
    kafka_partitions: int = Field(16, env='KAFKA_PARTITIONS')
    redis_url: str = Field('redis://redis:6379/0', env='REDIS_URL')
    clickhouse_host: str = Field('clickhouse', env='CLICKHOUSE_HOST')
    clickhouse_database: str = Field('default', env='CLICKHOUSE_DB')
    metrics_port: int = Field(9101, env='METRICS_PORT')
    max_batch_size: int = Field(2000, env='MAX_BATCH_SIZE')
    max_concurrent_requests: int = Field(512, env='MAX_CONCURRENT_REQUESTS')
    jwt_public_key: str = Field(None, env='JWT_PUBLIC_KEY')
    jwt_alg: str = Field('RS256', env='JWT_ALG')
    class Config:
        env_file = '.env'
settings = Settings()
