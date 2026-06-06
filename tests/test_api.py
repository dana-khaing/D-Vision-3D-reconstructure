"""Basic smoke tests for the FastAPI endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


async def test_create_and_list_event(client):
    r = await client.post("/api/v1/events", json={"name": "Test Party"})
    assert r.status_code == 201
    event = r.json()
    assert event["name"] == "Test Party"
    assert event["status"] == "created"

    r2 = await client.get("/api/v1/events")
    assert r2.status_code == 200
    ids = [e["id"] for e in r2.json()]
    assert event["id"] in ids


async def test_get_missing_event(client):
    r = await client.get("/api/v1/events/does-not-exist")
    assert r.status_code == 404
