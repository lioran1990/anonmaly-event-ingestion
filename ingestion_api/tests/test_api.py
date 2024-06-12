import pytest
from httpx import AsyncClient
from ingestion_api.api import app


@pytest.mark.asyncio
async def test_ingest_event_success(mocker):
    # Mocking the publish_event function to assume it always succeeds
    mocker.patch('ingestion_api.api.publish_event', return_value=None)

    # Define a sample payload that matches the AnomalyEvent model
    payload = {
        "id": "123452",
        "event_id": "52572",
        "role_id": "role123",
        "event_type": "CreateInstance",
        "event_timestamp": "1717970237",
        "affected_assets": ["asset1", "asset2"]
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ingest", json=payload)
        assert response.status_code == 200
        assert response.json() == {"data": {"status": "success"}, "metadata": {"request_id": "123452"}}


@pytest.mark.asyncio
async def test_ingest_event_failure(mocker):
    # Simulating an exception in the publish_event function
    mocker.patch('ingestion_api.api.publish_event', side_effect=Exception("Connection failed"))

    payload = {
        "id": "123452",
        "event_id": "52572",
        "role_id": "role123",
        "event_type": "CreateInstance",
        "event_timestamp": "1717970237",
        "affected_assets": ["asset1", "asset2"]
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ingest", json=payload)
        assert response.status_code == 500
        assert response.json() == {"detail": "Error publishing event"}
