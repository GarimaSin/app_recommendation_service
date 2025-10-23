import redis, os, json
REDIS_URL = os.getenv('REDIS_URL','redis://localhost:6379/0')
class Cache:
    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL)
    def get_recs(self, user_id, k):
        key = f'recs:{user_id}:{k}'
        v = self.client.get(key)
        if v:
            return json.loads(v)
        return None
    def set_recs(self, user_id, k, recs, ttl=5):
        key = f'recs:{user_id}:{k}'
        self.client.set(key, json.dumps(recs), ex=ttl)
