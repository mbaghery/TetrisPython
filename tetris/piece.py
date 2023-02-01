from typing import List, Optional, Tuple

import numpy as np

from tetris.color import Color

Canvas = np.ndarray


class Piece:

    def __init__(
        self,
        cells: List[List[Color]],
        position: Optional[Tuple[int, int]] = None,
    ) -> None:
        self._cells = np.atleast_2d(cells)
        self._position = position if position is not None else (0, 0)

    @classmethod
    def from_2d_bool_list(
        cls,
        cells: List[List[bool]],
        color: Color,
        position: Optional[Tuple[int, int]] = None,
    ):
        return cls(cells=np.atleast_2d(cells) * color, position=position)

    def copy(self) -> "Piece":
        # no need to copy position since its a tuple and therefore immutable
        return self.__class__(
            cells=self._cells.copy(),
            position=self._position,
        )

    def __eq__(self, __o: object) -> bool:
        return (np.all(self._cells == __o._cells)
                and (self._position == __o._position))

    def _rotate(self, direction: str) -> "Piece":
        k = -1 if direction == 'right' else 1

        return self.__class__(
            cells=np.rot90(self._cells, k=k),
            position=self._position,
        )

    def rotate_clockwise(self) -> "Piece":
        return self._rotate(direction='right')

    def rotate_counterclockwise(self) -> "Piece":
        return self._rotate(direction='left')

    def _move(self, displacement: Tuple[int, int]) -> "Piece":
        return self.__class__(
            cells=self._cells.copy(),
            position=(self._position[0] + displacement[0],
                      self._position[1] + displacement[1]),
        )

    def move_down(self) -> "Piece":
        return self._move((1, 0))

    def move_right(self) -> "Piece":
        return self._move((0, 1))

    def move_left(self) -> "Piece":
        return self._move((0, -1))

    def is_inside(self, canvas: Canvas) -> bool:
        height_a, width_a = canvas.shape
        height_b, width_b = self._cells.shape
        pos_y, pos_x = self._position

        return (pos_x + width_b <= width_a) and (pos_x >= 0) and (
            pos_y + height_b <= height_a) and (pos_y >= 0)

    def _overlaps_with(self, canvas: Canvas) -> bool:
        height_b, width_b = self._cells.shape
        pos_y, pos_x = self._position

        return np.array(canvas[pos_y:pos_y + height_b, pos_x:pos_x + width_b][
            self._cells != Color.Transparent] != Color.Transparent).any()

    def fits_in(self, canvas: Canvas):
        return self.is_inside(
            canvas=canvas) and not self._overlaps_with(canvas=canvas)

    def merge_into(self, canvas: Canvas) -> Canvas:
        height_b, width_b = self._cells.shape
        pos_y, pos_x = self._position

        a = canvas.copy()
        a[pos_y:pos_y + height_b, pos_x:pos_x + width_b] += self._cells

        return a

    def __repr__(self) -> str:
        return str(self._cells)
