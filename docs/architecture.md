Architecture overview:
- Online FastAPI service for recommendations
- Redis feature store and cache
- Kafka event bus for impressions and interactions
- Offline trainer builds item embeddings and Annoy index
- Realtime updater consumes events and updates user embeddings
