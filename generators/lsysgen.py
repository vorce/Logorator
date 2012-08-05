import math
import logorator
import pyglet.graphics, pyglet.image
from pyglet.gl import *

"""
Hmm, one generator for each different l-system should be good.
This file should instead be called something like
DragonCurveLsys or KochLSys
"""
class LSysGen(logorator.Generator):
    """

    """

    def __init__(self, height, width, pos):
        self.pos = pos
        self.seed = {}
        self.params = {'red': self.g_color_range(),
                       'green': self.g_color_range(),
                       'blue': self.g_color_range(),
                       'alpha': self.g_int_span(75, 150),
                       'startx': self.g_int_const(0), #self.g_int_span(-10, 10),
                       'starty': self.g_int_const(0), #self.g_int_span(-10, 10),
                       'thickness': self.g_int_span(8, 20),
                       'iterations': self.g_int_span(3, 10),
                       'angle': self.g_int_range(359),
                       'axiom': self.g_char('FXB-+[]', 1, 4),
                       'substitutions': self.g_subs('FXB-+[]')}

    def render(self, layer):
        pass

    
