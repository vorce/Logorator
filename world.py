import pyglet
from pyglet.gl import *
import random
import os, sys, inspect
#cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
#if cmd_folder not in sys.path:
#    sys.path.insert(0, cmd_folder)
sys.path.insert(0, 'generators')
import testgen
import lsysgen
import textgen

class World(object):
    def __init__(self, win, seeds):
        self.paused = False
        self.win = win

        self.gens = [((0, int(win.height/1.5)), textgen.TextGen()),
                    #((0, int(win.height/1.5)), testgen.TestGen()),
                     ((win.width/3, int(win.height/1.5)), lsysgen.LSysGen()),
                     ((int(win.width/1.5), int(win.height/1.5)), testgen.TestGen()),
                     ((0, win.height/3), testgen.TestGen()),
                     ((win.width/3, win.height/3), lsysgen.LSysGen()),
                     ((int(win.width/1.5), win.height/3), testgen.TestGen()),

                     ((0, 0), testgen.TestGen()),
                     ((win.width/3, 0), testgen.TestGen()),
                     ((int(win.width/1.5), 0), testgen.TestGen())]

        if seeds != None:
            (module, generator) = seeds.get('__generator__', ('testgen',
                                                              'TestGen'))

            new_gens = []
            for g in self.gens:
                print("module: {0}, generator: {1}".format(module, generator))
                ((x, y), tmp) = g
                genclass = reduce(getattr, [generator],
                                  sys.modules[module])
                gen = genclass()
                gen.seed = seeds
                newgen = ((x, y), gen)
                new_gens.append(newgen)
            self.gens = new_gens
            print(self.gens)
        else:
            self.create_seeds(0)

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
        s = {'__generator__':(gen.__module__, gen.__class__.__name__)}
        for p in gen.params:
            s[p] = gen.params[p].next()
        gen.seed = s
        

    def create_seeds(self, dt):
        if not self.paused:
            for g in self.gens:
                (c, gen) = g
                self.create_seed(gen)
                print("seed: {0}".format(gen.dump()))
            print("------------------")
        #for ent in self.entities.values():
            #ent.update()

    def tick(self, events):
        self.paused = events.paused
        if events.next_seeds:
            self.create_seeds(None)
            events.next_seeds = False

    def _setup_view(self, coords):
        (x, y) = coords
        glViewport(x, y, self.win.width/3, self.win.height/3)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        zoom = 50.0
        width_ratio = (self.win.width/3) / (self.win.height/3)
        gluOrtho2D(-zoom * width_ratio,
                   zoom * width_ratio,
                   -zoom,
                   zoom)

        glPushAttrib(GL_ENABLE_BIT|GL_SCISSOR_BIT)
        glEnable(GL_SCISSOR_TEST)
        glScissor(x, y, self.win.width/3, self.win.height/3)

    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT)

        for g in self.gens:
            (coords, gen) = g
            self._setup_view(coords)
            gen.render(None)
            glPopAttrib()

        glDisable(GL_SCISSOR_TEST)
        glFlush()
        
