import math
import logorator
import pyglet.graphics, pyglet.image
from pyglet.gl import *
import lsys

def _lsys_forward_func(state):
    d = state.get("d", math.radians(90))
    s = state.get("s", 10)
    a = state.get("a")
    x = (state.get("x") + (s * math.cos(a)))
    y = (state.get("y") + (s * math.sin(a)))

    pyglet.graphics.draw(2, GL_LINES,
        ('v2f', (state.get("x"), state.get("y"), x, y)))

    return {"x":x,
            "y":y,
            "a":a,
            "s":s,
            "d":d}
"""
"""
class LSysGen(logorator.Generator):
    """

    """

    def __init__(self, height, width, pos):
        self.seed = {}
        self.pos = pos
        self.params = {'red': self.g_color_range(),
                       'green': self.g_color_range(),
                       'blue': self.g_color_range(),
                       'alpha': self.g_int_span(75, 150),
                       'startx': self.g_int_const(10), #self.g_int_span(-10, 10),
                       'starty': self.g_int_const(50), #self.g_int_span(-10, 10),
                       'thickness': self.g_int_span(8, 20),
                       'angle': self.g_int_const(120),
                       'step': self.g_int_const(3)}

        self.sierpinski_tri = lsys.LSys("F",
                              {"F":"B-F-B", "B":"BB"},
                              4)

    def render(self, layer):
        if self.seed:
            (x, y) = self.pos
            self.sierpinski_state = {"x":(self.seed["startx"] + x),
                                     "y":(self.seed["starty"] + y),
                                     "a":0.0,
                                     "s":self.seed["step"],
                                     "d":self.seed["angle"]}

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            glColor4ub(self.seed['red'], self.seed['green'],
                       self.seed['blue'], self.seed['alpha'])
            self.sierpinski_tri.parse(self.sierpinski_state,
                                      self.sierpinski_tri.commands,
                                       _lsys_forward_func)
            
