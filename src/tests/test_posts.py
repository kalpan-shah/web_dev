import pytest
# from conftest import
# conts
TITLE = "We are Testing"
CONTENT = "As we are supposed to test this API, we are testing it."

@pytest.mark.asyncio
async def test_create_post(authorized_client):
    res = await authorized_client.post(
        "/api/v1/posts/",
        json={
            "title": TITLE,
            "content": CONTENT
        }
    )
    assert res.status_code == 200
    data =  res.json()
    assert data["title"] == TITLE 

    user_id = data["user_id"]

    res = await authorized_client.get(
        f"/api/v1/users/{user_id}"
    )
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == user_id


@pytest.mark.asyncio
async def test_list_posts(authorized_client):
    res = await authorized_client.get(
        "/api/v1/posts/"
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
