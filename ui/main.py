import asyncio

import httpx
import streamlit as st

API_URL = "http://localhost:8000"


async def check_api_status() -> bool:
    """APIサーバーの稼働状況を確認する"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/health")
            return response.status_code == 200
    except httpx.ConnectError:
        return False


def main() -> None:
    """Streamlitアプリケーションのメイン関数"""
    st.set_page_config(
        page_title="商品管理アプリ",
        page_icon="📦",
        layout="wide",
    )

    # ヘッダー
    st.header("商品管理ダッシュボード")

    # APIステータス表示
    if asyncio.run(check_api_status()):
        st.success("API正常稼働中")
    else:
        st.error("API接続エラー")


if __name__ == "__main__":
    main()
