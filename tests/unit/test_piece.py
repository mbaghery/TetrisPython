from unittest import TestCase

import numpy as np

from tetris.piece import Piece
from tetris.color import Color

Canvas = np.ndarray


class TestPiece(TestCase):

    def setUp(self) -> None:
        self.piece = Piece.from_2d_bool_list(
            cells=[
                [False, False, False],
                [True, True, True],
            ],
            position=(1, 0),
            color=Color.Red,
        )

    def assert_pieces_equal(self, expected: Piece, actual: Piece):
        self.assertEqual(expected, actual)
        self.assertIsNot(expected, actual)

    def test_new_piece(self):
        new_piece = self.piece.copy()

        self.assert_pieces_equal(self.piece, new_piece)

    def test_rotate_right_90(self):
        expected_piece = Piece.from_2d_bool_list(
            cells=[
                [True, False],
                [True, False],
                [True, False],
            ],
            position=(1, 0),
            color=Color.Red,
        )
        actual_piece = self.piece.rotate_clockwise()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_rotate_right_180(self):
        expected_piece = Piece.from_2d_bool_list(
            cells=[
                [True, True, True],
                [False, False, False],
            ],
            position=(1, 0),
            color=Color.Red,
        )
        actual_piece = self.piece.rotate_clockwise().rotate_clockwise()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_rotate_right_270(self):
        expected_piece = Piece.from_2d_bool_list(
            cells=[
                [False, True],
                [False, True],
                [False, True],
            ],
            position=(1, 0),
            color=Color.Red,
        )
        actual_piece = self.piece.rotate_clockwise().rotate_clockwise(
        ).rotate_clockwise()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_rotate_right_360(self):
        expected_piece = self.piece
        actual_piece = self.piece.rotate_clockwise().rotate_clockwise(
        ).rotate_clockwise().rotate_clockwise()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_right_left(self):
        expected_piece = self.piece
        actual_piece = self.piece.rotate_clockwise().rotate_counterclockwise()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_left_right(self):
        expected_piece = self.piece
        actual_piece = self.piece.rotate_counterclockwise().rotate_clockwise()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_rotate_left_90(self):
        expected_piece = Piece.from_2d_bool_list(
            cells=[
                [False, True],
                [False, True],
                [False, True],
            ],
            position=(1, 0),
            color=Color.Red,
        )
        actual_piece = self.piece.rotate_counterclockwise()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_move_down(self):
        expected_piece = Piece.from_2d_bool_list(
            cells=[
                [False, False, False],
                [True, True, True],
            ],
            position=(2, 0),
            color=Color.Red,
        )
        actual_piece = self.piece.move_down()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_move_right(self):
        expected_piece = Piece.from_2d_bool_list(
            cells=[
                [False, False, False],
                [True, True, True],
            ],
            position=(1, 1),
            color=Color.Red,
        )
        actual_piece = self.piece.move_right()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_move_left(self):
        expected_piece = Piece.from_2d_bool_list(
            cells=[
                [False, False, False],
                [True, True, True],
            ],
            position=(1, -1),
            color=Color.Red,
        )
        actual_piece = self.piece.move_left()

        self.assert_pieces_equal(expected_piece, actual_piece)

    def test_canvas_has_space(self):
        canvas = np.array([
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Red, Color.Transparent],
        ])

        piece = Piece.from_2d_bool_list(
            cells=[
                [False, True, False],
                [True, True, True],
            ],
            position=(0, 0),
            color=Color.Red,
        )

        self.assertTrue(piece.is_inside(canvas))
        self.assertTrue(piece.fits_in(canvas))

    def test_canvas_has_no_space(self):
        canvas = np.array([
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Red, Color.Transparent],
        ])

        piece = Piece.from_2d_bool_list(
            cells=[
                [False, True, False],
                [True, True, True],
            ],
            position=(1, 0),
            color=Color.Red,
        )

        self.assertTrue(piece.is_inside(canvas))
        self.assertFalse(piece.fits_in(canvas))

    def test_piece_outside(self):
        canvas = np.array([
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Transparent, Color.Transparent],
            [Color.Transparent, Color.Red, Color.Transparent],
        ])

        piece = Piece.from_2d_bool_list(
            cells=[
                [False, True, False],
                [True, True, True],
            ],
            position=(-1, 0),
            color=Color.Red,
        )

        self.assertFalse(piece.is_inside(canvas))
        self.assertFalse(piece.fits_in(canvas))
