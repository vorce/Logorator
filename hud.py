import pyglet
from pyglet.gl import *

class Hud(object):
    def __init__(self, win):
        #font = pyglet.font.load('Inconsolata', win.width / 15.0)
        """self.text = pyglet.font.Text(font,
                              'Logorator',
                              x=win.width / 2,
                              y=(win.height / 3),
                              halign=pyglet.font.Text.CENTER,
                              valign=pyglet.font.Text.CENTER,
                              color=(1, 1, 1, 0.5),
                             )
                             """
        #self.text = pyglet.text.Label('Hello')
        self.fps = pyglet.clock.ClockDisplay()

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #self.text.draw()
        self.fps.draw()
        #pass
