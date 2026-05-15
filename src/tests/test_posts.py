import pytest
# from conftest import
# conts
TITLE = "We are Testing"
CONTENT = "As we are supposed to test this API, we are testing it."

@pytest.mark.asyncio
async def test_create_post(client):
    res = await client.post(
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
async def test_list_posts(client):
    res = await client.get("/api/v1/posts/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
