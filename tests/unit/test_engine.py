from unittest import TestCase
from unittest.mock import Mock
import numpy as np

from tetris.engine import Engine, GameStatus, clear_full_rows
from tetris.piece import Color, Piece

Canvas = np.ndarray


class TestFuncs(TestCase):

    def test_init(self):
        actual = np.full(shape=(2, 3), fill_value=Color.Transparent)
        expected = np.array([
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Transparent, Color.Transparent],
        ])
        np.testing.assert_equal(actual, expected)

    def test_cleanup_one_row(self):
        a = np.array([
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Red, Color.Yellow],
            [Color.Red, Color.Blue, Color.Transparent],
            [Color.Blue, Color.Blue, Color.Red],
        ])

        expected_array = np.array([
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Red, Color.Yellow],
            [Color.Red, Color.Blue, Color.Transparent],
        ])
        actual_array, _ = clear_full_rows(a)

        np.testing.assert_equal(actual_array, expected_array)

    def test_cleanup_two_rows(self):
        a = np.array([
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Yellow, Color.Cyan, Color.Red],
            [Color.Transparent, Color.Red, Color.Yellow],
            [Color.Red, Color.Blue, Color.Transparent],
            [Color.Blue, Color.Blue, Color.Red],
        ])

        expected_array = np.array([
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Red, Color.Yellow],
            [Color.Red, Color.Blue, Color.Transparent],
        ])
        actual_array, _ = clear_full_rows(a)

        np.testing.assert_equal(actual_array, expected_array)


class TestBoardOutsidePieces(TestCase):

    def setUp(self) -> None:
        self.engine = Engine(
            canvas=np.full(shape=(5, 4), fill_value=Color.Transparent),
            scorer=Mock(),
        )

    def test_gameover(self):
        long_piece = Piece.from_2d_bool_list(
            cells=[
                [True],
                [True],
                [True],
                [True],
                [True],
            ],
            position=(0, 0),
            color=Color.Red,
        )

        self.engine.add_piece(long_piece)
        self.engine.move_down()
        status = self.engine.add_piece(long_piece)
        self.assertEqual(GameStatus.GameOver, status)

    def test_add_pieces_outside_1(self):
        piece_1 = Piece.from_2d_bool_list(
            cells=[
                [False, True, False],
                [True, True, True],
            ],
            position=(0, -1),
            color=Color.Red,
        )
        self.assertRaises(ValueError, self.engine.add_piece, piece_1)

    def test_add_pieces_outside_2(self):
        piece_2 = Piece.from_2d_bool_list(
            cells=[
                [False, True, False],
                [True, True, True],
            ],
            position=(-1, 0),
            color=Color.Red,
        )
        self.assertRaises(ValueError, self.engine.add_piece, piece_2)

    def test_add_pieces_outside_3(self):
        piece_3 = Piece.from_2d_bool_list(
            cells=[
                [False, True, False],
                [True, True, True],
            ],
            position=(0, 2),
            color=Color.Red,
        )

        self.assertRaises(ValueError, self.engine.add_piece, piece_3)

    def test_add_pieces_outside_4(self):
        piece_4 = Piece.from_2d_bool_list(
            cells=[
                [False, True, False],
                [True, True, True],
            ],
            position=(4, 0),
            color=Color.Red,
        )

        self.assertRaises(ValueError, self.engine.add_piece, piece_4)


class TestPiecesInside(TestCase):

    def setUp(self) -> None:
        piece = Piece.from_2d_bool_list(
            cells=[
                [False, True, False],
                [True, True, True],
            ],
            position=(0, 0),
            color=Color.Red,
        )

        self.engine = Engine(
            canvas=np.full(shape=(5, 4), fill_value=Color.Transparent),
            scorer=Mock(),
        )

        self.engine.add_piece(piece)

    def test_add_piece_inside(self):
        expected_canvas = np.array([
            [
                Color.Transparent,
                Color.Red,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Red,
                Color.Red,
                Color.Red,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
        ])
        actual_canvas = self.engine.canvas

        np.testing.assert_equal(actual_canvas, expected_canvas)

    def test_bottomout(self):
        status = self.engine.move_down()
        self.assertEqual(GameStatus.Active, status)

        status = self.engine.move_down()
        self.assertEqual(GameStatus.Active, status)

        status = self.engine.move_down()
        self.assertEqual(GameStatus.Active, status)

        status = self.engine.move_down()
        self.assertEqual(GameStatus.Inactive, status)

        expected_canvas = np.array([
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Red,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Red,
                Color.Red,
                Color.Red,
                Color.Transparent,
            ],
        ])
        actual_canvas = self.engine.canvas

        np.testing.assert_equal(actual_canvas, expected_canvas)

    def test_softdrop(self):
        status = self.engine.move_down()
        self.assertEqual(GameStatus.Active, status)

        status = self.engine.soft_drop()
        self.assertEqual(GameStatus.Active, status)

        expected_canvas = np.array([
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Red,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Red,
                Color.Red,
                Color.Red,
                Color.Transparent,
            ],
        ])

        np.testing.assert_equal(self.engine.canvas, expected_canvas)

    def test_harddrop(self):
        status = self.engine.move_down()
        self.assertEqual(GameStatus.Active, status)

        status = self.engine.hard_drop()
        self.assertEqual(GameStatus.Inactive, status)

        expected_canvas = np.array([
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Transparent,
                Color.Red,
                Color.Transparent,
                Color.Transparent,
            ],
            [
                Color.Red,
                Color.Red,
                Color.Red,
                Color.Transparent,
            ],
        ])

        np.testing.assert_equal(self.engine.canvas, expected_canvas)
