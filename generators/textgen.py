import math
import logorator
import pyglet.text
from pyglet.gl import *


class TextGen(logorator.Generator):
    def __init__(self):
        self.seed = {}
        self.params = {'red': self.g_color_range(),
                       'green': self.g_color_range(),
                       'blue': self.g_color_range(),
                       'alpha': self.g_int_span(75, 150),
                       'x': self.g_int_const(0),
                       'y': self.g_int_const(0)
                      }

        self.label = pyglet.text.Label()
        self.label.font_name = 'Inconsolata'
        self.label.font_size = 18
        self.label.x = 0
        self.label.y = 0
        self.label.anchor_x = 'center'
        self.label.anchor_y = 'center'
        self.label.text = 'TextGen'

    def render(self, layer):
        if self.seed:
            self.label.color = (self.seed['red'], self.seed['green'],
                                self.seed['blue'], self.seed['alpha'])
            self.label.draw()
