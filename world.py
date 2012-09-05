import pyglet
from pyglet.gl import *
import random
import os, sys, inspect
sys.path.insert(0, 'generators')
import testgen
import lsysgen
import textgen

def _setup_view(width, height, coords):
        (x, y) = coords
        glViewport(x, y, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        zoom = 50.0
        width_ratio = width / height
        gluOrtho2D(-zoom * width_ratio,
                   zoom * width_ratio,
                   -zoom,
                   zoom)

        glPushAttrib(GL_ENABLE_BIT | GL_SCISSOR_BIT)
        glEnable(GL_SCISSOR_TEST)
        glScissor(x, y, width, height)

class GenView():
    """
    A view for one or more generators.
    """
    def __init__(self, position, dimensions, gens = None):
        self.pos = position
        self.gens = gens
        self.width, self.height = dimensions

    def render(self, multi_view = True):
        if multi_view:
            _setup_view(self.width, self.height, self.pos)

        for g in self.gens:
            g.render(None)

        if multi_view:
            glPopAttrib()


class World(object):
    def __init__(self, win, seeds):
        self.paused = False
        self.multi_view = True
        self.win = win
        
        self.single_gen = None

        w = win.width / 3
        h = win.height / 3

        self.views = [GenView((0, int(win.height/1.5)), (w, h),
                              [textgen.TextGen()]),
                      GenView((w, int(win.height/1.5)), (w, h),
                              [lsysgen.LSysGen(), testgen.TestGen()]),
                      GenView((int(win.width/1.5), int(win.height/1.5)), (w, h),
                              [testgen.TestGen(), testgen.TestGen()]),

                      GenView((0, h), (w, h),
                              [testgen.TestGen()]),
                      GenView((w, h), (w, h),
                              [lsysgen.LSysGen(), lsysgen.LSysGen()]),
                      GenView((int(win.width/1.5), h), (w, h),
                              [testgen.TestGen()]),

                      GenView((0, 0), (w, h),
                              [lsysgen.LSysGen()]),
                      GenView((w, 0), (w, h),
                              [testgen.TestGen()]),
                      GenView((int(win.width/1.5), 0), (w, h),
                              [])
                    ]

        if seeds != None:
            # Untested!
            newgens = []
            for s in seeds:
                (module, generator) = s.get('__generator__', ('testgen',
                                                              'TestGen'))
                genclass = reduce(getattr, [generator], sys.modules[module])
                gen = genclass()
                gen.seed = s
                newgens.append(gen)

            for v in self.views:
                v.gens = newgens
                
            print(self.views)
        else:
            self.create_seeds(0)

        pyglet.clock.schedule_interval(self.create_seeds, 10)

    def create_seed(self, gen):
        s = {'__generator__':(gen.__module__, gen.__class__.__name__)}
        for p in gen.params:
            s[p] = gen.params[p].next()
        gen.seed = s
        

    def create_seeds(self, dt):
        if not self.paused:
            for v in self.views:
                for g in v.gens:
                    self.create_seed(g)
                    print("seed: {0}".format(g.dump()))
            print("-------------------")

    def tick(self, events):
        self.paused = events.paused
        self.multi_view = events.multi_view

        if events.next_seeds:
            self.create_seeds(None)
            events.next_seeds = False

        if events.click_coord and not self.multi_view:
            self.single_gen = self.__get_gen_view(events.click_coord)

    def __get_gen_view(self, coords):
        (x, y) = coords
        
        if x < int(self.win.width/3):
            if y < int(self.win.height/3):
                return self.views[6]
            elif y < int(self.win.height/1.5):
                return self.views[3]
            else:
                return self.views[0]
        elif x < int(self.win.width/1.5):
            if y < int(self.win.height/3):
                return self.views[7]
            elif y < int(self.win.height/1.5):
                return self.views[4]
            else:
                return self.views[1]
        else:
            if y < int(self.win.height/3):
                return self.views[8]
            elif y < int(self.win.height/1.5):
                return self.views[5]
            else:
                return self.views[2]


    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT)

        if self.multi_view:
            for v in self.views:
                v.render(True)
            glDisable(GL_SCISSOR_TEST)

        elif self.single_gen:
            self.single_gen.render(False)
        
