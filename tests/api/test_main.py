import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


@pytest.mark.anyio
async def test_sample() -> None:
    """仮のテスト"""
    assert True
