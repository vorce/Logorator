import pyglet
from pyglet.gl import *

class Hud(object):
    def __init__(self, win):
        helv = pyglet.font.load('Helvetica', win.width / 15.0)
        self.text = pyglet.font.Text(helv,
                              'Logorator',
                              x=win.width / 2,
                              y=win.height / 2,
                              halign=pyglet.font.Text.CENTER,
                              valign=pyglet.font.Text.CENTER,
                              color=(1, 1, 1, 0.5),
                             )
        self.fps = pyglet.clock.ClockDisplay()

    def draw(self):
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        self.text.draw()
        self.fps.draw()

