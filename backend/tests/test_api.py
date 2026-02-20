from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    c = TestClient(app)
    r = c.get('/api/health')
    assert r.status_code == 200
    assert 'status' in r.json()
