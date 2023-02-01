import random
from typing import List, TypeVar

T = TypeVar('T')


class RandomPieceGenerator:

    def __init__(self, items: List[T]) -> None:
        self._items = items
        self._items_still_unused = []

    def draw(self) -> T:
        if len(self._items_still_unused) == 0:
            self._items_still_unused = self._items.copy()

        result = random.choice(self._items_still_unused)
        self._items_still_unused.remove(result)

        return result