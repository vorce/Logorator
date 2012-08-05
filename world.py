import pyglet
from pyglet.gl import *
import random
import os, sys, inspect
#cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
#if cmd_folder not in sys.path:
#    sys.path.insert(0, cmd_folder)
sys.path.insert(0, 'generators')
import testgen

class World(object):
    def __init__(self, win, seeds):
        self.gens = [testgen.TestGen(win.width, win.height, (-75, 75)),
                     testgen.TestGen(win.width, win.height, (0, 75)),
                     testgen.TestGen(win.width, win.height, (75, 75)),
                     testgen.TestGen(win.width, win.height, (-75, 0)),
                     testgen.TestGen(win.width, win.height, (0, 0)),
                     testgen.TestGen(win.width, win.height, (75, 0)),
                     testgen.TestGen(win.width, win.height, (-75, -75)),
                     testgen.TestGen(win.width, win.height, (0, -75)),
                     testgen.TestGen(win.width, win.height, (75, -75))]

        if seeds != None:
            for g in self.gens:
                g.seed = seeds
        else:
            self.create_seeds(0)

        self.paused = False
        #self.entities = {}
        #self.nextEntity = 0
        #pyglet.clock.schedule_interval(self.spawnEntity, 1)
        pyglet.clock.schedule_interval(self.create_seeds, 10)
        #self.batch = pyglet.graphics.Batch()
        #pass

    #def spawnEntity(self, dt):
        #print("spawning..")
        #probe = probes.MeleeProbe(self.nextEntity, (400, 300), 0)
        #self.entities[probe.id] = probe
        #self.nextEntity += 1
        #return probe
        #ent = entity.Foo(self.nextEntity, size, x, y, rot)
        #probe = probes.MeleeProbe(self.nextEntity,
                                  #(100.0, random.uniform(-100.0,100.0)),
                                  #1, self.batch)
        #self.entities[probe.id] = probe
        #self.nextEntity += 1
        #return probe

    #def updateBaseStats(self, dt):
        #for ent in self.entities.values():
            #ent.updateBaseStats()

    def create_seed(self, gen):
        s = {}
        for p in gen.params:
            s[p] = gen.params[p].next()
        gen.seed = s
        

    def create_seeds(self, dt):
        if not self.paused:
            for g in self.gens:
                self.create_seed(g)
                print("seed: {0}".format(g.dump()))
        #for ent in self.entities.values():
            #ent.update()

    def tick(self, paused):
        self.paused = paused

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        #self.batch.draw()
        for g in self.gens:
            g.render(None)

