from httpx import AsyncClient, ASGITransport
from app.main import app

import pytest

@pytest.mark.asyncio
async def test_health():
    # Define the transport with your app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/api/v1/health")
        assert res.status_code == 200
        assert res.json() == {"status": "probably okay"}
