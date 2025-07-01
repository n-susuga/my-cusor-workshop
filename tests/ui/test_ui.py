import httpx
import pytest
from httpx import Response
from pytest_httpx import HTTPXMock

from ui.main import Product, check_api_status, register_product

# APIのエンドポイントURL
API_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_check_api_status_success(httpx_mock: HTTPXMock) -> None:
    """APIが正常な場合にTrueを返すことをテストする"""
    httpx_mock.add_response(
        method="GET",
        url=f"{API_URL}/health",
        status_code=200,
        json={"status": "ok"},
    )

    status = await check_api_status()
    assert status is True


@pytest.mark.asyncio
async def test_check_api_status_failure(httpx_mock: HTTPXMock) -> None:
    """APIが利用不可能な場合にFalseを返すことをテストする"""
    httpx_mock.add_exception(httpx.ConnectError("Connection failed"))

    status = await check_api_status()
    assert status is False


@pytest.mark.asyncio
async def test_register_product_success(httpx_mock: HTTPXMock) -> None:
    """商品登録が成功するケースをテストする"""
    product_data = {"name": "テスト商品", "price": 1000}
    response_data = {
        "id": 1,
        "name": "テスト商品",
        "price": 1000,
        "created_at": "2023-01-01T00:00:00Z",
    }

    httpx_mock.add_response(
        method="POST",
        url=f"{API_URL}/items",
        status_code=201,
        json=response_data,
    )

    result = await register_product(product_data["name"], product_data["price"])

    assert isinstance(result, Product)
    assert result.name == product_data["name"]
    assert result.price == product_data["price"]
