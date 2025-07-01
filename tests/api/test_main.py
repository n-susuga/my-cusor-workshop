import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


@pytest.mark.anyio
async def test_create_product_returns_201_and_created_product() -> None:
    """商品作成リクエストを送信すると、ステータスコード201と作成された商品情報が返ること"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json={"name": "テスト商品", "price": 1000})

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert data["name"] == "テスト商品"
    assert data["price"] == 1000


@pytest.mark.anyio
async def test_health_check_returns_200() -> None:
    """/health にGETリクエストを送信すると、ステータスコード200と{"status": "ok"}が返ること"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
