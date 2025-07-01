import httpx
import pytest
from httpx import Response
from pytest_httpx import HTTPXMock

from ui.main import Product, check_api_status, get_product_by_id, register_product

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
async def test_register_product_failure_validation_error(httpx_mock: HTTPXMock) -> None:
    """商品登録がバリデーションエラーで失敗するケースをテストする"""
    product_data = {"name": "", "price": 1000}  # 無効なデータ
    error_response = {"detail": "Validation error"}

    httpx_mock.add_response(
        method="POST",
        url=f"{API_URL}/items",
        status_code=422,
        json=error_response,
    )

    result = await register_product(product_data["name"], product_data["price"])

    assert result is None


@pytest.mark.asyncio
async def test_get_product_by_id_success(httpx_mock: HTTPXMock) -> None:
    """IDによる商品検索が成功するケースをテストする"""
    product_id = 1
    response_data = {
        "id": product_id,
        "name": "テスト商品",
        "price": 1000,
        "created_at": "2023-01-01T00:00:00Z",
    }

    httpx_mock.add_response(
        method="GET",
        url=f"{API_URL}/items/{product_id}",
        status_code=200,
        json=response_data,
    )

    result = await get_product_by_id(product_id)

    assert isinstance(result, Product)
    assert result.id == product_id


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(httpx_mock: HTTPXMock) -> None:
    """存在しないIDで商品を検索した場合にNoneを返すことをテストする"""
    product_id = 999  # 存在しないID
    error_response = {"detail": "Product not found"}

    httpx_mock.add_response(
        method="GET",
        url=f"{API_URL}/items/{product_id}",
        status_code=404,
        json=error_response,
    )

    result = await get_product_by_id(product_id)

    assert result is None


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
