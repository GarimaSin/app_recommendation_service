import asyncio, logging, json, hashlib
from typing import Iterable, Optional, Tuple
from aiokafka import AIOKafkaProducer
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from app.config.settings import settings
logger = logging.getLogger('producer_manager')
class ProducerManager:
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop = loop or asyncio.get_event_loop()
        self._producer: Optional[AIOKafkaProducer] = None
        self._start_lock = asyncio.Lock()
    async def start(self):
        async with self._start_lock:
            if self._producer is None:
                self._producer = AIOKafkaProducer(
                    bootstrap_servers=settings.kafka_bootstrap,
                    acks='all',
                    max_request_size=10_485_760,
                    linger_ms=5,
                    enable_idempotence=True,
                    loop=self.loop,
                )
                await self._producer.start()
                logger.info('Kafka producer started')
    async def stop(self):
        if self._producer:
            await self._producer.stop()
            logger.info('Kafka producer stopped')
    def _partition_key(self, key: Optional[bytes]):
        # Deterministic partitioning by hash of key; returns partition id as int
        if key is None: return None
        h = int(hashlib.sha1(key).hexdigest(), 16)
        return h % settings.kafka_partitions
    @retry(wait=wait_exponential(multiplier=0.5, min=0.5, max=10), stop=stop_after_attempt(5),
           retry=retry_if_exception_type(Exception))
    async def _send_once(self, topic: str, key: Optional[bytes], value: bytes, partition: Optional[int] = None):
        if partition is not None:
            return await self._producer.send_and_wait(topic, value=value, key=key, partition=partition)
        return await self._producer.send_and_wait(topic, value=value, key=key)
    async def send_batch(self, topic: str, messages: Iterable[Tuple[Optional[bytes], bytes]], dlq_topic: Optional[str] = None):
        results = []
        for key, value in messages:
            partition = self._partition_key(key)
            try:
                res = await self._send_once(topic, key, value, partition=partition)
                results.append(res)
            except Exception as exc:
                logger.exception('Failed to send; attempting DLQ: %s', exc)
                if dlq_topic:
                    try:
                        await self._send_once(dlq_topic, key, value)
                        logger.info('Published to DLQ %s', dlq_topic)
                    except Exception:
                        logger.exception('DLQ publish failed; dropping message')
                results.append(None)
        return results
