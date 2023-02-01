from unittest import TestCase

from tetris.generator import RandomPieceGenerator


class TestRandomPieceGenerator(TestCase):

    def setUp(self) -> None:
        self.items = [1, 2, 3, 4, 5]
        self.generator = RandomPieceGenerator(items=self.items)

    def test_all_items_are_drawn(self):
        expected = self.items
        actuals = [self.generator.draw() for _ in range(len(self.items))]

        for actual in actuals:
            self.assertIn(actual, expected)
            expected.remove(actual)

    def test_all_items_are_drawn_twice(self):
        expected = self.items * 2
        actuals = [self.generator.draw() for _ in range(2 * len(self.items))]

        for actual in actuals:
            self.assertIn(actual, expected)
            expected.remove(actual)
