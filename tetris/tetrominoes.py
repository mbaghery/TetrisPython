from tetris.color import Color
from tetris.piece import Piece

l_piece = Piece.from_2d_bool_list(
    cells=[
        [True, False, False],
        [True, True, True],
    ],
    position=(0, 3),
    color=Color.Orange,
)

j_piece = Piece.from_2d_bool_list(
    cells=[
        [False, False, True],
        [True, True, True],
    ],
    position=(0, 4),
    color=Color.Blue,
)

o_piece = Piece.from_2d_bool_list(
    cells=[
        [True, True],
        [True, True],
    ],
    position=(0, 4),
    color=Color.Yellow,
)

i_piece = Piece.from_2d_bool_list(
    cells=[
        [True],
        [True],
        [True],
        [True],
    ],
    position=(0, 4),
    color=Color.Cyan,
)

t_piece = Piece.from_2d_bool_list(
    cells=[
        [False, True, False],
        [True, True, True],
    ],
    position=(0, 3),
    color=Color.Purple,
)

s_piece = Piece.from_2d_bool_list(
    cells=[
        [False, True, True],
        [True, True, False],
    ],
    position=(0, 3),
    color=Color.Green,
)

z_piece = Piece.from_2d_bool_list(
    cells=[
        [True, True, False],
        [False, True, True],
    ],
    position=(0, 4),
    color=Color.Red,
)

tetrominoes = [l_piece, j_piece, o_piece, i_piece, t_piece, s_piece, z_piece]
