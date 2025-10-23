from pydantic import BaseModel
from typing import List

class RecRequest(BaseModel):
    user_id: str
    k: int = 10
    region: str = 'US'
    device: str = 'tv'

class RecItem(BaseModel):
    app_id: str

class RecResponse(BaseModel):
    user_id: str
    recs: List[RecItem]
