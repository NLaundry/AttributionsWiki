import asyncio

import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio()
async def test_create_factor(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    response = client.post(
        "http://localhost:8000/api/v1/factor/create",
        json={"description": "Test Factor"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test Factor"

    # Cleanup: delete the test factor
    # db.factor.delete(where={"description": "Test Factor"})
