from pyglet.gl import *

class Camera(object):
    def __init__(self, win, zoom=1.0):
        self.win = win
        self.zoom = zoom

    def world(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width_ratio = self.win.width / self.win.height
        gluOrtho2D(-self.zoom * width_ratio,
                   self.zoom * width_ratio,
                   -self.zoom,
                   self.zoom)

    def hud(self):
        glViewport(0, 0, self.win.width, self.win.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.win.width, 0, self.win.height)

