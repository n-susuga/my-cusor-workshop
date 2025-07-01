from .models import Product


class InMemoryStorage:
    """インメモリストレージクラス"""

    def __init__(self) -> None:
        self._products: dict[int, Product] = {}
        self._next_id: int = 1
