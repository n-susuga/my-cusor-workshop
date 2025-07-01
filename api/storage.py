from .models import Product, ProductCreate


class InMemoryStorage:
    """インメモリストレージクラス"""

    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
        self._next_id: int = 1

    def create_product(self, product_create: ProductCreate) -> Product:
        """商品を作成して保存する"""
        product = Product(id=self._next_id, **product_create.model_dump())
        self._products[self._next_id] = product
        self._next_id += 1
        return product

    def get_product(self, product_id: int) -> Product | None:
        """IDで商品を検索する"""
        return self._products.get(product_id)
