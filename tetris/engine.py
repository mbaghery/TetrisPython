from enum import Enum
from typing import Tuple

import numpy as np
from tetris.color import Color

from tetris.piece import Piece
from tetris.scorer import Scorer

Canvas = np.ndarray


class GameStatus(Enum):
    Inactive = 0
    Active = 1
    GameOver = 2


class Engine:

    def __init__(
        self,
        canvas: Canvas,
        scorer: Scorer,
    ) -> None:
        self._canvas = canvas
        self._scorer = scorer

        self._current_piece: Piece = None

    @property
    def score(self) -> float:
        return self._scorer.score

    @property
    def level(self) -> float:
        return self._scorer.level

    @property
    def canvas(self) -> Canvas:
        if self._current_piece is None:
            return self._canvas
        else:
            return self._current_piece.merge_into(self._canvas)

    def add_piece(self, piece: Piece) -> GameStatus:
        if self._current_piece is not None:
            raise ValueError('Board has an active piece already.')

        self._current_piece = piece

        if piece.fits_in(self._canvas):
            return GameStatus.Active
        else:
            if piece.is_inside(self._canvas):
                return GameStatus.GameOver
            else:
                raise ValueError('Piece outside of the bounds of the board.')

    def move_right(self):
        if self._current_piece is None:
            return

        new_piece = self._current_piece.move_right()
        if new_piece.fits_in(self._canvas):
            self._current_piece = new_piece

    def move_left(self):
        if self._current_piece is None:
            return

        new_piece = self._current_piece.move_left()
        if new_piece.fits_in(self._canvas):
            self._current_piece = new_piece

    def rotate_clockwise(self):
        if self._current_piece is None:
            return

        new_piece = self._current_piece.rotate_clockwise()
        if new_piece.fits_in(self._canvas):
            self._current_piece = new_piece

    def soft_drop(self) -> GameStatus:
        self.move_down()
        status = self.move_down()

        return status

    def hard_drop(self) -> GameStatus:
        status = self.move_down()
        while status == GameStatus.Active:
            status = self.move_down()

        return status

    def move_down(self) -> GameStatus:
        if self._current_piece is None:
            return GameStatus.Inactive

        new_piece = self._current_piece.move_down()
        if new_piece.fits_in(self._canvas):
            self._current_piece = new_piece
            return GameStatus.Active
        else:
            self._canvas, n_lines_cleared = clear_full_rows(
                self._current_piece.merge_into(self._canvas))
            self._current_piece = None
            self._scorer.add_score(n_lines_cleared=n_lines_cleared)
            return GameStatus.Inactive

    def __repr__(self) -> str:
        return str(self.canvas)


def clear_full_rows(canvas: Canvas) -> Tuple[Canvas, int]:
    canvas_with_nonfull_rows = _delete_full_rows(canvas)

    height, _ = canvas.shape
    new_height, _ = canvas_with_nonfull_rows.shape

    return np.pad(
        canvas_with_nonfull_rows,
        pad_width=((height - new_height, 0), (0, 0)),
        mode='constant',
        constant_values=Color.Transparent,
    ), height - new_height


def _delete_full_rows(canvas: Canvas) -> Canvas:
    row_indices_to_remove = (canvas != Color.Transparent).all(axis=1)
    return np.delete(canvas, row_indices_to_remove, axis=0)