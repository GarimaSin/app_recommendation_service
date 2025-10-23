from fastapi import APIRouter, HTTPException
from online.api.schemas import RecRequest, RecResponse, RecItem
from online.core.recommender import Recommender
from online.storage.redis_store import RedisFeatureStore
from online.producers.kafka_producer import KafkaProducerWrapper

router = APIRouter()
rec = Recommender()
store = RedisFeatureStore()
producer = KafkaProducerWrapper()

@router.post('/recommend', response_model=RecResponse)
async def recommend(req: RecRequest):
    # Try to get user embedding
    vec = store.get_user_embedding(req.user_id)
    if vec is None:
        # fallback to global average embedding from models
        vec = rec.get_default_vector()
    try:
        ids = rec.recommend_by_vector(vec, k=req.k)
    except Exception as e:
        ids = rec.recommend_popular(k=req.k)
    # prepare response
    recs = [RecItem(app_id=i) for i in ids]
    # emit impression event (fire and forget)
    try:
        await producer.produce_impression(req.user_id, [r.app_id for r in recs])
    except Exception:
        pass
    return RecResponse(user_id=req.user_id, recs=recs)
