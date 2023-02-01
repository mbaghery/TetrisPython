import numpy as np

from kivy.app import App
from kivy.clock import Clock

from tetris.color import Color
from tetris.engine import Engine
from tetris.game import start_game
from tetris.generator import RandomPieceGenerator
from tetris.gui import GUI
from tetris.scorer import Scorer
from tetris.tetrominoes import tetrominoes


def _schedule(func, interval):
    Clock.schedule_once(lambda dt: func(), interval)


class MyTetrisApp(App):

    def build(self):
        gui = GUI(size=(700, 1400))
        start_game(
            engine=Engine(
                canvas=np.full(shape=(20, 10), fill_value=Color.Transparent),
                scorer=Scorer(score=0, level=1),
            ),
            random_piece_generator=RandomPieceGenerator(items=tetrominoes),
            schedule=_schedule,
            gui=gui,
        )
        return gui


if __name__ == '__main__':
    MyTetrisApp().run()
