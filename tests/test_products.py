import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(auth_client: AsyncClient):
    product = {
        "name": "string",
        "description": "string",
        "price": 50,
        "stock": 10,
    }
    response = await auth_client.post("/products/", json=product)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "string"
    assert data["price"] == 50


@pytest.mark.asyncio
async def test_get_by_name_product(auth_client: AsyncClient):
    product = {
        "name": "string",
        "description": "string",
        "price": 50,
        "stock": 10,
    }
    create_response = await auth_client.post("/products/", json=product)
    assert create_response.status_code == 201

    product_name = create_response.json()["name"]
    response = await auth_client.get(f"/products/{product_name}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_product_invalid(auth_client: AsyncClient):
    product_name = {
        "name": "",
    }
    response = await auth_client.post("/products/", json=product_name)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_products(auth_client: AsyncClient):
    response = await auth_client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
