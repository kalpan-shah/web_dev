from httpx import AsyncClient
from app.main import app

import pytest

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get("/api/v1/health")
        assert res.status_code == 200
        assert res.json() == {"status": "probably okay"}
