import streamlit as st


def main() -> None:
    """Streamlitアプリケーションのメイン関数"""
    st.set_page_config(
        page_title="商品管理アプリ",
        page_icon="📦",
        layout="wide",
    )

    # ヘッダー
    st.header("商品管理ダッシュボード")


if __name__ == "__main__":
    main()
