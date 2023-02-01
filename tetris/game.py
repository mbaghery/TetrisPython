from functools import partial
from typing import Callable

from tetris.engine import Engine, GameStatus
from tetris.generator import RandomPieceGenerator
from tetris.gui import GUI


def start_game(
    engine: Engine,
    gui: GUI,
    random_piece_generator: RandomPieceGenerator,
    schedule: Callable,
):
    Game(
        engine=engine,
        random_piece_generator=random_piece_generator,
        schedule=schedule,
        gui=gui,
    )


class Game:

    def __init__(
        self,
        engine: Engine,
        gui: GUI,
        random_piece_generator: RandomPieceGenerator,
        schedule: Callable,
    ) -> None:
        self._engine = engine
        self._gui = gui
        self._random_piece_generator = random_piece_generator
        self._schedule = schedule

        self._gui.bind_keys(
            on_enter_down=self._start_game,
            on_right_down=partial(self._on_key_down, engine.move_right),
            on_left_down=partial(self._on_key_down, engine.move_left),
            on_up_down=partial(self._on_key_down, engine.rotate_clockwise),
            on_down_down=partial(self._on_key_down, engine.soft_drop),
            on_spacebar_down=partial(self._on_key_down, engine.hard_drop),
        )

    def _on_key_down(self, func):
        func()
        self._gui.draw(self._engine.canvas)

    def _start_game(self):
        self._schedule(self._step_forward, 0)

    def _step_forward(self):
        status = self._engine.move_down()
        if status == GameStatus.Inactive:
            status = self._engine.add_piece(
                self._random_piece_generator.draw())

        self._gui.draw(self._engine.canvas)

        if status == GameStatus.GameOver:
            self._gui.gameover()
        else:
            self._schedule(self._step_forward, 1 / self._engine.level)
