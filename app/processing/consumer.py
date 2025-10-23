import asyncio, json, logging, time
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from clickhouse_connect import Client as CHClient
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from app.config.settings import settings
from app.observability.otel import init_tracing
init_tracing('consumer')
logger = logging.getLogger('consumer')
class ClickHouseSink:
    def __init__(self, host: str = None, database: str = None):
        self.client = CHClient(host or settings.clickhouse_host, database=database or settings.clickhouse_database)
    def bulk_insert(self, table: str, rows: list):
        # expects rows as list of dicts; map to columns
        if not rows:
            return
        # naive implementation: build insert from dicts
        columns = list(rows[0].keys())
        values = [[r[c] for c in columns] for r in rows]
        self.client.insert(table, values, column_names=columns)
class ConsumerService:
    def __init__(self, topic: str = None, group_id: str = 'processor-group'):
        self.topic = topic or settings.kafka_topic
        self.group_id = group_id
        self.consumer = AIOKafkaConsumer(self.topic, bootstrap_servers=settings.kafka_bootstrap, group_id=self.group_id,
                                        enable_auto_commit=False, max_poll_records=1000)
        self.producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap, acks='all', enable_idempotence=True)
        self.ch_sink = ClickHouseSink()
        self.batch_size = 500
        self.batch_timeout = 1.0  # seconds
    async def start(self):
        await self.consumer.start()
        await self.producer.start()
        logger.info('consumer & producer started')
    async def stop(self):
        await self.consumer.stop()
        await self.producer.stop()
        logger.info('consumer & producer stopped')
    async def process_loop(self):
        buffer = []
        last_flush = time.time()
        async for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode())
                row = {'ts': data.get('timestamp'), 'agent': data.get('agent_id'), 'metric': data.get('metric'),
                       'value': float(data.get('value',0)), 'tags': json.dumps(data.get('tags', {}))}
                buffer.append((msg, row))
            except Exception as e:
                logger.exception('Deserialization error, sending to DLQ: %s', e)
                await self._send_dlq(msg)
            # flush conditions
            if len(buffer) >= self.batch_size or (time.time() - last_flush) >= self.batch_timeout:
                await self._flush_buffer(buffer)
                last_flush = time.time()
    async def _flush_buffer(self, buffer):
        if not buffer:
            return
        msgs, rows = zip(*buffer)
        rows_list = list(rows)
        try:
            # bulk insert to ClickHouse
            self.ch_sink.bulk_insert('events', rows_list)
            # commit offsets for messages we processed - commit up to last message offset
            last_msg = msgs[-1]
            await self.consumer.commit({last_msg.topic_partition: last_msg.offset + 1})
            logger.info('Inserted %d rows and committed offset', len(rows_list))
        except Exception as e:
            logger.exception('Sink error, sending all to DLQ: %s', e)
            for m, _ in buffer:
                await self._send_dlq(m)
        finally:
            buffer.clear()
    @retry(wait=wait_exponential(multiplier=0.5, min=0.5, max=10), stop=stop_after_attempt(5),
           retry=retry_if_exception_type(Exception))
    async def _send_dlq(self, msg):
        try:
            await self.producer.send_and_wait(settings.kafka_dlq_topic, value=msg.value, key=msg.key)
            logger.info('Sent message to DLQ')
        except Exception as e:
            logger.exception('Failed to send to DLQ: %s', e)
