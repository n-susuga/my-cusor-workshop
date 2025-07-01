import asyncio
from datetime import datetime

import httpx
import streamlit as st
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    """商品作成リクエストモデル"""

    name: str = Field(..., min_length=1, description="商品名")
    price: float = Field(..., gt=0, description="単価")


class Product(ProductCreate):
    """商品レスポンスモデル"""

    id: int = Field(..., description="商品ID")
    created_at: datetime = Field(default_factory=datetime.now, description="作成日時")


API_URL = "http://localhost:8000"


async def check_api_status() -> bool:
    """APIサーバーの稼働状況を確認する"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/health")
            return response.status_code == 200
    except httpx.ConnectError:
        return False


async def register_product(name: str, price: float) -> Product | None:
    """商品を登録する。成功した場合はProductモデルを、失敗した場合はNoneを返す"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/items",
                json={"name": name, "price": price},
            )
            response.raise_for_status()
            return Product(**response.json())
    except httpx.HTTPStatusError:
        return None
    except httpx.ConnectError:
        return None


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

    st.divider()

    # --- 商品登録フォーム ---
    st.subheader("商品を登録する")
    with st.form("register_form"):
        name = st.text_input("商品名", key="register_name")
        price = st.number_input("価格", min_value=0.0, step=0.01, key="register_price")
        submitted = st.form_submit_button("登録")

        if submitted:
            if not name:
                st.warning("商品名を入力してください。")
            else:
                with st.spinner("登録中..."):
                    product = asyncio.run(register_product(name, float(price)))

                if product:
                    st.success(f"商品を登録しました。ID: {product.id}")
                else:
                    st.error(
                        "商品の登録に失敗しました。入力内容やAPIの接続状況を確認してください。"
                    )


if __name__ == "__main__":
    main()
