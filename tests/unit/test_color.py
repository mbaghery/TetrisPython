from unittest import TestCase

from tetris.color import Color


class TestColor(TestCase):

    def test_equal(self):
        self.assertEqual(Color.Yellow, Color.Yellow)
        self.assertNotEqual(Color.Yellow, Color.Transparent)

    def test_sum_two_transparents(self):
        self.assertEqual(Color.Yellow + Color.Transparent, Color.Yellow)
        self.assertEqual(Color.Transparent + Color.Yellow, Color.Yellow)

    def test_multiplication(self):
        self.assertEqual(Color.Yellow * True, Color.Yellow)
        self.assertEqual(Color.Yellow * False, Color.Transparent)

    def test_right_multiplication(self):
        self.assertEqual(True * Color.Yellow, Color.Yellow)
        self.assertEqual(False * Color.Yellow, Color.Transparent)
