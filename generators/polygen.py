import math
import generator
import pyglet.graphics, pyglet.image
from pyglet.gl import *

class PolyGen(generator.Generator):
    """
    Draws a polygon. Position, points and color is
    controlled by the seed.
    """

    def __init__(self):
        self.seed = {}
        self.params = {'red': self.g_color_range(),
                       'green': self.g_color_range(),
                       'blue': self.g_color_range(),
                       'alpha': self.g_int_span(75, 150),
                       'x': self.g_constant(0), #self.g_int_span(-10, 10),
                       'y': self.g_constant(0), #self.g_int_span(-10, 10),
                       'radius': self.g_int_span(8, 30),
                       'sides': self.g_int_span(3, 9),
                       'start_angle': self.g_int_range(359)}

    def render(self):
        if self.seed:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            glColor4ub(self.seed['red'], self.seed['green'],
                       self.seed['blue'], self.seed['alpha'])
            self.ngon(self.seed['x'], self.seed['y'],
                      self.seed['radius'],
                      self.seed['sides'], self.seed['start_angle'])

    def _concat(self, it):
        return list(y for x in it for y in x)
    
    def _iter_ngon(self, x, y, r, sides, start_angle = 0.0):
        rad = max(r, 0.01)
        rad_ = max(min(sides / rad / 2.0, 1), -1)
        da = math.pi * 2 / sides
        a = start_angle
        while a <= math.pi * 2 + start_angle:
            yield (x + math.cos(a) * r, y + math.sin(a) * r)
            a += da
    

    def ngon(self, x, y, r, sides, start_angle = 0.0):
        """
        Draw a polygon of n sides of equal length.
    
        @param x, y: center position
        @param r: radius
        @param sides: number of sides in the polygon
        @param start_angle: rotation of the entire polygon
        """
        points = self._concat(self._iter_ngon(x, y, r, sides, start_angle))
        pyglet.graphics.draw(len(points)/2, GL_TRIANGLE_FAN, ('v2f', points))
   
