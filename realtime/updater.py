import asyncio, os, json, numpy as np
from aiokafka import AIOKafkaConsumer
from online.storage.redis_store import RedisFeatureStore
KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP','localhost:9092')
TOPIC = os.getenv('KAFKA_TOPIC','events.impressions')
async def run_consumer():
    consumer = AIOKafkaConsumer(TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP, group_id='realtime-updater', auto_offset_reset='earliest')
    await consumer.start()
    store = RedisFeatureStore()
    try:
        async for msg in consumer:
            payload = json.loads(msg.value.decode('utf-8'))
            uid = payload.get('user_id')
            recs = payload.get('recs', [])
            if not uid: continue
            # Simple online update: set random vector or small perturbation
            vec = np.random.rand(64).astype('float32')
            store.set_user_embedding(uid, vec)
    finally:
        await consumer.stop()
if __name__=='__main__':
    asyncio.run(run_consumer())
