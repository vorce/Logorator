"""
Logorator is meant to be a prototype tool to assist with
creating generated graphic designs.

2012 Joel Carlbark (c)
"""
import sys

import pyglet
from pyglet.gl import *

import eventhandler
import utils
import hud
import world


class Logorator():
    def __init__(self, width, height, inp=None):
        pyglet.clock.set_fps_limit(60)

        config = Config(sample_buffers=1, samples=4,
                        depth_size=16, double_buffer=True,)

        self.window = pyglet.window.Window(width=width, height=height,
                                           config=config)

        self.world = world.World(self.window, inp)

        self.camera = utils.Camera(self.window, zoom=100)

        self.hud = hud.Hud(self.window)

        self.event_handler = eventhandler.Eventhandler(self.window)

    def start(self):
        glClearColor(0, 0, 0, 1)
        while not self.window.has_exit:
            self.window.dispatch_events()

            self.world.tick(self.event_handler)

            self.camera.world()
            self.world.draw()

            self.camera.hud()
            self.hud.draw()

            pyglet.clock.tick()
            self.window.flip()

if __name__ == "__main__":
    logorator = None

    if len(sys.argv) > 1:
        f = open(sys.argv[1], 'r')
        line = f.readline()
        inp = eval(line)  # hue, hue, hue
        if isinstance(inp, list):
            logorator = Logorator(800, 800, inp)
    else:
        logorator = Logorator(800, 800)

    logorator.start()
