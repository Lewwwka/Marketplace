import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_to_basket(auth_client: AsyncClient):
    basket_data = {
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 2},
        ]
    }
    response = await auth_client.post("/orders/basket", json=basket_data)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Товар добавлен в корзину"


@pytest.mark.asyncio
async def test_list_basket(auth_client: AsyncClient):
    response = await auth_client.get("/orders/basket")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_clear_basket(auth_client: AsyncClient):
    response = await auth_client.delete("/orders/basket")
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Корзина очищена"


@pytest.mark.asyncio
async def test_list_orders(auth_client: AsyncClient):
    response = await auth_client.get("/orders/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
