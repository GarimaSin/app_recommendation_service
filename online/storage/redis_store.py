import os, numpy as np, redis
REDIS_URL = os.getenv('REDIS_URL','redis://localhost:6379/0')
class RedisFeatureStore:
    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL)
    def get_user_embedding(self, user_id):
        key = f'user_emb:{user_id}'
        b = self.client.get(key)
        if not b:
            return None
        return np.frombuffer(b, dtype=np.float32)
    def set_user_embedding(self, user_id, vec, ex=7*24*3600):
        key = f'user_emb:{user_id}'
        self.client.set(key, np.asarray(vec, dtype=np.float32).tobytes(), ex=ex)
