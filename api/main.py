from fastapi import FastAPI, HTTPException

from .models import Product, ProductCreate
from .storage import InMemoryStorage

app = FastAPI(title="商品管理API")
storage = InMemoryStorage()


@app.post("/items", response_model=Product, status_code=201)
async def create_item(item: ProductCreate) -> Product:
    """商品を作成する"""
    return storage.create_product(item)


@app.get("/items/{item_id}", response_model=Product)
async def get_item(item_id: int) -> Product:
    """IDで商品を取得する"""
    product = storage.get_product(item_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/health", status_code=200)
async def health_check() -> dict[str, str]:
    """ヘルスチェックエンドポイント"""
    return {"status": "ok"}
