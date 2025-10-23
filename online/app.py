from fastapi import FastAPI
from online.api.endpoints import router as rec_router

app = FastAPI(title='Recommender Service')
app.include_router(rec_router, prefix='/v1')
