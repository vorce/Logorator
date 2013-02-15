"""
Logorator is meant to be a prototype tool to assist with
creating generated graphic designs.

2012 Joel Carlbark (c)
"""

import random
import sys

import pyglet
from pyglet.gl import *

import eventhandler
import utils
import hud
import world


def init(width, height, inp=None):
    pyglet.clock.set_fps_limit(60)

    config = Config(sample_buffers=1, samples=4, depth_size=16,
                    double_buffer=True,)

    screen = pyglet.window.Window(width=width, height=height,
                                  config=config)

    w = world.World(screen, inp)

    camera = utils.Camera(screen, zoom=100)

    h = hud.Hud(screen)

    e = eventhandler.Eventhandler(screen)

    return (screen, camera, h, w, e)


def main_loop(screen, camera, myhud, myworld, myeventhandler):
    glClearColor(0, 0, 0, 1)
    while not screen.has_exit:
        screen.dispatch_events()

        myworld.tick(myeventhandler)

        camera.world()
        myworld.draw()

        camera.hud()
        myhud.draw()

        pyglet.clock.tick()
        screen.flip()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        f = open(sys.argv[1], 'r')
        line = f.readline()
        inp = eval(line)  # hue, hue, hue
        if isinstance(inp, list):
            (screen, cam, myhud, myworld, myeventhandler) = init(800, 800, inp)
    else:
        (screen, cam, myhud, myworld, myeventhandler) = init(800, 800)

    main_loop(screen, cam, myhud, myworld, myeventhandler)
