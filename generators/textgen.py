import generator
import pyglet.text
from pyglet.gl import *


class TextGen(generator.Generator):
    def __init__(self, text='TextGen', font_name='Inconsolata', font_size = 18):
        self.seed = {}
        self.params = {'red': self.g_color_range(),
                       'green': self.g_color_range(),
                       'blue': self.g_color_range(),
                       'alpha': self.g_int_span(75, 150),
                       'x': self.g_constant(0),
                       'y': self.g_constant(0)
                      }

        self.label = pyglet.text.Label()
        self.label.font_name = font_name
        self.label.font_size = font_size
        self.label.x = 0
        self.label.y = 0
        self.label.anchor_x = 'center'
        self.label.anchor_y = 'center'
        self.label.text = text


    def render(self):
        if self.seed:
            self.label.color = (self.seed['red'], self.seed['green'],
                                self.seed['blue'], self.seed['alpha'])
            self.label.draw()

