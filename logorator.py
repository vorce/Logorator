import random
import sys

import pyglet
from pyglet.gl import *

import eventhandler
import utils
import hud
import world

class Generator:
    """
    Basic generator contract/interface
    """
    def __init__(self, height, width, pos):
        self.pos = pos
        self.params = {}
        self.seed = {}

        #self.color_range = lambda: range(256)
        #self.color_range = g_int_range(255)
        #self.boolean_range = g_boolean_range() #lambda: [True, False]
        #self.int_range = g_int_range#lambda (x,): range(x)
        #self.int_span = lambda (a, b): range(a, b)
        #self.double_range = lambda: [random.random()] # use a generator instead?

    def g_int_range(self, m):
        while True:
            yield random.randint(0, m)

    def g_boolean_range(self):
        while True:
            yield [True, False][random.randint(0, 1)]

    def g_int_span(self, a, b):
        while True:
            yield random.randint(a, b)

    def g_double_range(self):
        while True:
            yield random.random()

    def g_color_range(self):
        return self.g_int_range(255)

    def g_int_const(self, c):
        while True:
            yield c

    def dump(self):
        return str(self.seed)

    def render(self, layer):
        raise NotImplementedException("Should implement this")

    def save_seed(self, filename):
        raise NotImplementedException("Should implement this")

    def load_seed(self, filename):
        raise NotImplementedException("Should implement this")


def init(width, height, inp=None):
    pyglet.clock.set_fps_limit(60)

    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)

    screen = pyglet.window.Window(width=width,
                                  height=height, config=config)

    w = world.World(screen, inp)

    camera = utils.Camera(screen, zoom=100)

    h = hud.Hud(screen)

    e = eventhandler.Eventhandler(screen)

    return (screen, camera, h, w, e)

def main_loop(screen, camera, hud, world, eventhandler):
    glClearColor(0, 0, 0, 1)
    while not screen.has_exit:
        screen.dispatch_events()
            
        world.tick(eventhandler.paused)
            
        camera.world()
        world.draw()

        camera.hud()
        hud.draw()

        pyglet.clock.tick()
        screen.flip()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        f = open(sys.argv[1], 'r')
        line = f.readline()
        inp = eval(line) # hue, hue, hue
        if isinstance(inp, dict):
            (screen, camera, hud, world, eventhandler) = init(800, 800, inp)
    else:
        (screen, camera, hud, world, eventhandler) = init(800, 800)

    main_loop(screen, camera, hud, world, eventhandler)

