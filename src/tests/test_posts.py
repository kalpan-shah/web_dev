from httpx import AsyncClient, ASGITransport
from app.main import app

import pytest

# conts
TITLE = "We are Testing"
CONTENT = "As we are supposed to test this API, we are testing it."

@pytest.mark.asyncio
async def test_create_post():
    # Define the transport with your app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/api/v1/posts/",
            json={
                "title": TITLE,
                "content": CONTENT
            }
        )
        assert res.status_code == 200
        data =  res.json()
        assert data["title"] == TITLE

@pytest.mark.asyncio
async def test_list_posts():
    # Define the transport with your app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/api/v1/posts/")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
