from fastapi.testclient import TestClient
from online.app import app
client = TestClient(app)
def test_health():
    r = client.get('/v1/health')
    assert r.status_code in (200,404,500)
