import pyglet
from pyglet.gl import *
import random
import os, sys, inspect
import itertools
sys.path.insert(0, 'generators')
import testgen
import lsysgen
import textgen

class GenView():
    """
    A view for zero or more generators.
    """
    def __init__(self, position, dimensions, gens = None):
        self.pos = position
        self.gens = gens
        self.width, self.height = dimensions
        self._structure_gens()
    
    def _structure_gens(self):
        s_gens = {}
        for g in self.gens:
            mod_class = (g.__module__, g.__class__.__name__)
            ll = s_gens.get(mod_class, [])
            ll.append(g)
            s_gens[mod_class] = ll
        self.s_gens = s_gens

    def _setup_view(self, width, height, coords):
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

    def render(self, multi_view = True):
        if multi_view:
            self._setup_view(self.width, self.height, self.pos)

        for g in self.gens: 
            g.render()

        if multi_view:
            glPopAttrib()

    def mix(self, another_view):
        """
        Mix this view with another_view,
        creating a new view.
        """
        new_gens = {}
        for smc in self.s_gens:
            for amc in another_view.s_gens:
                if smc == amc:
                    (sm, sc) = smc
                    (am, ac) = amc
                    for sg in self.s_gens[smc]:
                        for ag in another_view.s_gens[amc]:
                            #import pdb; pdb.set_trace()
                            try:
                                ng = sg.mix(ag)
                            except AttributeError:
                                ng = getattr(sys.modules[sm], sc)()
                                for s in sg.seed:
                                    if s == '__generator__':
                                        continue
                                    ng.seed[s] = (sg.seed[s] + ag.seed[s]) / 2

                            ll = new_gens.get(smc, [])
                            ll.append(ng)
                            new_gens[smc] = ll
            if new_gens.get(smc, []) == []:
                new_gens[smc] = self.s_gens[smc]

        # import pdb; pdb.set_trace()
        # deal with more gens of a type than max in any of the two sets
        for nmc in new_gens:
            max_c = max(len(self.s_gens.get(nmc, [])),
                        len(another_view.s_gens.get(nmc, [])))
            while len(new_gens[nmc]) > max_c:
                new_gens[nmc].pop(random.randint(0, len(new_gens[nmc])-1))

        only_gens = list(itertools.chain.from_iterable(new_gens.values()))
        gv = GenView((0, 0), (self.width, self.height), only_gens)
        
        return gv



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
                              [lsysgen.LSysGen(), testgen.TestGen(),
                               testgen.TestGen(), testgen.TestGen()]),
                      GenView((int(win.width/1.5), int(win.height/1.5)), (w, h),
                              [testgen.TestGen(), testgen.TestGen(),
                               lsysgen.LSysGen()]),

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

            # Mix the second and third view to form a new one, and place it
            # in the lower right position.
            gv = self.views[1].mix(self.views[2])
            gv.pos = (int(win.width/1.5), 0)
            self.views[8] = gv

        pyglet.clock.schedule_interval(self.create_seeds, 10)

    def create_seed(self, gen):
        s = {'__generator__':(gen.__module__, gen.__class__.__name__)}
        for p in gen.params:
            s[p] = gen.params[p].next()
        gen.seed = s
        

    def create_seeds(self, dt):
        for v in self.views:
            for g in v.gens:
                self.create_seed(g)
                print("seed: {0}".format(g.dump()))
        print("-------------------")

    def tick(self, events):
        if not self.paused and events.paused:
            pyglet.clock.unschedule(self.create_seeds)
        elif self.paused and not events.paused:
            pyglet.clock.schedule_interval(self.create_seeds, 10)

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
        
