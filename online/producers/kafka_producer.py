import os, asyncio, json
from aiokafka import AIOKafkaProducer
KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP','localhost:9092')
TOPIC = os.getenv('KAFKA_TOPIC','events.impressions')
class KafkaProducerWrapper:
    def __init__(self):
        self._producer = None
    async def _ensure(self):
        if self._producer is None:
            self._producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
            await self._producer.start()
    async def produce_impression(self, user_id, recs):
        await self._ensure()
        msg = json.dumps({'user_id': user_id, 'recs': recs}).encode('utf-8')
        await self._producer.send_and_wait(TOPIC, msg)
    async def stop(self):
        if self._producer:
            await self._producer.stop()
