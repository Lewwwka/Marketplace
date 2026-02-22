import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    user_data = {
        "email": "user@example.com",
        "full_name": "string",
        "password": "stringst",
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"


@pytest.mark.asyncio
async def test_create_user_duplicate(client: AsyncClient):
    user_data = {
        "email": "user@example.com",
        "full_name": "string",
        "password": "stringst",
    }
    await client.post("/users/", json=user_data)
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert "Этот email уже зарегистрирован" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    user_data = {
        "email": "user2@example.com",
        "full_name": "string2",
        "password": "stringst2",
    }
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user2@example.com"
