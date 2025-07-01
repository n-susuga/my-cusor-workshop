import httpx
import pytest
from httpx import Response
from pytest_httpx import HTTPXMock

from ui.main import check_api_status

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
