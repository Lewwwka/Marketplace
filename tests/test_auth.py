import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):

    user_data = {
        "email": "user@example.com",
        "full_name": "string",
        "password": "stringst",
    }

    await client.post("/users/", json=user_data)

    login_data = {
        "email": "user@example.com",
        "password": "stringst",
    }
    response = await client.post("/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):

    user_data = {
        "email": "user1@example.com",
        "full_name": "string",
        "password": "stringst",
    }

    await client.post("/users/", json=user_data)

    login_data = {
        "email": "user1@example.com",
        "password": "123321123",
    }

    response = await client.post("/auth/login", json=login_data)
    assert response.status_code == 401
