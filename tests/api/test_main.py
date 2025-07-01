import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


@pytest.mark.parametrize(
    ("payload", "error_message"),
    [
        ({"name": "", "price": 1000}, "String should have at least 1 character"),
        ({"name": "テスト商品", "price": 0}, "Input should be greater than 0"),
        ({"name": "テスト商品", "price": -1}, "Input should be greater than 0"),
    ],
)
@pytest.mark.anyio
async def test_create_product_with_invalid_data_returns_422(
    payload: dict[str, str | int],
    error_message: str,
) -> None:
    """不正なデータで商品作成リクエストを送信すると、ステータスコード422とエラーメッセージが返ること"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/items", json=payload)

    assert response.status_code == 422
    assert error_message in response.text


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


@pytest.mark.anyio
async def test_get_product_returns_200_and_product() -> None:
    """存在する商品IDでGETリクエストを送信すると、ステータスコード200と商品情報が返ること"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # まず商品を作成
        payload = {"name": "取得用テスト商品", "price": 500}
        create_response = await client.post("/items", json=payload)
        assert create_response.status_code == 201
        created_product_id = create_response.json()["id"]

        # 作成した商品を取得
        get_response = await client.get(f"/items/{created_product_id}")

    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == created_product_id
    assert data["name"] == "取得用テスト商品"
    assert data["price"] == 500


@pytest.mark.anyio
async def test_get_non_existent_product_returns_404() -> None:
    """存在しない商品IDでGETリクエストを送信すると、ステータスコード404が返ること"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/items/999")
    assert response.status_code == 404
