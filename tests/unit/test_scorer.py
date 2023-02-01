from unittest import TestCase

from tetris.scorer import Scorer


class TestScorer(TestCase):

    def setUp(self) -> None:
        self.scorer = Scorer(score=0, level=1)

    def test_one_level_up(self):
        self.scorer.add_score(n_lines_cleared=4)
        self.scorer.add_score(n_lines_cleared=4)
        self.scorer.add_score(n_lines_cleared=4)

        self.assertEqual(2, self.scorer.level)

        self.scorer.add_score(n_lines_cleared=4)
        self.scorer.add_score(n_lines_cleared=4)

        self.assertEqual(3, self.scorer.level)
