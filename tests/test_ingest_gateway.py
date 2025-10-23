import json
import pytest
from fastapi.testclient import TestClient
from app.ingest.ingest_gateway import app

client = TestClient(app)

def test_ingest_empty_batch():
    resp = client.post('/v1/events', json={'events': []})
    assert resp.status_code == 400

def test_ingest_invalid_json():
    resp = client.post('/v1/events', data='not-json', headers={'content-type':'application/json'})
    assert resp.status_code == 400

def test_ingest_small_batch():
    payload = {'events':[{'agent_id':'a1','timestamp':1620000000,'metric':'cpu','value':0.5}]}
    resp = client.post('/v1/events', json=payload)
    assert resp.status_code == 202
    data = resp.json()
    assert data['count'] == 1
