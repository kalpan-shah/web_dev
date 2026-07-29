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

# Testing update
# 1. Update the title and status
@pytest.mark.asyncio
async def test_update_todo_high_level_fields(authorized_client):
    # create a todo first
    res = await authorized_client.post(
        "/api/v1/todo/",
        json=test_todo
    )
    assert res.status_code == 200
    data =  res.json()
    todo_id = data["id"] 
        
    # update the todo Title
    update_title = {
        "title": "Updated Test Todo"
    }
    res = await authorized_client.patch(
        f"/api/v1/todo/{todo_id}",
        json=update_title
    )
    assert res.status_code == 200
    data = res.json()
    assert data["title"] == update_title["title"]

    # update the todo status
    update_status = {
        "status": "skipped"
    }
    res = await authorized_client.patch(
        f"/api/v1/todo/{todo_id}",
        json=update_status
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == update_status["status"]


@pytest.mark.asyncio
async def test_update_todo_nested_fields(authorized_client):
    # create a todo first
    res = await authorized_client.post(
        "/api/v1/todo/",
        json=test_todo
    )
    assert res.status_code == 200
    data =  res.json()
    todo_id = data["id"]

    # id of one of the items
    item_id = data["items"][0]["id"]

    # Add to the todo items
    new_item = {
        "items": [
            {"item": "New Sub-task", "is_checked": False}
        ]
    }
    res = await authorized_client.patch(
        f"/api/v1/todo/{todo_id}",
        json=new_item
    )
    assert res.status_code == 200
    data = res.json()
    assert any(item["item"] == "New Sub-task" for item in data["items"])

    # Update an existing todo item
    update_item = {
        "items": [
            {"id": item_id, "item": "Updated Sub-task", "is_checked": True}
        ]
    }
    res = await authorized_client.patch(
        f"/api/v1/todo/{todo_id}",
        json=update_item
    )
    assert res.status_code == 200
    data = res.json()
    updated_item = next(item for item in data["items"] if item["id"] == item_id)
    assert updated_item["item"] == "Updated Sub-task"
    assert updated_item["is_checked"] == True

