import pytest
# from conftest import
# conts

test_todo = {
    "title": "Test Todo",  
    "items": [    
        {"item": "Create a Todo", "is_checked": False},
        {"item": "Create the same Todo again", "is_checked": False},
        {"item": "List all Todos", "is_checked": False},
        {"item": "Delete a Todo", "is_checked": False}
    ]
}

@pytest.mark.asyncio
async def test_create_todo(authorized_client):
    res = await authorized_client.post(
        "/api/v1/todo/",
        json=test_todo
    )
    assert res.status_code == 200
    data =  res.json()
    assert data["title"] == test_todo["title"] 

    user_id = data["user_id"]

    res = await authorized_client.get(
        f"/api/v1/users/{user_id}"
    )
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == user_id


@pytest.mark.asyncio
async def test_list_todos(authorized_client):
    res = await authorized_client.get(
        "/api/v1/todo/"
    )
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_delete_todo(authorized_client):
    # create a todo first
    res = await authorized_client.post(
        "/api/v1/todo/",
        json=test_todo
    )
    assert res.status_code == 200
    data =  res.json()
    todo_id = data["id"]
    # delete the todo
    res = await authorized_client.delete(
        f"/api/v1/todo/{todo_id}"
    )
    assert res.status_code == 204

    # check if the todo is deleted
    res = await authorized_client.get(
        f"/api/v1/todo/{todo_id}"
    )
    assert res.status_code == 404

