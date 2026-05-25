import pytest

@pytest.mark.asyncio
async def test_list_users(authorized_client):
    res = await authorized_client.get("/api/v1/users/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)

test_user_info = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword"
}

async def create_user(authorized_client, user_info=None):
    if user_info is None:
        user_info = test_user_info

    res = await authorized_client.post(
        "/api/v1/users/",
        json={
            "username": user_info["username"],
            "email": user_info["email"],
            "password": user_info["password"]
        }
    )
    assert res.status_code == 201, "Failed to create user"
    data = res.json()
    assert data["email"] == user_info["email"], "Email in response does not match input"
    return data["id"]

async def delete_user(authorized_client, user_id):
    res = await authorized_client.delete(
        f"/api/v1/users/{user_id}"
    )
    assert res.status_code == 204, "Failed to delete user"

async def verify_user_deleted(authorized_client, user_id):
    res = await authorized_client.get(
        f"/api/v1/users/{user_id}"
    )
    assert res.status_code == 404, "Deleted user still accessible"

async def user_login(authorized_client, username=test_user_info["username"], password=test_user_info["password"], deleted=False):
    res = await authorized_client.post(
        "/api/v1/users/token",
        json={
            "username": username,
            "password": password
        }
    )
    if deleted:
        assert res.status_code == 401, "Deleted user should not be able to log in"
        return None

    assert res.status_code == 200, "Failed to log in"
    data = res.json()
    token = data.get("access_token")
    assert token is not None, "No access token returned"
    return token

@pytest.mark.asyncio
async def test_create_user(authorized_client):
    await create_user(authorized_client)

@pytest.mark.asyncio
async def test_create_delete_user(authorized_client):
    # First create a user to delete
    user_id = await create_user(authorized_client)

    # Now delete the user
    await delete_user(authorized_client, user_id)

    # Verify the user is deleted
    await verify_user_deleted(authorized_client, user_id)

@pytest.mark.asyncio
async def test_create_delete_login_user(authorized_client):

    # First create a user to delete
    user_id = await create_user(authorized_client)

    # Now delete the user
    await delete_user(authorized_client, user_id)

    # Verify the user is deleted by attempting to log in with the deleted user's credentials
    await user_login(authorized_client, deleted=True)

@pytest.mark.asyncio
async def test_create_login_delete_user(authorized_client):
    # First create a user to delete
    user_id = await create_user(authorized_client)

    # log in with the user's credentials
    token = await user_login(authorized_client)

    # Now delete the user
    await delete_user(authorized_client, user_id) 

    # update the authorized_client to include the token in the headers for subsequent requests
    authorized_client.headers["Bearer"] = token

    # now use the deleted user token to access a protected endpoint and verify it fails
    res = await authorized_client.get(
        "/api/v1/users/"
    )
    assert res.status_code == 401
