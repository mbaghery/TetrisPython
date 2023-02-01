from typing import Callable

import numpy as np
from kivy import graphics as gfx
from kivy.core.window import Window
from kivy.uix.widget import Widget

from tetris.color import Color

Canvas = np.ndarray

kivy_colors = {
    Color.Black: (0, 0, 0),
    Color.Transparent: (0.1, 0.1, 0.1),
    Color.Red: (1, 0, 0),
    Color.Blue: (0, 0, 1),
    Color.Green: (0, 1, 0),
    Color.Orange: (1, 0.5, 0),
    Color.Cyan: (0, 1, 1),
    Color.Purple: (0.5, 0, 0.5),
    Color.Yellow: (1, 1, 0)
}


def do_nothing():
    pass


class GUI(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed,
            self,
            'text',
        )
        Window.size = (kwargs['size'][0] / 2, kwargs['size'][1] / 2)

        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass

    def draw(self, canvas: Canvas):
        self.canvas.clear()  # kivy has a canvas too
        self._draw(canvas=canvas)

    def _draw(self, canvas: Canvas):
        n_rows, n_cols = canvas.shape
        height, width = self.height, self.width
        cell_height, cell_width = height / n_rows, width / n_cols

        with self.canvas:
            for row_no in range(n_rows):
                for col_no in range(n_cols):
                    gfx.Color(*kivy_colors[canvas[row_no, col_no]], 1)
                    gfx.Rectangle(pos=(col_no * cell_width,
                                       (n_rows - 1 - row_no) * cell_height),
                                  size=(cell_width, cell_height))

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def gameover(self):
        print('gameover')

    def bind_keys(
        self,
        on_enter_down: Callable,
        on_right_down: Callable,
        on_left_down: Callable,
        on_up_down: Callable,
        on_down_down: Callable,
        on_spacebar_down: Callable,
    ):
        self._event_listeners = {
            'enter': on_enter_down,
            'right': on_right_down,
            'left': on_left_down,
            'up': on_up_down,
            'down': on_down_down,
            'spacebar': on_spacebar_down,
        }

        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self._event_listeners.get(keycode[1], do_nothing)()

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True
